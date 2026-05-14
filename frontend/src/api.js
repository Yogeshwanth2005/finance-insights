import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// File endpoints
export const fileAPI = {
  upload: (file, columnMapping = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (columnMapping) {
      formData.append('columnMapping', JSON.stringify(columnMapping));
    }
    return apiClient.post('/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  list: () => apiClient.get('/files/list'),
  delete: (fileId) => apiClient.delete(`/files/${fileId}`),
  preview: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/files/preview', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Analysis endpoints
export const analysisAPI = {
  getLatePayments: () => apiClient.get('/analysis/late-payments'),
  getTrends: (months = 12) => apiClient.get(`/analysis/trends?months=${months}`),
  getCustomerBehavior: () => apiClient.get('/analysis/customer-behavior'),
  getSummary: () => apiClient.get('/analysis/summary'),
  getNotifications: () => apiClient.get('/analysis/notifications'),
};

// Dashboard endpoints
export const dashboardAPI = {
  getStats: () => apiClient.get('/dashboard/stats'),
  exportReport: () => apiClient.get('/dashboard/export'),
};
