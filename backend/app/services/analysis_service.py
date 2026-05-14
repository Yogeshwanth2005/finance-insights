from datetime import datetime, timedelta
from app.models.payment import Payment
from app.models.customer import Customer
from app import db

class AnalysisService:
    """Analyze payment data and generate insights"""
    
    @staticmethod
    def calculate_days_late(due_date, payment_date):
        """Calculate days late for a payment"""
        if payment_date is None:
            # Still pending - calculate days until today
            delta = datetime.utcnow() - due_date
            return max(0, delta.days)
        
        if payment_date > due_date:
            delta = payment_date - due_date
            return delta.days
        return 0
    
    @staticmethod
    def determine_status(due_date, payment_date):
        """Determine payment status"""
        if payment_date is None:
            if datetime.utcnow() > due_date:
                return 'overdue'
            return 'pending'
        return 'paid'
    
    @staticmethod
    def get_late_payments():
        """Get list of late payments"""
        late_payments = Payment.query.filter(
            Payment.status.in_(['overdue', 'paid'])
        ).filter(Payment.days_late > 0).all()
        
        return [
            {
                'customer_name': p.customer.name,
                'amount': p.amount,
                'due_date': p.due_date.isoformat(),
                'payment_date': p.payment_date.isoformat() if p.payment_date else None,
                'days_late': p.days_late,
                'status': p.status
            }
            for p in late_payments
        ]
    
    @staticmethod
    def get_payment_trends(months=12):
        """Get payment trends over months"""
        now = datetime.utcnow()
        trends = []
        
        for i in range(months, 0, -1):
            target_date = now - timedelta(days=30*i)
            month_key = target_date.strftime('%Y-%m')
            
            # Total amount due this month
            total_due = db.session.query(db.func.sum(Payment.amount)).filter(
                db.func.strftime('%Y-%m', Payment.due_date) == month_key
            ).scalar() or 0
            
            # Total paid this month
            total_paid = db.session.query(db.func.sum(Payment.amount)).filter(
                db.func.strftime('%Y-%m', Payment.payment_date) == month_key,
                Payment.payment_date.isnot(None)
            ).scalar() or 0
            
            # Late payments this month
            late_count = Payment.query.filter(
                db.func.strftime('%Y-%m', Payment.due_date) == month_key,
                Payment.days_late > 0
            ).count()
            
            trends.append({
                'month': month_key,
                'total_due': float(total_due),
                'total_paid': float(total_paid),
                'late_count': late_count,
                'collection_rate': (total_paid / total_due * 100) if total_due > 0 else 0
            })
        
        return trends
    
    @staticmethod
    def get_customer_behavior():
        """Analyze customer payment behavior"""
        customers = Customer.query.all()
        behavior = []
        
        for customer in customers:
            payments = Payment.query.filter_by(customer_id=customer.id).all()
            if not payments:
                continue
            
            late_payments = [p for p in payments if p.days_late > 0]
            avg_delay = sum([p.days_late for p in late_payments]) / len(late_payments) if late_payments else 0
            
            behavior.append({
                'customer_id': customer.id,
                'customer_name': customer.name,
                'total_transactions': len(payments),
                'late_payment_count': len(late_payments),
                'late_percentage': (len(late_payments) / len(payments) * 100) if payments else 0,
                'average_delay_days': avg_delay,
                'total_amount': sum([p.amount for p in payments]),
                'risk_score': customer.risk_score
            })
        
        # Sort by risk score
        behavior.sort(key=lambda x: x['risk_score'], reverse=True)
        return behavior
    
    @staticmethod
    def get_dashboard_summary():
        """Get summary statistics for dashboard"""
        total_invoices = Payment.query.count()
        total_amount = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
        overdue_count = Payment.query.filter(Payment.status == 'overdue').count()
        overdue_amount = db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.status == 'overdue'
        ).scalar() or 0
        
        paid_count = Payment.query.filter(Payment.status == 'paid').count()
        paid_amount = db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.status == 'paid'
        ).scalar() or 0
        
        unique_customers = Customer.query.count()
        avg_days_late = db.session.query(db.func.avg(Payment.days_late)).filter(
            Payment.days_late > 0
        ).scalar() or 0
        
        return {
            'total_invoices': total_invoices,
            'total_amount': float(total_amount),
            'paid_invoices': paid_count,
            'paid_amount': float(paid_amount),
            'overdue_invoices': overdue_count,
            'overdue_amount': float(overdue_amount),
            'pending_invoices': total_invoices - paid_count - overdue_count,
            'unique_customers': unique_customers,
            'average_days_late': float(avg_days_late),
            'collection_rate': (paid_count / total_invoices * 100) if total_invoices > 0 else 0
        }
