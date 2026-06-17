import duckdb
import os

# Connect to a blazing-fast in-memory DuckDB instance
db = duckdb.connect(database=':memory:')

# Global state to keep track of the currently loaded file
CURRENT_FILE_METADATA = {
    "active_table": None,
    "columns": []
}

def load_file_into_duckdb(file_path):
    """
    Takes a dropped file path, creates a SQL table, and extracts its columns.
    """
    global CURRENT_FILE_METADATA
    
    # Extract the filename without the extension to use as the SQL table name
    file_name = os.path.basename(file_path)
    # Clean the name so SQL doesn't break (replace spaces/hyphens with underscores)
    table_name = os.path.splitext(file_name)[0].replace("-", "_").replace(" ", "_")
    
    try:
        # DuckDB natively reads CSV/JSON/Excel files incredibly fast
        db.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}');")
        
        # Query DuckDB to get the table schema (column names and types)
        schema = db.execute(f"PRAGMA table_info({table_name});").fetchall()
        
        # Extract just the column names (the second item in the schema tuple)
        columns = [col[1] for col in schema]
        
        # Update the global state so the API and Frontend know the file is ready
        CURRENT_FILE_METADATA["active_table"] = table_name
        CURRENT_FILE_METADATA["columns"] = columns
        
        print(f"✅ Successfully ingested table '{table_name}' with columns: {columns}")
    except Exception as e:
        print(f"❌ Error loading file into DuckDB: {str(e)}")

def query_active_table(sql_query):
    """
    Executes a SQL query against the loaded table and returns a dictionary.
    (This is ready for when you want the AI to generate actual data queries!)
    """
    try:
        result = db.execute(sql_query).df() 
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
