import React, { useState } from 'react';
import './App.css';
import Upload from './components/Upload';
import Chat from './components/Chat';

function App() {
  const [isFileUploaded, setIsFileUploaded] = useState(false);
  const [schema, setSchema] = useState(null);
  const [tableName, setTableName] = useState('');

  const handleFileUploadSuccess = (uploadedSchema, uploadedTableName) => {
    setIsFileUploaded(true);
    setSchema(uploadedSchema);
    setTableName(uploadedTableName);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>NL to SQL Chatbot</h1>
        <p>Upload an Excel/CSV file and ask questions in natural language</p>
      </header>
      <main>
        {!isFileUploaded ? (
          <Upload onUploadSuccess={handleFileUploadSuccess} />
        ) : (
          <Chat schema={schema} tableName={tableName} />
        )}
      </main>
      <footer>
        <p>Powered by Groq API</p>
      </footer>
    </div>
  );
}

export default App;