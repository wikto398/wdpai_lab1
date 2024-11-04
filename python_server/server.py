import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import psycopg2
import os
import time

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)
        
def select_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, role FROM users")
        conn.commit()
        data = []
        for row in cursor:
            data.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "role": row[3]
            })
        return data 
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return []

def insert_user(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, role) VALUES (%s, %s, %s)",
                    (user["first_name"], user["last_name"], user["role"]))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()

def delete_user(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()

# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):

    # Handle OPTIONS requests (used in CORS preflight checks).
    # CORS (Cross-Origin Resource Sharing) is a mechanism that allows restricted resources
    # on a web page to be requested from another domain outside the domain from which the resource originated.
    def do_OPTIONS(self):
        # Send a 200 OK response to acknowledge the request was processed successfully.
        self.send_response(200, "OK")

        # Set headers to indicate that this server allows any origin (*) to access its resources.
        # This is important for browsers when making cross-origin requests.
        self.send_header("Access-Control-Allow-Origin", "*")

        # Specify the allowed HTTP methods that can be used in the actual request.
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        # Indicate what request headers are allowed (e.g., Content-Type for JSON requests).
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # End headers and complete the response
        self.end_headers()

    # Handle GET requests.
    # When the client sends a GET request, this method will be called.
    def do_GET(self) -> None:
        # Set the HTTP response status to 200 OK, which means the request was successful.
        self.send_response(200)

        # Set the Content-Type header to application/json, meaning the response will be in JSON format.
        self.send_header('Content-type', 'application/json')

        # Allow any domain to make requests to this server (CORS header).
        self.send_header('Access-Control-Allow-Origin', '*')

        # Finish sending headers
        self.end_headers()

        # Prepare the response data, which will be returned in JSON format.
        # The response contains a simple message and the path of the request.
        conn = connect_to_db()
        user_list = select_all_users(conn)
        response: dict = {
            "message": "Users sent from the server",
            "users": user_list
        }

        # Convert the response dictionary to a JSON string and send it back to the client.
        # `self.wfile.write()` is used to send the response body.
        self.wfile.write(json.dumps(response).encode())

    # Handle POST requests.
    # This method is called when the client sends a POST request.
    def do_POST(self) -> None:
        # Retrieve the content length from the request headers.
        # This tells us how much data to read from the request body.
        content_length: int = int(self.headers['Content-Length'])

        # Read the request body based on the content length.
        post_data: bytes = self.rfile.read(content_length)

        # Decode the received byte data and parse it as JSON.
        # We expect the POST request body to contain JSON-formatted data.
        received_data: dict = json.loads(post_data.decode())

        response: dict = {}

        if received_data.get("first_name") and received_data.get("last_name") and received_data.get("role"):
            conn = connect_to_db()
            insert_user(conn, received_data)
            response: dict = {
                "message": "User added"
            }
            self.send_response(200)
        else:
            response: dict = {
                "message": "Failed to add user. Required fields: first_name, last_name, role",
                "received_data": received_data
            }
            self.send_response(400)

        # Send the response headers.
        # Set the status to 200 OK and indicate the response content will be in JSON format.
        self.send_header('Content-type', 'application/json')

        # Again, allow any origin to access this resource (CORS header).
        self.send_header('Access-Control-Allow-Origin', '*')

        # Finish sending headers.
        self.end_headers()

        # Convert the response dictionary to a JSON string and send it back to the client.
        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())
        response: dict = {}

        if received_data.get("first_name") and received_data.get("last_name") and received_data.get("role"):
            conn = connect_to_db()
            delete_user(conn, received_data["id"])
            response: dict = {
                "message": "User removed"
            }
            self.send_response(200)
        else:
            response: dict = {
                "message": "Failed to remove user. Required fields: first_name, last_name, role",
                "received_data": received_data
            }
            self.send_response(400)

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


# Function to start the server.
# It takes parameters to specify the server class, handler class, and port number.
def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    # Define the server address.
    # '' means it will bind to all available network interfaces on the machine, and the port is specified.
    server_address: tuple = ('', port)

    # Create an instance of HTTPServer with the specified server address and request handler.
    httpd: HTTPServer = server_class(server_address, handler_class)

    # Print a message to the console indicating that the server is starting and which port it will listen on.
    print(f"Starting HTTP server on port {port}...")

    # Start the server and make it continuously listen for requests.
    # This method will block the program and keep running until interrupted.
    httpd.serve_forever()


# If this script is executed directly (not imported as a module), this block runs.
# It calls the `run()` function to start the server.
if __name__ == '__main__':
    run()