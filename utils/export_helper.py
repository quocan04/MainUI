import json
import csv
from typing import List
from datetime import datetime
from pathlib import Path
import logging

from models.reader import Reader
from config.settings import AppConfig

logger = logging.getLogger(__name__)


class ExportHelper:
    """Helper class để xuất dữ liệu ra các định dạng khác nhau"""

    @staticmethod
    def export_to_json(readers: List[Reader], filename: str = None) -> tuple[bool, str]:
        """
        Xuất danh sách bạn đọc ra file JSON

        Returns:
            tuple: (success, message hoặc filepath)
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = AppConfig.EXPORT_DIR / f"readers_{timestamp}.json"

            data = {
                'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_records': len(readers),
                'readers': [reader.to_dict() for reader in readers]
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Đã xuất {len(readers)} bạn đọc ra JSON:  {filename}")
            return True, str(filename)

        except Exception as e:
            logger.error(f"❌ Lỗi xuất JSON: {e}")
            return False, f"Lỗi:  {str(e)}"

    @staticmethod
    def export_to_csv(readers: List[Reader], filename: str = None) -> tuple[bool, str]:
        """
        Xuất danh sách bạn đọc ra file CSV

        Returns:
            tuple:  (success, message hoặc filepath)
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = AppConfig.EXPORT_DIR / f"readers_{timestamp}. csv"

            with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)

                # Header
                writer.writerow([
                    'ID', 'Họ tên', 'Địa chỉ', 'Điện thoại', 'Email',
                    'Ngày cấp thẻ', 'Ngày hết hạn', 'Trạng thái', 'Điểm uy tín'
                ])

                # Data
                for reader in readers:
                    writer.writerow([
                        reader.reader_id or '',
                        reader.full_name or '',
                        reader.address or '',
                        reader.phone or '',
                        reader.email or '',
                        reader.card_start or '',
                        reader.card_end or '',
                        reader.status or '',
                        reader.reputation_score or ''
                    ])

            logger.info(f"✅ Đã xuất {len(readers)} bạn đọc ra CSV: {filename}")
            return True, str(filename)

        except Exception as e:
            logger.error(f"❌ Lỗi xuất CSV: {e}")
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def export_to_excel(readers: List[Reader], filename: str = None) -> tuple[bool, str]:
        """
        Xuất danh sách bạn đọc ra file Excel

        Returns:
            tuple: (success, message hoặc filepath)
        """
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, PatternFill

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = AppConfig.EXPORT_DIR / f"readers_{timestamp}.xlsx"

            wb = Workbook()
            ws = wb.active
            ws.title = "Danh sách Bạn đọc"

            # Header style
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")

            # Headers
            headers = [
                'ID', 'Họ tên', 'Địa chỉ', 'Điện thoại', 'Email',
                'Ngày cấp thẻ', 'Ngày hết hạn', 'Trạng thái', 'Điểm uy tín'
            ]

            for col, header in enumerate(headers, start=1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment

            # Data
            for row, reader in enumerate(readers, start=2):
                ws.cell(row=row, column=1, value=reader.reader_id or '')
                ws.cell(row=row, column=2, value=reader.full_name or '')
                ws.cell(row=row, column=3, value=reader.address or '')
                ws.cell(row=row, column=4, value=reader.phone or '')
                ws.cell(row=row, column=5, value=reader.email or '')
                ws.cell(row=row, column=6, value=reader.card_start or '')
                ws.cell(row=row, column=7, value=reader.card_end or '')
                ws.cell(row=row, column=8, value=reader.status or '')
                ws.cell(row=row, column=9, value=reader.reputation_score or '')

            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width

            wb.save(filename)

            logger.info(f"✅ Đã xuất {len(readers)} bạn đọc ra Excel: {filename}")
            return True, str(filename)

        except ImportError:
            return False, "Chưa cài đặt thư viện openpyxl.  Chạy:  pip install openpyxl"
        except Exception as e:
            logger.error(f"❌ Lỗi xuất Excel: {e}")
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def export_to_pdf(readers: List[Reader], filename: str = None) -> tuple[bool, str]:
        """
        Xuất danh sách bạn đọc ra file PDF

        Returns:
            tuple: (success, message hoặc filepath)
        """
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = AppConfig.EXPORT_DIR / f"readers_{timestamp}.pdf"

            # Create PDF
            doc = SimpleDocTemplate(
                str(filename),
                pagesize=landscape(A4),
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=18
            )

            # Container for elements
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1976D2'),
                spaceAfter=30,
                alignment=1  # Center
            )

            # Title
            title = Paragraph("DANH SÁCH BẠN ĐỌC", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.2 * inch))

            # Info
            info_text = f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Tổng số:  {len(readers)} bạn đọc"
            info = Paragraph(info_text, styles['Normal'])
            elements.append(info)
            elements.append(Spacer(1, 0.3 * inch))

            # Table data
            data = [['ID', 'Họ tên', 'Điện thoại', 'Email', 'Ngày cấp', 'Ngày HH', 'Trạng thái', 'Điểm UT']]

            for reader in readers:
                data.append([
                    str(reader.reader_id or ''),
                    reader.full_name or '',
                    reader.phone or '',
                    reader.email or '',
                    reader.card_start or '',
                    reader.card_end or '',
                    reader.status or '',
                    str(reader.reputation_score or '')
                ])

            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(table)

            # Build PDF
            doc.build(elements)

            logger.info(f"✅ Đã xuất {len(readers)} bạn đọc ra PDF: {filename}")
            return True, str(filename)

        except ImportError:
            return False, "Chưa cài đặt thư viện reportlab. Chạy: pip install reportlab"
        except Exception as e:
            logger.error(f"❌ Lỗi xuất PDF: {e}")
            return False, f"Lỗi: {str(e)}"