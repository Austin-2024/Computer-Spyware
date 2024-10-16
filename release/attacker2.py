import socket

def listen_for_client():
    
    attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attacker_socket.bind(('0.0.0.0', 45923))
    attacker_socket.listen(5)
    print("Listening for connections coming from port 45923...")
    
    while True:
        client_socket, addr = attacker_socket.accept()
        print(f"Connected to: {addr}")

if __name__ == "__main__":
    listen_for_client()