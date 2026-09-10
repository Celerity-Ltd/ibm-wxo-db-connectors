import json
from typing import cast

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType, ExpectedCredentials
from ibm_watsonx_orchestrate.run import connections
from mapepire_python.data_types import DaemonServer, QueryResult

APP_ID = "ibmi_db2"


@tool(
    name="execute_db2_sql_query",
    display_name="Execute DB2 SQL Query",
    description=(
        "Executes a SQL query against the connected IBM DB2 database using Mapepire and returns "
        "the results as a formatted JSON string. Use this tool to run any SELECT (or other) SQL "
        "statement produced from the user's natural language request."
    ),
    expected_credentials=[
        ExpectedCredentials(app_id=APP_ID, type=ConnectionType.KEY_VALUE)
    ],
)
def execute_db2_sql_query(sql_query: str) -> str:
    """Executes a SQL query against the configured IBM DB2 database using Mapepire.

    The database connection details (host, port, username, and password) are read
    securely from the 'db2_db' key_value connection.

    Args:
        sql_query (str): A valid SQL query to execute against the IBM DB2 database.

    Returns:
        str: A JSON-formatted string containing the query results as a list of row dicts,
             or an error message if the query fails.
    """
    from mapepire_python.client.sql_job import SQLJob

    creds = connections.key_value(APP_ID)

    db_host = creds.get("DB_HOST")
    db_port = creds.get("DB_PORT", "8076")
    db_user = creds.get("DB_USER")
    db_password = creds.get("DB_PASSWORD")

    if not all([db_host, db_user, db_password]):
        return json.dumps({
            "error": (
                "Missing required connection credentials. Ensure DB_HOST, DB_USER, and "
                "DB_PASSWORD are set in the 'db2_db' connection."
            )
        })

    assert db_host is not None
    assert db_user is not None
    assert db_password is not None

    server = DaemonServer(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        ignoreUnauthorized=True,
    )
    job = SQLJob()
    job.connect(server)

    try:
        result = cast(QueryResult, job.query_and_run(sql_query, rows_to_fetch=100))

        if not result.success:
            return json.dumps({
                "error": result.error or "Query failed with no further details."
            })

        columns = [col.name for col in (result.metadata.columns if result.metadata else [])]
        raw_data = result.data or []

        # Mapepire may return rows already as dicts (keyed by column name) or as
        # positional tuples/lists. Only zip when the rows are positional.
        if columns and raw_data and not isinstance(raw_data[0], dict):
            rows = [dict(zip(columns, row)) for row in raw_data]
        else:
            rows = raw_data

        return json.dumps(rows, default=str, indent=2)
    finally:
        job.close()
