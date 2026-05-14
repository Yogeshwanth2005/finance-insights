import React, { useState, useEffect } from 'react';
import { fileAPI } from '../api';
import './FileManagement.css';

function FileManagement() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      setLoading(true);
      const response = await fileAPI.list();
      setFiles(response.data.files);
    } catch (err) {
      setError('Failed to load files: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this file?')) return;

    try {
      await fileAPI.delete(fileId);
      setFiles(files.filter((f) => f.id !== fileId));
      alert('File deleted successfully');
    } catch (err) {
      setError('Failed to delete file: ' + err.message);
    }
  };

  if (loading) return <div className="loading">Loading files...</div>;
  if (error) return <div className="error">{error}</div>;
  if (files.length === 0) return <div className="empty">No files uploaded yet</div>;

  return (
    <div className="file-management">
      <h2>📁 Uploaded Files</h2>
      <div className="files-table">
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Upload Date</th>
              <th>Records</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>{file.filename}</td>
                <td>{new Date(file.upload_date).toLocaleDateString()}</td>
                <td>{file.record_count}</td>
                <td>
                  <span className={`status-badge ${file.status}`}>
                    {file.status}
                  </span>
                </td>
                <td>
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(file.id)}
                  >
                    🗑️ Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default FileManagement;
