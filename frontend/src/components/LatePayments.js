import React, { useState, useEffect } from 'react';
import { analysisAPI } from '../api';
import './LatePayments.css';

function LatePayments() {
  const [latePayments, setLatePayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLatePayments();
  }, []);

  const fetchLatePayments = async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.getLatePayments();
      setLatePayments(response.data.late_payments);
    } catch (err) {
      setError('Failed to load late payments: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading late payments...</div>;
  if (error) return <div className="error">{error}</div>;
  if (latePayments.length === 0)
    return <div className="empty">No late payments found! 🎉</div>;

  return (
    <div className="late-payments-container">
      <h2>⏰ Late Payments</h2>
      <div className="payments-list">
        {latePayments.map((payment, idx) => (
          <div key={idx} className="payment-card">
            <div className="payment-header">
              <h3>{payment.customer_name}</h3>
              <span className={`status ${payment.status}`}>{payment.status}</span>
            </div>
            <div className="payment-details">
              <div className="detail">
                <span className="label">Amount:</span>
                <span className="value">${payment.amount.toFixed(2)}</span>
              </div>
              <div className="detail">
                <span className="label">Days Late:</span>
                <span className="value days-late">{payment.days_late} days</span>
              </div>
              <div className="detail">
                <span className="label">Due Date:</span>
                <span className="value">
                  {new Date(payment.due_date).toLocaleDateString()}
                </span>
              </div>
              {payment.payment_date && (
                <div className="detail">
                  <span className="label">Paid Date:</span>
                  <span className="value">
                    {new Date(payment.payment_date).toLocaleDateString()}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LatePayments;
