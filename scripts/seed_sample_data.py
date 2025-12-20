"""
Script thêm dữ liệu mẫu cho AI Forecast
Chạy: python scripts/seed_sample_data.py
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db


def clear_old_data():
    """Xóa dữ liệu test cũ (optional)"""
    print("🗑️  Đang xóa dữ liệu test cũ...")

    # Không xóa dữ liệu thật, chỉ xóa dữ liệu test
    # Bạn có thể bỏ qua bước này nếu muốn giữ dữ liệu hiện tại

    print("✅ Đã xóa dữ liệu test cũ")


def seed_borrow_slips():
    """Thêm dữ liệu mượn sách cho 12 tháng"""
    print("\n📚 Đang thêm dữ liệu mượn sách...")

    # Lấy reader_id và staff_id có sẵn
    reader = db.fetchone("SELECT reader_id FROM readers LIMIT 1")
    staff = db.fetchone("SELECT staff_id FROM staff LIMIT 1")

    if not reader or not staff:
        print("⚠️  Cần có ít nhất 1 reader và 1 staff trong DB")
        print("   Vui lòng tạo dữ liệu cơ bản trước")
        return

    reader_id = reader['reader_id']
    staff_id = staff['staff_id']

    today = datetime.now()

    for month_ago in range(12, 0, -1):
        # Tính ngày của tháng đó
        target_date = today - timedelta(days=month_ago * 30)

        # Số lượt mượn tăng dần (450 -> 650)
        base_count = 400 + (12 - month_ago) * 20
        count = base_count + random.randint(-20, 30)

        print(f"  Tháng {target_date.strftime('%Y-%m')}: {count} lượt mượn")

        # Thêm nhiều bản ghi mượn
        for i in range(count):
            borrow_date = target_date - timedelta(days=random.randint(0, 28))
            return_due = borrow_date + timedelta(days=14)

            query = """
            INSERT INTO borrow_slips 
            (reader_id, staff_id, borrow_date, return_due, status)
            VALUES (%s, %s, %s, %s, 'RETURNED')
            """

            try:
                db.execute(query, (reader_id, staff_id, borrow_date, return_due))
            except Exception as e:
                print(f"    ⚠️  Lỗi thêm borrow slip: {e}")
                break

    print("✅ Hoàn tất thêm dữ liệu mượn sách")


def seed_penalties():
    """Thêm dữ liệu phạt cho 12 tháng"""
    print("\n💰 Đang thêm dữ liệu phạt...")

    reader = db.fetchone("SELECT reader_id FROM readers ORDER BY RAND() LIMIT 1")
    book = db.fetchone("SELECT book_id FROM books ORDER BY RAND() LIMIT 1")

    if not reader or not book:
        print("⚠️  Thiếu reader hoặc book")
        return

    today = datetime.now()

    for month_ago in range(12, 0, -1):
        target_date = today - timedelta(days=month_ago * 30)

        base_revenue = 2200000 + (12 - month_ago) * 180000
        total_revenue = base_revenue + random.randint(-400000, 400000)

        print(f"  Tháng {target_date.strftime('%Y-%m')}: {total_revenue:,.0f} VNĐ")

        num_penalties = random.randint(15, 40)
        amount_per_penalty = round(total_revenue / num_penalties, 2)

        for _ in range(num_penalties):
            slip = db.fetchone("""
                SELECT slip_id 
                FROM borrow_slips 
                ORDER BY RAND() 
                LIMIT 1
            """)

            if not slip:
                continue

            penalty_type = random.choice(['LATE', 'LOST', 'DAMAGED'])

            query = """
            INSERT INTO penalties 
            (reader_id, slip_id, book_id, penalty_type, amount)
            VALUES (%s, %s, %s, %s, %s)
            """

            db.execute(query, (
                reader['reader_id'],
                slip['slip_id'],
                book['book_id'],
                penalty_type,
                amount_per_penalty
            ))

    print("✅ Hoàn tất thêm dữ liệu phạt")


def seed_readers():
    """Thêm bạn đọc mới cho 12 tháng"""
    print("\n👥 Đang thêm dữ liệu bạn đọc mới...")

    today = datetime.now()

    for month_ago in range(12, 0, -1):
        target_date = today - timedelta(days=month_ago * 30)

        base_count = 30 + (12 - month_ago) * 4
        count = base_count + random.randint(-5, 8)

        print(f"  Tháng {target_date.strftime('%Y-%m')}: {count} bạn đọc mới")

        for i in range(count):
            card_start = target_date - timedelta(days=random.randint(0, 28))
            card_end = card_start + timedelta(days=365)

            query = """
            INSERT INTO readers 
            (full_name, address, phone, email, card_start, card_end)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            db.execute(query, (
                f"Test Reader {month_ago}_{i}",
                f"Test Address {i}",
                f"090{random.randint(1000000, 9999999)}",
                f"test{month_ago}_{i}@example.com",
                card_start.date(),
                card_end.date()
            ))

    print("✅ Hoàn tất thêm dữ liệu bạn đọc")


def verify_data():
    """Kiểm tra dữ liệu đã thêm"""
    print("\n📊 Kiểm tra dữ liệu...")

    # Đếm borrow_slips
    result = db.fetchone("SELECT COUNT(*) as count FROM borrow_slips")
    print(f"  📚 Tổng lượt mượn: {result['count']}")

    # Đếm penalties
    result = db.fetchone("SELECT COUNT(*) as count, SUM(amount) as total FROM penalties")
    print(f"  💰 Tổng phạt: {result['count']} khoản = {result['total']:,.0f} VNĐ")

    # Đếm readers
    result = db.fetchone("SELECT COUNT(*) as count FROM readers")
    print(f"  👥 Tổng bạn đọc: {result['count']}")

    # Kiểm tra dữ liệu theo tháng
    result = db.fetchall("""
        SELECT 
            DATE_FORMAT(borrow_date, '%Y-%m') as month,
            COUNT(*) as count
        FROM borrow_slips
        WHERE borrow_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month DESC
        LIMIT 3
    """)

    print("\n  📅 3 tháng gần nhất:")
    for row in result:
        print(f"     {row['month']}: {row['count']} lượt mượn")


def main():
    print("=" * 60)
    print("🌱 THÊM DỮ LIỆU MẪU CHO AI FORECAST")
    print("=" * 60)

    try:
        # Kiểm tra kết nối
        if not db.test_connection():
            print("❌ Không thể kết nối database!")
            return

        print("✅ Kết nối database thành công\n")

        # Thêm dữ liệu
        seed_borrow_slips()
        seed_penalties()
        seed_readers()

        # Kiểm tra
        verify_data()

        print("\n" + "=" * 60)
        print("✅ HOÀN TẤT! Dữ liệu đã được thêm vào database")
        print("=" * 60)
        print("\n🎯 Bây giờ bạn có thể:")
        print("  1. Refresh API: http://localhost:5000/api/ai/forecast")
        print("  2. Refresh Dashboard: http://localhost:8000/ai-dashboard.html")
        print("  3. Xem biểu đồ dự đoán đầy đủ!\n")

    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()