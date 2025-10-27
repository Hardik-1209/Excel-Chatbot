// Configuration settings for the application
const config = {
  // API endpoint URL - adjust based on environment
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // Other configuration settings can be added here
  defaultTimeout: 30000,
  maxUploadSize: 10 * 1024 * 1024, // 10MB
};

export default config;