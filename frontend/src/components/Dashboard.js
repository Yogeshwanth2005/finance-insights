import React, { useState, useEffect } from 'react';
import { analysisAPI } from '../api';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './Dashboard.css';

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState([]);
  const [behavior, setBehavior] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, trendsRes, behaviorRes, notifRes] = await Promise.all([
        analysisAPI.getSummary(),
        analysisAPI.getTrends(6),
        analysisAPI.getCustomerBehavior(),
        analysisAPI.getNotifications(),
      ]);

      setSummary(summaryRes.data);
      setTrends(trendsRes.data.trends);
      setBehavior(behaviorRes.data.customers);
      setNotifications(notifRes.data.notifications);
    } catch (err) {
      setError('Failed to load dashboard: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!summary) return <div className="empty">No data available</div>;

  return (
    <div className="dashboard">
      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="notifications-section">
          <h3>🔔 Notifications & Insights</h3>
          <div className="notifications-list">
            {notifications.map((notif, idx) => (
              <div key={idx} className={`notification ${notif.severity}`}>
                {notif.message}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Stats */}
      <div className="summary-stats">
        <div className="stat-card">
          <h4>Total Invoices</h4>
          <p className="stat-value">{summary.total_invoices}</p>
          <span className="stat-currency">${summary.total_amount.toFixed(0)}</span>
        </div>
        <div className="stat-card success">
          <h4>Paid</h4>
          <p className="stat-value">{summary.paid_invoices}</p>
          <span className="stat-currency">${summary.paid_amount.toFixed(0)}</span>
        </div>
        <div className="stat-card warning">
          <h4>Overdue</h4>
          <p className="stat-value">{summary.overdue_invoices}</p>
          <span className="stat-currency">${summary.overdue_amount.toFixed(0)}</span>
        </div>
        <div className="stat-card">
          <h4>Collection Rate</h4>
          <p className="stat-value">{summary.collection_rate.toFixed(1)}%</p>
          <span className="stat-subtext">Target: 90%+</span>
        </div>
        <div className="stat-card">
          <h4>Avg Days Late</h4>
          <p className="stat-value">{summary.average_days_late.toFixed(0)}</p>
          <span className="stat-subtext">when overdue</span>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-section">
        <div className="chart-container">
          <h3>📈 Payment Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="total_paid"
                stroke="#51cf66"
                name="Paid"
              />
              <Line
                type="monotone"
                dataKey="total_due"
                stroke="#4dabf7"
                name="Due"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3>📊 Collection Rate Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="collection_rate"
                fill="#b197fc"
                name="Collection Rate (%)"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Customer Behavior */}
      <div className="customers-section">
        <h3>👥 Customer Risk Analysis</h3>
        <div className="customers-table">
          <table>
            <thead>
              <tr>
                <th>Customer</th>
                <th>Transactions</th>
                <th>Late Count</th>
                <th>Late %</th>
                <th>Avg Delay (days)</th>
                <th>Total Amount</th>
                <th>Risk Score</th>
              </tr>
            </thead>
            <tbody>
              {behavior.slice(0, 10).map((customer) => (
                <tr key={customer.customer_id} className={`risk-${Math.ceil(customer.risk_score / 25)}`}>
                  <td>{customer.customer_name}</td>
                  <td>{customer.total_transactions}</td>
                  <td>{customer.late_payment_count}</td>
                  <td>{customer.late_percentage.toFixed(1)}%</td>
                  <td>{customer.average_delay_days.toFixed(0)}</td>
                  <td>${customer.total_amount.toFixed(0)}</td>
                  <td>
                    <span className="risk-badge">
                      {customer.risk_score.toFixed(0)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
