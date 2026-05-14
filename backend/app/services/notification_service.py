from app.models.payment import Payment
from app.models.customer import Customer
from app import db

class NotificationService:
    """Generate notifications and insights"""
    
    @staticmethod
    def generate_notifications():
        """Generate all notifications"""
        notifications = []
        
        # Frequent late payers
        late_payers = Customer.query.filter(Customer.late_payment_count > 2).all()
        for customer in late_payers:
            notifications.append({
                'type': 'warning',
                'message': f"⚠️ {customer.name} has {customer.late_payment_count} late payments",
                'severity': 'high' if customer.late_payment_count > 5 else 'medium'
            })
        
        # High-value overdue invoices
        high_value_overdue = Payment.query.filter(
            Payment.status == 'overdue',
            Payment.amount > (
                db.session.query(db.func.avg(Payment.amount)).scalar() or 1000
            )
        ).all()
        
        for payment in high_value_overdue[:5]:  # Show top 5
            notifications.append({
                'type': 'alert',
                'message': f"🚨 High-value overdue invoice from {payment.customer.name}: ${payment.amount:,.2f}",
                'severity': 'critical'
            })
        
        return notifications
    
    @staticmethod
    def generate_summary_text():
        """Generate auto-summary insights"""
        from app.services.analysis_service import AnalysisService
        
        summary = AnalysisService.get_dashboard_summary()
        trends = AnalysisService.get_payment_trends(months=2)
        
        insights = []
        
        # Revenue trend
        if len(trends) >= 2:
            current_month = trends[-1]['total_paid']
            previous_month = trends[-2]['total_paid']
            if previous_month > 0:
                change = ((current_month - previous_month) / previous_month) * 100
                if abs(change) > 5:
                    direction = "increased" if change > 0 else "decreased"
                    insights.append(f"💰 Revenue {direction} by {abs(change):.1f}% this month")
        
        # Late payment trend
        if len(trends) >= 2:
            current_late = trends[-1]['late_count']
            previous_late = trends[-2]['late_count']
            if current_late > previous_late:
                insights.append(f"📈 Late payments increased from {previous_late} to {current_late}")
        
        # Overall collection rate
        collection_rate = summary['collection_rate']
        if collection_rate < 80:
            insights.append(f"⚠️ Collection rate is {collection_rate:.1f}% (target: 90%+)")
        
        return insights
