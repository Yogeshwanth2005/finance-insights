from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    total_transactions = db.Column(db.Integer, default=0)
    late_payment_count = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Float, default=0.0)
    risk_score = db.Column(db.Float, default=0.0)  # 0-100 score based on late payments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_risk_score(self):
        """Calculate risk score based on late payment frequency and amounts"""
        if self.total_transactions == 0:
            self.risk_score = 0
        else:
            late_ratio = self.late_payment_count / self.total_transactions
            self.risk_score = min(100, late_ratio * 100)  # 0-100
        return self.risk_score
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'total_transactions': self.total_transactions,
            'late_payment_count': self.late_payment_count,
            'total_amount': self.total_amount,
            'risk_score': self.risk_score,
            'created_at': self.created_at.isoformat()
        }
