# NL to SQL Chatbot

A full-stack application that allows users to upload Excel/CSV files and query the data using natural language, powered by the Groq API.

## Features

- **File Upload**: Support for Excel (.xlsx, .xls) and CSV files with 50,000+ rows
- **Natural Language Queries**: Convert natural language to SQL using Groq API
- **Interactive UI**: Modern React frontend with file upload and chat interface
- **Efficient Data Processing**: SQLite database with clean column naming
- **Pagination**: View large result sets with built-in pagination

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (with easy switch to PostgreSQL)
- **Frontend**: React (JavaScript)
- **NLP Layer**: Groq API (for NL → SQL conversion)

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 14+
- Groq API key

### Backend Setup

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
6. Run the Flask server:
   ```
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory
2. Install dependencies:
   ```
   npm install
   ```
3. Create a `.env` file:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```
4. Start the development server:
   ```
   npm start
   ```

## Usage

1. Open the application in your browser
2. Upload an Excel or CSV file
3. Once processed, enter natural language queries in the chat interface
4. View the generated SQL and results

## Sample Workflow

1. Upload the sample Excel file
2. Ask: "Show me all products with price > 500"
3. View the SQL query and results

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on deploying to Render (backend) and Vercel (frontend).

## Security Considerations

- SQL injection protection through parameterized queries
- Environment variables for sensitive information
- Input validation for file uploads

## License

MIT