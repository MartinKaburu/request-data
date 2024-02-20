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


# Main route
@app.route('/')
def get_reverse_ip():
    # Check if X-FORWARDED-FOR header exists, if it does, the request went through a proxy, nat or lb before getting to
    # the server therefore we should get the origin address from the header.
    if 'X-Forwarded-For' in request.headers:
        # Split the header value by comma and retrieve the first IP address
        client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        # Request went through no proxies and the remote_addr is accurate
        client_ip = request.remote_addr

    client_ip = request.remote_addr
    reversed_ip = '.'.join(reversed(client_ip.split('.')))  # opting to reverse the order of the IP numbers not digits

    # Save original IP, reversed IP, and headers in the database
    headers = json.dumps(dict(request.headers))
    cursor.execute("INSERT INTO req_data (original_ip, reversed_ip, headers) VALUES (?, ?, ?)",
                   (client_ip, reversed_ip, headers))
    conn.commit()

    return reversed_ip


# Extra route to view all requests made to server within it's life span
@app.route('/all_ips', methods=['GET'])
def get_all_ips():
    cursor.execute("SELECT original_ip, reversed_ip, headers FROM req_data")
    result = cursor.fetchall()
    ips = [{'original_ip': row[0], 'reversed_ip': row[1], 'headers': json.loads(row[2])} for row in result]
    return jsonify(ips)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
