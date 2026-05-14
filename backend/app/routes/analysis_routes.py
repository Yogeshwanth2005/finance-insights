from flask import Blueprint, request, jsonify
from app.services.analysis_service import AnalysisService
from app.services.notification_service import NotificationService

bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

@bp.route('/late-payments', methods=['GET'])
def get_late_payments():
    """Get late payment list"""
    try:
        late_payments = AnalysisService.get_late_payments()
        return jsonify({
            'late_payments': late_payments,
            'count': len(late_payments)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/trends', methods=['GET'])
def get_trends():
    """Get payment trends"""
    try:
        months = request.args.get('months', 12, type=int)
        trends = AnalysisService.get_payment_trends(months=months)
        return jsonify({'trends': trends}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/customer-behavior', methods=['GET'])
def get_customer_behavior():
    """Get customer behavior analysis"""
    try:
        behavior = AnalysisService.get_customer_behavior()
        return jsonify({
            'customers': behavior,
            'count': len(behavior)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/summary', methods=['GET'])
def get_summary():
    """Get dashboard summary"""
    try:
        summary = AnalysisService.get_dashboard_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Get notifications and insights"""
    try:
        notifications = NotificationService.generate_notifications()
        insights = NotificationService.generate_summary_text()
        
        return jsonify({
            'notifications': notifications,
            'insights': insights
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
