import pyodbc

def create_table():
    conn = None
    try:
        # Connect to your Azure SQL Database
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=testf.database.windows.net;'
            'DATABASE=TESTF;'
            'UID=FUSOADMIN;'
            'PWD=eMobility@19'
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Check if the table already exists and create it if it does not
        cur.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'items' AND type = 'U')
            BEGIN
                CREATE TABLE items (id INT PRIMARY KEY IDENTITY(1,1), content NVARCHAR(MAX));
            END
        """)

        # Commit changes
        conn.commit()

        # Close cursor
        cur.close()

        print("Table created successfully")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_table()
