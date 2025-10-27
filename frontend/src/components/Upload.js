import React, { useState } from 'react';
import axios from 'axios';
import './Upload.css';
import config from '../config';

function Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    // Check file extension
    const fileExt = file.name.split('.').pop().toLowerCase();
    if (!['csv', 'xlsx', 'xls'].includes(fileExt)) {
      setError('Only CSV and Excel files are supported');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Upload file
      const response = await axios.post(`${config.apiUrl}/upload_excel`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        },
      });

      // Get schema after successful upload
      const schemaResponse = await axios.get(`${config.apiUrl}/schema`);
      
      setIsUploading(false);
      onUploadSuccess(schemaResponse.data, response.data.table_name);
    } catch (err) {
      setIsUploading(false);
      setError(err.response?.data?.error || 'Error uploading file. Please try again.');
      console.error('Upload error:', err);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <h2>Upload Your Data</h2>
        <p>Upload an Excel or CSV file to start analyzing with natural language queries</p>
        
        <form onSubmit={handleSubmit}>
          <div className="file-input-container">
            <input
              type="file"
              id="file"
              onChange={handleFileChange}
              className="file-input"
              accept=".csv,.xlsx,.xls"
            />
            <label htmlFor="file" className="file-label">
              {file ? file.name : 'Choose a file'}
            </label>
          </div>
          
          {file && (
            <div className="file-info">
              <p>File: {file.name}</p>
              <p>Size: {(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          )}
          
          {error && <div className="error-message">{error}</div>}
          
          {isUploading ? (
            <div className="progress-container">
              <div 
                className="progress-bar" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
              <span>{uploadProgress}%</span>
            </div>
          ) : (
            <button type="submit" className="upload-button">
              Upload and Process
            </button>
          )}
        </form>
        
        <div className="upload-info">
          <h3>Supported Files</h3>
          <ul>
            <li>CSV (.csv)</li>
            <li>Excel (.xlsx, .xls)</li>
          </ul>
          <p className="note">Note: Large files (50,000+ rows) may take a moment to process</p>
        </div>
      </div>
    </div>
  );
}

export default Upload;