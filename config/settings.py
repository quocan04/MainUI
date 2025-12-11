import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class DatabaseConfig:
    """Cấu hình kết nối MySQL Database"""

    HOST = os.getenv('DB_HOST', '127.0.0.1')
    PORT = int(os.getenv('DB_PORT', 3307))
    USER = os.getenv('DB_USER', 'nvkhoadev')
    PASSWORD = os.getenv('DB_PASSWORD', '05042004')
    DATABASE = os.getenv('DB_NAME', 'library_management')

    # Connection pool settings
    POOL_NAME = 'library_pool'
    POOL_SIZE = 10
    POOL_RESET_SESSION = True

    @classmethod
    def get_config(cls) -> Dict[str, any]:
        """Trả về dict config cho MySQL connector"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': False,
            'raise_on_warnings': False,
            'use_pure': True
        }

    @classmethod
    def get_pool_config(cls) -> Dict[str, any]:
        """Config cho connection pool"""
        config = cls.get_config()
        config.update({
            'pool_name': cls.POOL_NAME,
            'pool_size': cls.POOL_SIZE,
            'pool_reset_session': cls.POOL_RESET_SESSION
        })
        return config


class AppConfig:
    """Cấu hình ứng dụng"""

    APP_NAME = os.getenv('APP_NAME', 'Library Management System')
    VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # Thư mục
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data'
    EXPORT_DIR = DATA_DIR / 'export'
    TEMP_DIR = DATA_DIR / 'temp'

    # Tạo các thư mục nếu chưa tồn tại
    for directory in [DATA_DIR, EXPORT_DIR, TEMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    # Settings
    MAX_SEARCH_RESULTS = 1000
    ITEMS_PER_PAGE = 50
    DEFAULT_CARD_VALIDITY_DAYS = 365

    # Colors
    COLOR_PRIMARY = '#2196F3'
    COLOR_SUCCESS = '#4CAF50'
    COLOR_WARNING = '#FF9800'
    COLOR_DANGER = '#F44336'
    COLOR_INFO = '#00BCD4'