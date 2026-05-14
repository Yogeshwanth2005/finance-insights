from flask import Blueprint, jsonify
from app.services.analysis_service import AnalysisService

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get all dashboard statistics"""
    try:
        summary = AnalysisService.get_dashboard_summary()
        trends = AnalysisService.get_payment_trends(months=6)
        customer_behavior = AnalysisService.get_customer_behavior()
        
        # Get top customers and late payers
        high_value = sorted(customer_behavior, key=lambda x: x['total_amount'], reverse=True)[:5]
        high_risk = [c for c in customer_behavior if c['risk_score'] > 50][:5]
        
        return jsonify({
            'summary': summary,
            'trends': trends,
            'top_customers': high_value,
            'high_risk_customers': high_risk,
            'all_customers': customer_behavior
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/export', methods=['GET'])
def export_report():
    """Export report as JSON"""
    try:
        from flask import send_file
        import json
        from datetime import datetime
        
        summary = AnalysisService.get_dashboard_summary()
        trends = AnalysisService.get_payment_trends(months=12)
        customer_behavior = AnalysisService.get_customer_behavior()
        late_payments = AnalysisService.get_late_payments()
        
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'summary': summary,
            'trends': trends,
            'customer_behavior': customer_behavior,
            'late_payments': late_payments
        }
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
