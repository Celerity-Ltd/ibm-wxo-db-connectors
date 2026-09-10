import json

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.run import connections
import sqlalchemy

APP_ID = "postgresql_db"


@tool(
    name="execute_sql_query",
    display_name="Execute SQL Query",
    description=(
        "Executes a SQL query against the connected PostgreSQL database and returns the results "
        "as a formatted JSON string. Use this tool to run any SELECT (or other) SQL statement "
        "produced from the user's natural language request."
    ),
    expected_credentials=[
        ExpectedCredentials(app_id=APP_ID, type=ConnectionType.KEY_VALUE)
    ],
)
def execute_sql_query(sql_query: str) -> str:
    """Executes a SQL query against the configured PostgreSQL database using SQLAlchemy.

    The database connection details (host, port, database name, username, and password)
    are read securely from the 'postgresql_db' key_value connection.

    Args:
        sql_query (str): A valid SQL query to execute against the PostgreSQL database.

    Returns:
        str: A JSON-formatted string containing the query results as a list of row dicts,
             or an error message if the query fails.
    """
    from sqlalchemy import create_engine, text

    creds = connections.key_value(APP_ID)

    db_host = creds.get("DB_HOST", "localhost")
    db_port = creds.get("DB_PORT", "5432")
    db_name = creds.get("DB_NAME")
    db_user = creds.get("DB_USER")
    db_password = creds.get("DB_PASSWORD")

    if not all([db_name, db_user, db_password]):
        return json.dumps({
            "error": "Missing required connection credentials. Ensure DB_NAME, DB_USER, and DB_PASSWORD are set in the 'postgresql_db' connection."
        })

    connection_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(connection_url)

    with engine.connect() as db_conn:
        result = db_conn.execute(text(sql_query))
        if result.returns_rows:
            columns = list(result.keys())
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            return json.dumps(rows, default=str, indent=2)
        else:
            return json.dumps({"message": "Query executed successfully.", "rowcount": result.rowcount})
