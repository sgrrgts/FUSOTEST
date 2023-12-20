from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=testf.database.windows.net;'
        'DATABASE=TESTF;'
        'UID=FUSOADMIN;'
        'PWD=eMobility@19'
    )
    return conn

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Write operation
        if request.method == 'POST':
            new_item = request.form['content']
            cursor.execute('INSERT INTO items (content) VALUES (?);', new_item)
            conn.commit()

        # Read operation
        cursor.execute('SELECT * FROM items;')
        items = cursor.fetchall()
        return render_template('index.html', items=items)

    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Delete operation
@app.route('/delete/<int:id>')
def delete(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?;', id)
        conn.commit()
        return redirect('/')

    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
