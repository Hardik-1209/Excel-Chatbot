import os
import sqlite3
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_and_execute_sql(user_query, cursor):
    """
    Convert user query -> SQL using Groq -> execute on SQLite DB.
    Returns (rows, columns, error).
    """

    try:
        # Step 1: Ask Groq to generate SQL query
        prompt = f"""
        You are an expert in SQL. 
        Convert the following natural language request into a valid **SQLite** SQL query. 
        The table is named 'sales'. 
        Do not explain, only return the SQL query.

        Request: {user_query}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Using currently supported Groq model       
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # deterministic output
        )

        sql_query = response.choices[0].message.content.strip()

        # Cleanup: remove code block wrappers if present
        if sql_query.startswith("```"):
            sql_query = sql_query.strip("`").replace("sql", "").strip()

        print(f"[Generated SQL]: {sql_query}")

        # Step 2: Execute SQL on DB
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        return rows, columns, None

    except Exception as e:
        print(f"[SQL Error] {e}")
        return None, None, str(e)
