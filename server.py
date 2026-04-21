import socket
import threading
import time
import json
import ssl

leaderboard = {}
clients = []
lock = threading.Lock()
last_update = {}

# 🔥 Auto-detect server IP
def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

try:
    with open("leaderboard.json", "r") as f:
        leaderboard = json.load(f)
        leaderboard = {k: tuple(v) for k, v in leaderboard.items()}
except:
    leaderboard = {}

def save_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def broadcast(message):
    dead_clients = []
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            dead_clients.append(client)

    for dc in dead_clients:
        if dc in clients:
            clients.remove(dc)

def format_leaderboard():
    sorted_board = sorted(
        leaderboard.items(),
        key=lambda x: x[1][0],
        reverse=True
    )

    msg = "\nLIVE LEADERBOARD\n"
    for i, (p, (s, _)) in enumerate(sorted_board[:5], 1):
        msg += f"{i}. {p} → {s}\n"
    return msg

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    with lock:
        clients.append(conn)

    buffer = ""

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                parts = line.split(",")

                if len(parts) != 3:
                    continue

                try:
                    player, score, ts = parts
                    score = int(score)
                    ts = float(ts)
                except:
                    continue

                if player in last_update and time.time() - last_update[player] < 1:
                    continue
                last_update[player] = time.time()

                updated = False

                with lock:
                    if player not in leaderboard:
                        leaderboard[player] = (score, ts)
                        updated = True
                    else:
                        old_score, old_ts = leaderboard[player]

                        if score > old_score or (score == old_score and ts > old_ts):
                            leaderboard[player] = (score, ts)
                            updated = True

                if updated:
                    save_leaderboard()
                    msg = format_leaderboard()
                    print(msg)
                    broadcast(msg)

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"[DISCONNECTED] {addr}")

    with lock:
        if conn in clients:
            clients.remove(conn)

    conn.close()

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.load_verify_locations("client.crt")
    context.verify_mode = ssl.CERT_REQUIRED

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5001))
    server.listen()

    server_ip = "172.20.10.3"
    print(f"[STARTED] Secure Server running on {server_ip}:5001")

    while True:
        conn, addr = server.accept()

        try:
            secure_conn = context.wrap_socket(conn, server_side=True)
        except ssl.SSLError:
            print("SSL handshake failed")
            conn.close()
            continue

        thread = threading.Thread(target=handle_client, args=(secure_conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_server()