import React, { useState } from 'react';
import axios from 'axios';
import './Chat.css';
import config from '../config';

function Chat({ schema, tableName }) {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [sqlQuery, setSqlQuery] = useState('');
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [history, setHistory] = useState([]);
  const rowsPerPage = 50;

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${config.apiUrl}/query_nl`, {
        query: query
      });
      
      setSqlQuery(response.data.sql_query);
      setResults(response.data.results);
      setCurrentPage(1);
      
      // Add to history
      setHistory([
        { 
          query, 
          sql: response.data.sql_query,
          timestamp: new Date().toLocaleTimeString()
        },
        ...history
      ]);
      
      setIsLoading(false);
    } catch (err) {
      setIsLoading(false);
      setError(err.response?.data?.error || 'Error processing query. Please try again.');
      console.error('Query error:', err);
    }
  };

  // Get column headers from results
  const getHeaders = () => {
    if (results.length === 0) return [];
    return Object.keys(results[0]);
  };

  // Pagination logic
  const totalPages = Math.ceil(results.length / rowsPerPage);
  const paginatedResults = results.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  return (
    <div className="chat-container">
      <div className="schema-info">
        <h3>Table: {tableName}</h3>
        <div className="schema-details">
          <p>Columns: {schema && schema[tableName] ? schema[tableName].columns.join(', ') : 'Loading...'}</p>
        </div>
      </div>

      <div className="query-section">
        <form onSubmit={handleSubmit}>
          <div className="query-input-container">
            <input
              type="text"
              value={query}
              onChange={handleQueryChange}
              placeholder="Ask a question about your data (e.g., 'Show me all products with price > 500')"
              className="query-input"
            />
            <button type="submit" className="query-button" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Ask'}
            </button>
          </div>
        </form>
        
        {error && <div className="error-message">{error}</div>}
      </div>

      {sqlQuery && (
        <div className="sql-section">
          <h3>Generated SQL</h3>
          <pre className="sql-code">{sqlQuery}</pre>
        </div>
      )}

      {results.length > 0 && (
        <div className="results-section">
          <h3>Results ({results.length} rows)</h3>
          
          <div className="table-container">
            <table className="results-table">
              <thead>
                <tr>
                  {getHeaders().map((header, index) => (
                    <th key={index}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {paginatedResults.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {getHeaders().map((header, colIndex) => (
                      <td key={colIndex}>{row[header]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {totalPages > 1 && (
            <div className="pagination">
              <button 
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span>Page {currentPage} of {totalPages}</span>
              <button 
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
              >
                Next
              </button>
            </div>
          )}
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section">
          <h3>Query History</h3>
          <ul className="history-list">
            {history.map((item, index) => (
              <li key={index} className="history-item">
                <div className="history-time">{item.timestamp}</div>
                <div className="history-query">{item.query}</div>
                <button 
                  className="history-rerun"
                  onClick={() => {
                    setQuery(item.query);
                    handleSubmit(new Event('submit'));
                  }}
                >
                  Rerun
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Chat;