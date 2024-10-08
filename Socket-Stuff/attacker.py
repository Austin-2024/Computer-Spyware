import socket

def start_client(target_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((target_ip, 45923))

    while True:
        command = input("Enter command to send (or 'exit' to quit): ")
        client_socket.sendall(command.encode('utf-8'))
        
        if command.lower() == 'exit':
            break
        
        response = client_socket.recv(4096).decode('utf-8')
        print("Response:\n", response)

    client_socket.close()

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    start_client(target_ip)
