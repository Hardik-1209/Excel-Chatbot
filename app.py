import os
import pandas as pd
import sqlite3
import re
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE_PATH = 'database.db'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
DEFAULT_LIMIT = 200

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to clean column names
def clean_column_name(name):
    # Convert to lowercase and replace spaces/special chars with underscores
    cleaned = re.sub(r'[^\w\s]', '', name.lower())
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned

# Helper function to get database schema
def get_db_schema():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    schema = {}
    for table in tables:
        # Get column information
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Get sample data (10 rows)
        cursor.execute(f"SELECT * FROM {table} LIMIT 10;")
        sample_data = cursor.fetchall()
        
        schema[table] = {
            'columns': columns,
            'sample_data': sample_data
        }
    
    conn.close()
    return schema

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Process the file based on extension
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:  # Excel file
                df = pd.read_excel(file_path)
            
            # Clean column names
            df.columns = [clean_column_name(col) for col in df.columns]
            
            # Create SQLite database and store data
            conn = sqlite3.connect(DATABASE_PATH)
            
            # Use the filename (without extension) as the table name
            table_name = os.path.splitext(filename)[0].lower()
            table_name = re.sub(r'[^\w]', '_', table_name)
            
            # Write to SQLite
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'File uploaded and processed successfully. Created table: {table_name}',
                'table_name': table_name,
                'row_count': len(df)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/schema', methods=['GET'])
def get_schema():
    try:
        schema = get_db_schema()
        return jsonify(schema)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query_nl', methods=['POST'])
def query_nl():
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        nl_query = data['query']
        
        # Get database schema for context
        schema = get_db_schema()
        
        # Format schema information for the Groq API
        schema_context = "Database Schema:\n"
        for table, info in schema.items():
            schema_context += f"Table: {table}\n"
            schema_context += f"Columns: {', '.join(info['columns'])}\n\n"
            
            # Add sample data
            schema_context += "Sample data:\n"
            for row in info['sample_data'][:3]:  # Just first 3 rows for brevity
                schema_context += f"{row}\n"
            schema_context += "\n"
        
        # Prepare prompt for Groq API
        prompt = f"""
        You are an expert SQL query generator. Given the following database schema and a natural language query, 
        generate a valid SQL query that answers the question. Always apply a LIMIT of {DEFAULT_LIMIT} unless 
        the user explicitly specifies a different limit.
        
        {schema_context}
        
        Natural language query: "{nl_query}"
        
        Respond with ONLY the SQL query, nothing else.
        """
        
        # Call Groq API
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return jsonify({'error': 'GROQ_API_KEY not found in environment variables'}), 500
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",  # Using currently supported production model
                "messages": [
                    {"role": "system", "content": "You are an expert SQL query generator."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1  # Low temperature for more deterministic output
            }
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'Groq API error: {response.text}'}), 500
        
        # Extract SQL query from Groq response
        sql_query = response.json()['choices'][0]['message']['content'].strip()
        
        # Execute the SQL query
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql_query)
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            # Convert results to list of dictionaries for JSON response
            formatted_results = []
            for row in results:
                formatted_results.append(dict(zip(columns, row)))
            
            conn.close()
            
            return jsonify({
                'sql_query': sql_query,
                'results': formatted_results,
                'count': len(formatted_results)
            })
            
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'error': f'SQL execution error: {str(e)}', 'sql_query': sql_query}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))