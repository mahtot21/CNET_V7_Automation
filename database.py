import pyodbc


def find_schema(table_name: str, server_name: str = 'DESKTOP-9GKJ3L7\CNET_V7', database_name: str = 'CNET_V7_DB', username: str = 'sa', password: str = 'rdpass') -> str:
    """
    Returns the schema of the specified table if it exists, or -1 if it does not.

    Args:
    table_name (str): The name of the table to retrieve the schema for.
    server_name (str): The name of the server where the SQL Server instance is running. Defaults to 'DESKTOP-9GKJ3L7\CNET_V7'.
    database_name (str): The name of the SQL Server database to connect to. Defaults to 'test_v7'.
    username (str): The username to use for SQL Server authentication. Defaults to 'sa'.
    password (str): The password to use for SQL Server authentication. Defaults to 'rdpass'.

    Returns:
    str: The schema of the table as a string, or -1 if the table does not exist.
    """

    # for tables range and delegate the table have 's' at the end so we should return like this for the cnetmedium for unknowingly entity framework scaffold like this
    if table_name.lower() in ['cnetmedium', 'range', 'delegate']:
        return 'Common'
    if table_name.lower() in ['roomfeature', 'vouchervalue', 'ratecodepackage', 'weekday']:
        table_name = f'{table_name}s'
    if table_name.lower() in ['medium']:
        table_name = 'Media'
    if table_name.lower() in ['registratordetail']:
        return 'Pms'
    if 'Vw' in table_name:
        return 'View'

    # Set up connection string
    connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # check if the table exists
    query = f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
    cursor.execute(query)

    if cursor.fetchone():
        # table exists, retrieve schema
        query = f"SELECT TABLE_SCHEMA FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
        cursor.execute(query)
        schema = cursor.fetchone()[0]
        conn.close()
        return schema.title()
    else:
        # table does not exist
        conn.close()
        return -1
