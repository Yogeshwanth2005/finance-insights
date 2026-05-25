import React, { useState, useCallback } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import LatePayments from './components/LatePayments';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUploadSuccess = (data) => {
    alert(`✅ ${data.message}`);
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1> Finance Insights Dashboard</h1>
          <p>AI-powered payment analytics and insights</p>
        </div>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-btn ${currentPage === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentPage('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={`nav-btn ${currentPage === 'late-payments' ? 'active' : ''}`}
          onClick={() => setCurrentPage('late-payments')}
        >
          Late Payments
        </button>
        <button
          className={`nav-btn ${currentPage === 'upload' ? 'active' : ''}`}
          onClick={() => setCurrentPage('upload')}
        >
          Upload
        </button>
      </nav>

      <main className="app-main">
        {currentPage === 'dashboard' && <Dashboard key={refreshKey} />}
        {currentPage === 'late-payments' && <LatePayments key={refreshKey} />}
        {currentPage === 'upload' && (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        )}
      </main>

      <footer className="app-footer">
        <p>
          © 2024 Finance Insights | Real-time payment analytics for your business
        </p>
      </footer>
    </div>
  );
}

export default App;
