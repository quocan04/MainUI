"""
Enhanced Flask API với AI Insights
Thêm vào file api/app.py (hoặc tạo mới)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import service mới
from services.ai_forecast_service import EnhancedAIForecastService
from config.database import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Khởi tạo service
ai_service = EnhancedAIForecastService()


# ========== EXISTING ENDPOINTS (giữ nguyên) ==========

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'message': 'Enhanced Library AI API v2.0',
        'endpoints': {
            'legacy': {
                'forecast': '/api/ai/forecast',
                'health': '/api/health'
            },
            'new_insights': {
                'categories': '/api/ai/insights/categories',
                'authors': '/api/ai/insights/authors',
                'publishers': '/api/ai/insights/publishers',
                'book_age': '/api/ai/insights/book-age',
                'comprehensive': '/api/ai/insights/comprehensive'
            },
            'smart_forecast': '/api/ai/forecast-smart'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db_status = db.test_connection()
        return jsonify({
            'status': 'healthy',
            'database': 'connected' if db_status else 'disconnected',
            'ai_model': 'Multi-Factor Linear Model v2.0'
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


# ========== NEW AI INSIGHTS ENDPOINTS ==========

@app.route('/api/ai/insights/categories', methods=['GET'])
def get_category_insights():
    """
    📊 Phân tích xu hướng theo thể loại sách

    Trả về:
    - Thể loại hot/trending/cold
    - Số lượt mượn từng thể loại
    - Popularity score
    - Recommendations
    """
    try:
        result = ai_service.analyze_category_trends()

        if result['success']:
            logger.info(f"✅ Category analysis: {len(result.get('categories', []))} categories")
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"❌ Category insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ai/insights/authors', methods=['GET'])
def get_author_insights():
    """
    ✍️ Phân tích tác giả phổ biến

    Trả về:
    - Top 10 tác giả được mượn nhiều nhất
    - Popularity score
    - Recent activity
    - Trending authors
    """
    try:
        limit = int(request.args.get('limit', 10))
        result = ai_service.analyze_author_popularity()

        if result['success']:
            # Limit results
            result['top_authors'] = result['top_authors'][:limit]
            logger.info(f"✅ Author analysis: {len(result['top_authors'])} authors")
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"❌ Author insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ai/insights/publishers', methods=['GET'])
def get_publisher_insights():
    """
    🏢 Phân tích hiệu suất nhà xuất bản

    Trả về:
    - Top NXB theo số lượt mượn
    - Performance score
    - Sách mới gần đây
    - Recommendations
    """
    try:
        result = ai_service.analyze_publisher_performance()

        if result['success']:
            logger.info(f"✅ Publisher analysis: {len(result.get('publishers', []))} publishers")
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"❌ Publisher insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ai/insights/book-age', methods=['GET'])
def get_book_age_insights():
    """
    📅 Phân tích ảnh hưởng năm xuất bản

    Trả về:
    - Phân nhóm theo tuổi sách
    - Lượt mượn theo năm XB
    - Insights về xu hướng sách mới vs sách cũ
    """
    try:
        result = ai_service.analyze_book_age_impact()

        if result['success']:
            logger.info("✅ Book age analysis completed")
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"❌ Book age insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ai/insights/comprehensive', methods=['GET'])
def get_comprehensive_insights():
    """
    🎯 Lấy TẤT CẢ insights trong 1 request

    Bao gồm:
    - Category analysis
    - Author popularity
    - Publisher performance
    - Book age impact
    - Smart forecast
    """
    try:
        logger.info("📊 Generating comprehensive AI insights...")
        result = ai_service.get_comprehensive_insights()

        if result['success']:
            logger.info("✅ Comprehensive insights generated successfully")
            return jsonify(result), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"❌ Comprehensive insights error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ai/forecast-smart', methods=['GET'])
def get_smart_forecast():
    """
    🔮 Dự đoán thông minh dựa trên nhiều yếu tố

    Query params:
    - months: Số tháng dự đoán (default: 6, max: 12)

    Factors:
    - Historical trend
    - Seasonality (theo lịch học)
    - Hot categories boost
    - Author & Publisher performance
    """
    try:
        months = int(request.args.get('months', 6))

        if months < 1 or months > 12:
            return jsonify({
                'success': False,
                'error': 'months phải từ 1 đến 12'
            }), 400

        logger.info(f"🔮 Generating smart forecast for {months} months...")
        result = ai_service.generate_smart_forecast(months)

        if result['success']:
            logger.info(f"✅ Smart forecast: {len(result['forecast'])} months predicted")
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid parameters'
        }), 400
    except Exception as e:
        logger.error(f"❌ Smart forecast error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ========== MAIN ==========

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 Starting Enhanced AI API Server v2.0")
    logger.info("=" * 60)

    if db.test_connection():
        logger.info("✅ Database connected")
    else:
        logger.error("❌ Database connection failed!")

    logger.info("\n📊 Available AI Endpoints:")
    logger.info("  - /api/ai/insights/categories")
    logger.info("  - /api/ai/insights/authors")
    logger.info("  - /api/ai/insights/publishers")
    logger.info("  - /api/ai/insights/book-age")
    logger.info("  - /api/ai/insights/comprehensive")
    logger.info("  - /api/ai/forecast-smart")
    logger.info("")

    app.run(host='0.0.0.0', port=5000, debug=True)


# ========== CÁCH SỬ DỤNG ==========
"""
1. Thay thế nội dung file api/app.py bằng code này

2. Chạy server:
   python api/app.py

3. Test các endpoint:

   # Phân tích thể loại
   curl http://localhost:5000/api/ai/insights/categories

   # Top tác giả
   curl http://localhost:5000/api/ai/insights/authors?limit=5

   # Top NXB
   curl http://localhost:5000/api/ai/insights/publishers

   # Phân tích theo năm XB
   curl http://localhost:5000/api/ai/insights/book-age

   # Tất cả insights
   curl http://localhost:5000/api/ai/insights/comprehensive

   # Dự đoán thông minh
   curl http://localhost:5000/api/ai/forecast-smart?months=6

4. Kết quả sẽ là JSON với insights chi tiết về:
   - Thể loại hot/trending/cold
   - Tác giả được yêu thích
   - NXB hiệu quả
   - Ảnh hưởng tuổi sách
   - Dự đoán dựa trên nhiều factors
"""