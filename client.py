import socket
import time
import random
import threading
import ssl

def get_default_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def listen_server(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                print(data)
        except:
            break

def start_client(player_name):
    context = ssl.create_default_context()
    context.load_cert_chain(certfile="client.crt", keyfile="client.key")
    context.load_verify_locations("server.crt")

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_client = context.wrap_socket(raw_socket, server_hostname="server")

    server_ip = "172.20.10.3"
    print(f"Auto connecting to server at {server_ip}")

    try:
        secure_client.connect((server_ip, 5001))
        print("Securely connected to server")
    except Exception as e:
        print("Connection failed:", e)
        return

    threading.Thread(target=listen_server, args=(secure_client,), daemon=True).start()

    while True:
        try:
            score = random.randint(100, 500)
            timestamp = time.time()
            message = f"{player_name},{score},{timestamp}\n"
            secure_client.sendall(message.encode())
            print(f"Sent: {score}")
            time.sleep(5)

        except:
            print("Connection lost")
            break

if __name__ == "__main__":
    name = input("Enter player name: ")
    start_client(name)
