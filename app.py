from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host='your_host',
        dbname='your_dbname',
        user='your_username',
        password='your_password')
    return conn

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Write operation
    if request.method == 'POST':
        new_item = request.form['content']
        cursor.execute('INSERT INTO your_table (content) VALUES (%s)',
                       (new_item,))
        conn.commit()

    # Read operation
    cursor.execute('SELECT * FROM your_table')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

# Delete operation
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM your_table WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
