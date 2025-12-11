"""
Library Management System - Main Entry Point
============================================

Hệ thống quản lý thư viện với Python GUI
Sử dụng:  Tkinter + MySQL + MVC Architecture

Author: NvkhoaDev54
Version: 1.0.0
Year: 2025
"""

import tkinter as tk
from tkinter import messagebox
import sys
import logging
from pathlib import Path

# Setup logging
log_dir = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging. FileHandler(log_dir / 'app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Kiểm tra các thư viện cần thiết"""
    required_packages = {
        'mysql': 'mysql-connector-python',           # ✅ FIX: mysql chứ không phải mysql.connector
        'openpyxl': 'openpyxl',
        'reportlab': 'reportlab',
        'dotenv': 'python-dotenv'
    }

    missing = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            logger. info(f"✓ Package '{package}' found")
        except ImportError:
            logger.warning(f"✗ Package '{package}' not found")
            missing.append(pip_name)

    if missing:
        error_msg = (
            "❌ Thiếu các thư viện sau:\n\n" +
            "\n".join(f"  • {pkg}" for pkg in missing) +
            "\n\nVui lòng cài đặt:\n" +
            f"pip install {' '.join(missing)}"
        )
        messagebox.showerror("Thiếu thư viện", error_msg)
        return False

    logger.info("✅ All dependencies OK")
    return True


def main():
    """Entry point của ứng dụng"""
    try:
        logger.info("="*50)
        logger.info("Starting Library Management System")
        logger.info("="*50)

        # Check dependencies
        if not check_dependencies():
            logger.error("Dependencies check failed")
            sys.exit(1)

        # Import views (after dependency check)
        from views.main_window import MainWindow

        # Create and run application
        logger.info("Creating main window...")
        app = MainWindow()

        logger.info("✅ Application started successfully")

        # Start main loop
        app.mainloop()

    except KeyboardInterrupt:
        logger. info("Application interrupted by user (Ctrl+C)")
        sys.exit(0)

    except ImportError as e:
        logger. critical(f"Import error: {e}", exc_info=True)
        messagebox. showerror(
            "Lỗi Import",
            f"Không thể import module:\n\n{str(e)}\n\n"
            f"Vui lòng kiểm tra:\n"
            f"1. Đã cài đặt đầy đủ dependencies\n"
            f"2. Đang chạy trong virtual environment đúng\n"
            f"3. Cấu trúc thư mục đúng"
        )
        sys.exit(1)

    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        messagebox. showerror(
            "Lỗi nghiêm trọng",
            f"Ứng dụng gặp lỗi không mong muốn:\n\n{str(e)}\n\n"
            f"Vui lòng xem file log để biết thêm chi tiết:\n"
            f"{log_dir / 'app. log'}"
        )
        sys.exit(1)

    finally:
        logger.info("Application shutdown")
        logger.info("="*50)


if __name__ == "__main__":
    main()