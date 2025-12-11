import mysql.connector
from mysql.connector import pooling, Error
from typing import Optional, Any
import logging

from config.settings import DatabaseConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Singleton class quản lý MySQL database connection pool"""

    _instance: Optional['Database'] = None
    _connection_pool: Optional[pooling.MySQLConnectionPool] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Khởi tạo connection pool"""
        if self._connection_pool is None:
            self._create_connection_pool()

    def _create_connection_pool(self):
        """Tạo MySQL connection pool"""
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                **DatabaseConfig.get_pool_config()
            )
            logger.info(f"✅ Đã tạo connection pool: {DatabaseConfig.DATABASE}")

            # Test connection
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                logger.info(f"✅ MySQL Version: {version[0]}")
                cursor.close()
                conn.close()

        except Error as e:
            logger.error(f"❌ Lỗi tạo connection pool: {e}")
            raise

    def get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Lấy connection từ pool
        QUAN TRỌNG: Phải close() connection sau khi sử dụng
        """
        try:
            if self._connection_pool is None:
                self._create_connection_pool()

            connection = self._connection_pool.get_connection()
            return connection

        except Error as e:
            logger.error(f"❌ Lỗi lấy connection: {e}")
            return None

    def execute_query(
            self,
            query: str,
            params: tuple = None,
            fetch: bool = False,
            commit: bool = False
    ) -> Any:
        """
        Helper method để execute query

        Args:
            query: SQL query
            params: Parameters cho prepared statement
            fetch: True nếu cần fetch kết quả (SELECT)
            commit: True nếu cần commit (INSERT/UPDATE/DELETE)

        Returns:
            - Nếu fetch=True: trả về list of tuples
            - Nếu commit=True: trả về lastrowid hoặc rowcount
            - Nếu lỗi: trả về None
        """
        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            if not connection:
                return None

            cursor = connection.cursor(dictionary=True)  # Trả về dict

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()
                return result

            if commit:
                connection.commit()
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

            return True

        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"❌ Lỗi execute query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            return None

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def test_connection(self) -> bool:
        """Test kết nối database"""
        try:
            conn = self.get_connection()
            if conn:
                conn.close()
                logger.info("✅ Test connection thành công")
                return True
            return False
        except Error as e:
            logger.error(f"❌ Test connection thất bại: {e}")
            return False

    def close_pool(self):
        """Đóng toàn bộ connection pool"""
        if self._connection_pool:
            # MySQL connector không có close pool method
            # Chỉ cần set None, Python garbage collector sẽ xử lý
            self._connection_pool = None
            logger.info("✅ Đã đóng connection pool")


# Singleton instance
db = Database()