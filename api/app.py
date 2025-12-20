"""
Flask API Server cho Library Management System
Chạy: python api/app.py
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import logging

# Thêm thư mục gốc vào path để import được services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_forecast_service import AIForecastService
from config.database import db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Cho phép CORS để web có thể gọi API

# Khởi tạo services
forecast_service = AIForecastService()


# ========== HEALTH CHECK ==========

@app.route('/', methods=['GET'])
def home():
    """API Home - Health check"""
    return jsonify({
        'status': 'running',
        'message': 'Library Management API v1.0',
        'endpoints': {
            'forecast': '/api/ai/forecast',
            'statistics': '/api/statistics',
            'health': '/api/health'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái API và Database"""
    try:
        # Test database connection
        db_status = db.test_connection()

        return jsonify({
            'status': 'healthy',
            'database': 'connected' if db_status else 'disconnected',
            'services': {
                'ai_forecast': 'active',
                'database': 'active' if db_status else 'inactive'
            }
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# ========== AI FORECAST ENDPOINTS ==========

@app.route('/api/ai/forecast', methods=['GET'])
def get_forecast():
    """
    Lấy dữ liệu dự đoán AI

    Query Parameters:
        - history_months: Số tháng lịch sử (default: 12)
        - forecast_months: Số tháng dự đoán (default: 6)

    Example: /api/ai/forecast?history_months=12&forecast_months=6
    """
    try:
        # Lấy parameters
        history_months = int(request.args.get('history_months', 12))
        forecast_months = int(request.args.get('forecast_months', 6))

        # Validate
        if history_months < 3 or history_months > 24:
            return jsonify({
                'success': False,
                'error': 'history_months phải từ 3 đến 24'
            }), 400

        if forecast_months < 1 or forecast_months > 12:
            return jsonify({
                'success': False,
                'error': 'forecast_months phải từ 1 đến 12'
            }), 400

        # Lấy dữ liệu
        logger.info(f"📊 Forecast request: history={history_months}, forecast={forecast_months}")
        result = forecast_service.get_forecast_data(history_months, forecast_months)

        if result['success']:
            logger.info(f"✅ Forecast successful: "
                        f"{len(result['historical'])} historical, "
                        f"{len(result['forecast'])} forecast")
            return jsonify(result), 200
        else:
            logger.warning(f"⚠️ Forecast failed: {result.get('message')}")
            return jsonify(result), 404

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameters'
        }), 400
    except Exception as e:
        logger.error(f"❌ Forecast error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/forecast/borrowing', methods=['GET'])
def get_borrowing_forecast():
    """Dự đoán riêng cho lượt mượn sách"""
    try:
        months = int(request.args.get('months', 6))

        # Lấy dữ liệu lịch sử
        historical = forecast_service.get_borrowing_history(12)
        combined = forecast_service.get_combined_history(12)

        # Tạo dự đoán
        forecast = forecast_service.generate_forecast(combined, months)

        return jsonify({
            'success': True,
            'metric': 'borrowing',
            'historical': historical.to_dict('records'),
            'forecast': forecast[['month_display', 'borrowing_count', 'confidence']].to_dict('records')
        }), 200

    except Exception as e:
        logger.error(f"❌ Borrowing forecast error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/forecast/revenue', methods=['GET'])
def get_revenue_forecast():
    """Dự đoán riêng cho doanh thu"""
    try:
        months = int(request.args.get('months', 6))

        # Lấy dữ liệu lịch sử
        historical = forecast_service.get_revenue_history(12)
        combined = forecast_service.get_combined_history(12)

        # Tạo dự đoán
        forecast = forecast_service.generate_forecast(combined, months)

        return jsonify({
            'success': True,
            'metric': 'revenue',
            'historical': historical.to_dict('records'),
            'forecast': forecast[['month_display', 'revenue', 'confidence']].to_dict('records')
        }), 200

    except Exception as e:
        logger.error(f"❌ Revenue forecast error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai/forecast/users', methods=['GET'])
def get_users_forecast():
    """Dự đoán riêng cho bạn đọc mới"""
    try:
        months = int(request.args.get('months', 6))

        # Lấy dữ liệu lịch sử
        historical = forecast_service.get_new_users_history(12)
        combined = forecast_service.get_combined_history(12)

        # Tạo dự đoán
        forecast = forecast_service.generate_forecast(combined, months)

        return jsonify({
            'success': True,
            'metric': 'new_users',
            'historical': historical.to_dict('records'),
            'forecast': forecast[['month_display', 'new_users', 'confidence']].to_dict('records')
        }), 200

    except Exception as e:
        logger.error(f"❌ Users forecast error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========== STATISTICS ENDPOINTS ==========

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Lấy thống kê tổng quan"""
    try:
        # Lấy dữ liệu 12 tháng gần nhất
        combined = forecast_service.get_combined_history(12)

        if len(combined) == 0:
            return jsonify({
                'success': False,
                'message': 'Không có dữ liệu'
            }), 404

        stats = forecast_service._calculate_statistics(combined)

        return jsonify({
            'success': True,
            'statistics': stats
        }), 200

    except Exception as e:
        logger.error(f"❌ Statistics error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ========== MAIN ==========

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🚀 Starting Flask API Server")
    logger.info("=" * 50)

    # Test database connection
    if db.test_connection():
        logger.info("✅ Database connected successfully")
    else:
        logger.error("❌ Database connection failed!")

    # Run server
    app.run(
        host='0.0.0.0',  # Cho phép truy cập từ mọi IP
        port=5000,  # Port 5000
        debug=True  # Debug mode
    )

    logger.info("Server is running on http://localhost:5000")