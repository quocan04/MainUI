import pandas as pd
from tkinter import filedialog
from datetime import datetime
from services.report_service import ReportService


class ReportController:
    def __init__(self):
        self.service = ReportService()

    def get_dashboard_data(self, mode='month'):
        """
        Lấy toàn bộ dữ liệu hiển thị lên Dashboard.
        Tham số mode: 'day' | 'month' | 'year' (để lọc biểu đồ mượn)
        """
        return {
            "borrow_stats": self.service.get_borrow_stats(mode=mode),
            "top_readers": self.service.get_top_readers(limit=10),
            # Lấy top 10 cho Excel, View hiển thị bao nhiêu tùy ý
            "damaged_lost": self.service.get_damaged_lost_books(),
            "inventory": self.service.get_inventory_stats()
        }

    def export_to_excel(self):
        """
        Xuất toàn bộ báo cáo ra file Excel (.xlsx)
        """
        try:
            # 1. Lấy dữ liệu mới nhất (Mặc định lấy theo tháng cho báo cáo tổng quan)
            data = self.get_dashboard_data(mode='month')

            # 2. Chuẩn bị các DataFrame (Bảng dữ liệu) cho từng Sheet

            # --- Sheet 1: Thống kê mượn ---
            df_borrow = pd.DataFrame(data['borrow_stats'])
            if not df_borrow.empty:
                df_borrow.columns = ['Thời gian', 'Số lượt mượn']

            # --- Sheet 2: Top bạn đọc ---
            df_readers = pd.DataFrame(data['top_readers'])
            if not df_readers.empty:
                # Chọn cột và đổi tên tiếng Việt
                if 'reader_id' in df_readers.columns:
                    df_readers = df_readers[['reader_id', 'full_name', 'borrow_count']]
                    df_readers.columns = ['Mã bạn đọc', 'Họ tên', 'Số lần mượn']

            # --- Sheet 3: Sách Hư hỏng / Mất ---
            df_risk = pd.DataFrame(data['damaged_lost'])
            if not df_risk.empty:
                # Map tên loại phạt sang tiếng Việt
                type_map = {'LOST': 'Mất sách', 'DAMAGED': 'Hư hỏng', 'LATE': 'Trễ hạn'}
                df_risk['penalty_type'] = df_risk['penalty_type'].map(type_map).fillna(df_risk['penalty_type'])

                df_risk.columns = ['Loại vi phạm', 'Số lượng', 'Tổng tiền phạt']

            # --- Sheet 4: Tổng quan Kho ---
            inv = data['inventory']
            # Tạo bảng tổng quan
            df_inventory_general = pd.DataFrame([
                {'Chỉ số': 'Tổng đầu sách', 'Giá trị': inv['total']},
                {'Chỉ số': 'Đang cho mượn', 'Giá trị': inv['borrowed']},
                {'Chỉ số': 'Còn trong kho', 'Giá trị': inv['available']}
            ])
            # Tạo bảng chi tiết thể loại
            df_categories = pd.DataFrame(inv['categories'])
            if not df_categories.empty:
                df_categories.columns = ['Thể loại', 'Số lượng']

            # 3. Mở hộp thoại chọn nơi lưu file
            filename = f"Bao_cao_Thu_vien_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            save_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=filename,
                title="Lưu file báo cáo Excel",
                filetypes=[("Excel files", "*.xlsx")]
            )

            if save_path:
                # 4. Ghi dữ liệu vào file Excel (Sử dụng engine openpyxl)
                with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                    if not df_inventory_general.empty:
                        df_inventory_general.to_excel(writer, sheet_name='Tổng Quan', index=False)

                    if not df_categories.empty:
                        df_categories.to_excel(writer, sheet_name='Chi tiết Thể loại', index=False)

                    if not df_borrow.empty:
                        df_borrow.to_excel(writer, sheet_name='Xu hướng Mượn', index=False)

                    if not df_readers.empty:
                        df_readers.to_excel(writer, sheet_name='Top Bạn Đọc', index=False)

                    if not df_risk.empty:
                        df_risk.to_excel(writer, sheet_name='Rủi ro & Phạt', index=False)

                return True, f"Đã xuất file thành công tại:\n{save_path}"

            return False, "Đã hủy lưu file."

        except Exception as e:
            # In lỗi ra console để debug nếu cần
            print(f"Lỗi xuất Excel: {e}")
            return False, f"Có lỗi xảy ra khi xuất file:\n{str(e)}"