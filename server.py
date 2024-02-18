from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('req_data.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS req_data (id INTEGER PRIMARY KEY, original_ip TEXT, reversed_ip TEXT, headers TEXT)
''')
conn.commit()


@app.route('/')
def get_reverse_ip():
    client_ip = request.remote_addr
    reversed_ip = '.'.join(reversed(client_ip.split('.')))

    # Save original IP, reversed IP, and headers in the database
    headers = json.dumps(dict(request.headers))
    cursor.execute("INSERT INTO req_data (original_ip, reversed_ip, headers) VALUES (?, ?, ?)",
                   (client_ip, reversed_ip, headers))
    conn.commit()

    return reversed_ip


@app.route('/all_ips', methods=['GET'])
def get_all_ips():
    cursor.execute("SELECT original_ip, reversed_ip, headers FROM req_data")
    result = cursor.fetchall()
    ips = [{'original_ip': row[0], 'reversed_ip': row[1], 'headers': json.loads(row[2])} for row in result]
    return jsonify(ips)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)