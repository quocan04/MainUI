"""
HTML Report Helper - Tạo báo cáo thống kê dạng HTML với biểu đồ
"""
import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class HTMLReportHelper:
    """Helper class để tạo báo cáo HTML với biểu đồ"""

    @staticmethod
    def create_reader_statistics_report(stats: Dict, readers: List = None) -> str:
        """
        Tạo báo cáo thống kê bạn đọc dạng HTML

        Args:
            stats: Dictionary chứa thống kê
            readers: List các reader objects (optional)

        Returns:
            str: Đường dẫn đến file HTML đã tạo
        """
        try:
            # Tạo thư mục reports nếu chưa có
            reports_dir = Path.cwd() / "reports"
            reports_dir.mkdir(exist_ok=True)

            # Tên file với timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = reports_dir / f"reader_statistics_{timestamp}.html"

            # Chuẩn bị dữ liệu cho biểu đồ
            total = max(stats.get('total', 1), 1)
            active = stats.get('active', 0)
            expired = stats.get('expired', 0)
            locked = stats.get('locked', 0)

            active_percent = (active / total * 100)
            expired_percent = (expired / total * 100)
            locked_percent = (locked / total * 100)

            # Tạo HTML content
            html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Thống Kê Bạn Đọc</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .timestamp {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        .stat-card.primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .stat-card.success {{
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
        }}

        .stat-card.danger {{
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            color: white;
        }}

        .stat-card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}

        .stat-icon {{
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .stat-label {{
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            opacity: 0.9;
        }}

        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .stat-subtext {{
            font-size: 0.9em;
            margin-top: 10px;
            opacity: 0.85;
        }}

        .charts-section {{
            margin-top: 40px;
        }}

        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #1976D2;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.4em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }}

        canvas {{
            max-height: 400px;
        }}

        .details-section {{
            margin-top: 50px;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
        }}

        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .detail-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #1976D2;
        }}

        .detail-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
        }}

        .detail-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            margin-top: 40px;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}
        }}

        @media (max-width: 768px) {{
            .stats-grid, .charts-grid, .detail-grid {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 BÁO CÁO THỐNG KÊ BẠN ĐỌC</h1>
            <div class="timestamp">
                Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        </div>

        <div class="content">
            <!-- Thống kê tổng quan -->
            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon">👥</div>
                    <div class="stat-label">Tổng Bạn Đọc</div>
                    <div class="stat-value">{stats.get('total', 0)}</div>
                    <div class="stat-subtext">Toàn bộ hệ thống</div>
                </div>

                <div class="stat-card success">
                    <div class="stat-icon">🟢</div>
                    <div class="stat-label">Đang Hoạt Động</div>
                    <div class="stat-value">{active}</div>
                    <div class="stat-subtext">{active_percent:.1f}% tổng số</div>
                </div>

                <div class="stat-card danger">
                    <div class="stat-icon">🔴</div>
                    <div class="stat-label">Hết Hạn</div>
                    <div class="stat-value">{expired}</div>
                    <div class="stat-subtext">{expired_percent:.1f}% tổng số</div>
                </div>

                <div class="stat-card warning">
                    <div class="stat-icon">🔒</div>
                    <div class="stat-label">Bị Khóa</div>
                    <div class="stat-value">{locked}</div>
                    <div class="stat-subtext">{locked_percent:.1f}% tổng số</div>
                </div>
            </div>

            <!-- Biểu đồ -->
            <div class="charts-section">
                <h2 class="section-title">📈 Phân Tích Chi Tiết</h2>

                <div class="charts-grid">
                    <div class="chart-container">
                        <h3 class="chart-title">Phân Bố Trạng Thái</h3>
                        <canvas id="statusChart"></canvas>
                    </div>

                    <div class="chart-container">
                        <h3 class="chart-title">Biểu Đồ Tròn Trạng Thái</h3>
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>

                <div class="charts-grid">
                    <div class="chart-container">
                        <h3 class="chart-title">Phân Loại Uy Tín</h3>
                        <canvas id="reputationChart"></canvas>
                    </div>

                    <div class="chart-container">
                        <h3 class="chart-title">Cảnh Báo Hết Hạn</h3>
                        <canvas id="expiryChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Chi tiết bổ sung -->
            <div class="details-section">
                <h2 class="section-title">📋 Thông Tin Chi Tiết</h2>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">⭐ Điểm Uy Tín Trung Bình</div>
                        <div class="detail-value">{stats.get('avg_reputation', 0):.2f}/100</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">🌟 Bạn Đọc Xuất Sắc (≥90)</div>
                        <div class="detail-value">{stats.get('high_reputation', 0)}</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">❌ Bạn Đọc Uy Tín Thấp (<50)</div>
                        <div class="detail-value">{stats.get('low_reputation', 0)}</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">⏰ Thẻ Sắp Hết Hạn (30 ngày)</div>
                        <div class="detail-value">{stats.get('expiring_soon', 0)}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>© 2025 Library Management System - Báo cáo được tạo tự động</p>
            <p>Phát triển bởi NvkhoaDev54</p>
        </div>
    </div>

    <script>
        // Dữ liệu
        const statusData = {{
            labels: ['Hoạt động', 'Hết hạn', 'Bị khóa'],
            datasets: [{{
                label: 'Số lượng bạn đọc',
                data: [{active}, {expired}, {locked}],
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(244, 67, 54, 0.8)',
                    'rgba(255, 152, 0, 0.8)'
                ],
                borderColor: [
                    'rgba(76, 175, 80, 1)',
                    'rgba(244, 67, 54, 1)',
                    'rgba(255, 152, 0, 1)'
                ],
                borderWidth: 2
            }}]
        }};

        const reputationData = {{
            labels: ['Xuất sắc (≥90)', 'Tốt (75-89)', 'Trung bình (50-74)', 'Kém (<50)'],
            datasets: [{{
                label: 'Số lượng',
                data: [
                    {stats.get('high_reputation', 0)},
                    {stats.get('total', 0) - stats.get('high_reputation', 0) - stats.get('low_reputation', 0)},
                    0,
                    {stats.get('low_reputation', 0)}
                ],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(139, 195, 74, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(244, 67, 54, 0.8)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(139, 195, 74, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(244, 67, 54, 1)'
                ],
                borderWidth: 2
            }}]
        }};

        const expiryData = {{
            labels: ['Còn hạn', 'Sắp hết hạn', 'Đã hết hạn'],
            datasets: [{{
                label: 'Số lượng',
                data: [
                    {active - stats.get('expiring_soon', 0)},
                    {stats.get('expiring_soon', 0)},
                    {expired}
                ],
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(244, 67, 54, 0.8)'
                ],
                borderColor: [
                    'rgba(76, 175, 80, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(244, 67, 54, 1)'
                ],
                borderWidth: 2
            }}]
        }};

        // Cấu hình chung
        const commonOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{
                    position: 'bottom',
                    labels: {{
                        font: {{
                            size: 12,
                            family: "'Segoe UI', sans-serif"
                        }},
                        padding: 15
                    }}
                }},
                tooltip: {{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {{
                        size: 14
                    }},
                    bodyFont: {{
                        size: 13
                    }},
                    padding: 12,
                    cornerRadius: 8
                }}
            }},
            animation: {{
                duration: 1500,
                easing: 'easeInOutQuart'
            }}
        }};

        // Tạo biểu đồ cột
        new Chart(document.getElementById('statusChart'), {{
            type: 'bar',
            data: statusData,
            options: {{
                ...commonOptions,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            font: {{
                                size: 12
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                size: 12
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Tạo biểu đồ tròn
        new Chart(document.getElementById('pieChart'), {{
            type: 'doughnut',
            data: statusData,
            options: {{
                ...commonOptions,
                cutout: '60%'
            }}
        }});

        // Tạo biểu đồ uy tín
        new Chart(document.getElementById('reputationChart'), {{
            type: 'bar',
            data: reputationData,
            options: {{
                ...commonOptions,
                indexAxis: 'y',
                scales: {{
                    x: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // Tạo biểu đồ hết hạn
        new Chart(document.getElementById('expiryChart'), {{
            type: 'pie',
            data: expiryData,
            options: commonOptions
        }});
    </script>
</body>
</html>
"""

            # Ghi file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"✅ Đã tạo báo cáo HTML: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"❌ Lỗi tạo báo cáo HTML: {e}")
            raise

    @staticmethod
    def create_book_statistics_report(stats: Dict) -> str:
        """
        Tạo báo cáo thống kê sách dạng HTML

        Args:
            stats: Dictionary chứa thống kê sách

        Returns:
            str: Đường dẫn đến file HTML đã tạo
        """
        try:
            reports_dir = Path.cwd() / "reports"
            reports_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = reports_dir / f"book_statistics_{timestamp}.html"

            # Chuẩn bị dữ liệu
            total_books = stats.get('total_books', 0)
            total_quantity = stats.get('total_quantity', 0)
            available = stats.get('available_quantity', 0)
            borrowed = stats.get('borrowed_quantity', 0)
            out_of_stock = stats.get('out_of_stock', 0)
            low_stock = stats.get('low_stock', 0)

            html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Thống Kê Sách</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .timestamp {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            color: white;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}

        .stat-card.primary {{
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        }}

        .stat-card.success {{
            background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        }}

        .stat-card.warning {{
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        }}

        .stat-card.danger {{
            background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
        }}

        .stat-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}

        .stat-label {{
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            opacity: 0.9;
        }}

        .stat-value {{
            font-size: 3em;
            font-weight: bold;
        }}

        .stat-subtext {{
            font-size: 0.9em;
            margin-top: 10px;
            opacity: 0.85;
        }}

        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin: 40px 0 25px 0;
            padding-bottom: 15px;
            border-bottom: 3px solid #2196F3;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.4em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }}

        .details-section {{
            margin-top: 50px;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
        }}

        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .detail-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #2196F3;
        }}

        .detail-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
        }}

        .detail-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            margin-top: 40px;
        }}

        @media (max-width: 768px) {{
            .stats-grid, .charts-grid, .detail-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 BÁO CÁO THỐNG KÊ SÁCH</h1>
            <div class="timestamp">
                Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        </div>

        <div class="content">
            <div class="stats-grid">
                <div class="stat-card primary">
                    <div class="stat-icon">📚</div>
                    <div class="stat-label">Tổng Đầu Sách</div>
                    <div class="stat-value">{total_books}</div>
                    <div class="stat-subtext">Trong thư viện</div>
                </div>

                <div class="stat-card success">
                    <div class="stat-icon">📦</div>
                    <div class="stat-label">Tổng Số Lượng</div>
                    <div class="stat-value">{total_quantity}</div>
                    <div class="stat-subtext">Tất cả sách</div>
                </div>

                <div class="stat-card warning">
                    <div class="stat-icon">✅</div>
                    <div class="stat-label">Còn Trong Kho</div>
                    <div class="stat-value">{available}</div>
                    <div class="stat-subtext">{(available / max(total_quantity, 1) * 100):.1f}% tổng số</div>
                </div>

                <div class="stat-card danger">
                    <div class="stat-icon">📤</div>
                    <div class="stat-label">Đang Cho Mượn</div>
                    <div class="stat-value">{borrowed}</div>
                    <div class="stat-subtext">{(borrowed / max(total_quantity, 1) * 100):.1f}% tổng số</div>
                </div>
            </div>

            <h2 class="section-title">📊 Phân Tích Chi Tiết</h2>

            <div class="charts-grid">
                <div class="chart-container">
                    <h3 class="chart-title">Tình Trạng Tồn Kho</h3>
                    <canvas id="stockChart"></canvas>
                </div>

                <div class="chart-container">
                    <h3 class="chart-title">Phân Bố Sách</h3>
                    <canvas id="distributionChart"></canvas>
                </div>
            </div>

            <div class="details-section">
                <h2 class="section-title">📋 Thông Tin Chi Tiết</h2>
                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">❌ Sách Hết Hàng</div>
                        <div class="detail-value">{out_of_stock} đầu</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">⚠️ Sách Sắp Hết</div>
                        <div class="detail-value">{low_stock} đầu</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">👤 Tổng Tác Giả</div>
                        <div class="detail-value">{stats.get('total_authors', 0)}</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">🏷️ Tổng Thể Loại</div>
                        <div class="detail-value">{stats.get('total_categories', 0)}</div>
                    </div>

                    <div class="detail-item">
                        <div class="detail-label">🏭 Tổng NXB</div>
                        <div class="detail-value">{stats.get('total_publishers', 0)}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>© 2025 Library Management System - Báo cáo được tạo tự động</p>
            <p>Phát triển bởi NvkhoaDev54</p>
        </div>
    </div>

    <script>
        const stockData = {{
            labels: ['Còn hàng', 'Sắp hết', 'Hết hàng'],
            datasets: [{{
                label: 'Số đầu sách',
                data: [
                    {total_books - out_of_stock - low_stock},
                    {low_stock},
                    {out_of_stock}
                ],
                backgroundColor: [
                    'rgba(76, 175, 80, 0.8)',
                    'rgba(255, 152, 0, 0.8)',
                    'rgba(244, 67, 54, 0.8)'
                ],
                borderColor: [
                    'rgba(76, 175, 80, 1)',
                    'rgba(255, 152, 0, 1)',
                    'rgba(244, 67, 54, 1)'
                ],
                borderWidth: 2
            }}]
        }};

        const distributionData = {{
            labels: ['Trong kho', 'Đang mượn'],
            datasets: [{{
                label: 'Số lượng sách',
                data: [{available}, {borrowed}],
                backgroundColor: [
                    'rgba(33, 150, 243, 0.8)',
                    'rgba(255, 152, 0, 0.8)'
                ],
                borderColor: [
                    'rgba(33, 150, 243, 1)',
                    'rgba(255, 152, 0, 1)'
                ],
                borderWidth: 2
            }}]
        }};

        const commonOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{
                    position: 'bottom',
                    labels: {{
                        font: {{
                            size: 12,
                            family: "'Segoe UI', sans-serif"
                        }},
                        padding: 15
                    }}
                }}
            }},
            animation: {{
                duration: 1500,
                easing: 'easeInOutQuart'
            }}
        }};

        new Chart(document.getElementById('stockChart'), {{
            type: 'bar',
            data: stockData,
            options: {{
                ...commonOptions,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        new Chart(document.getElementById('distributionChart'), {{
            type: 'doughnut',
            data: distributionData,
            options: {{
                ...commonOptions,
                cutout: '60%'
            }}
        }});
    </script>
</body>
</html>
"""

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"✅ Đã tạo báo cáo sách HTML: {filename}")
            return str(filename)

        except Exception as e:
            logger.error(f"❌ Lỗi tạo báo cáo sách HTML: {e}")
            raise

    @staticmethod
    def open_report_in_browser(filepath: str) -> bool:
        """
        Mở file HTML trong trình duyệt mặc định

        Args:
            filepath: Đường dẫn đến file HTML

        Returns:
            bool: True nếu mở thành công
        """
        try:
            webbrowser.open('file://' + os.path.abspath(filepath))
            logger.info(f"✅ Đã mở báo cáo trong trình duyệt")
            return True
        except Exception as e:
            logger.error(f"❌ Lỗi mở trình duyệt: {e}")
            return False