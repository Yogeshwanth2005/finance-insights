from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    days_late = db.Column(db.Integer, default=0)
    file_upload_id = db.Column(db.Integer, db.ForeignKey('file_uploads.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = db.relationship('Customer', backref=db.backref('payments', lazy=True))
    file_upload = db.relationship('FileUpload', backref=db.backref('payments', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else 'Unknown',
            'amount': self.amount,
            'due_date': self.due_date.isoformat(),
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'status': self.status,
            'days_late': self.days_late,
            'created_at': self.created_at.isoformat()
        }
