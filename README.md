# 🔐 Secure Real-Time Leaderboard System

A Python-based secure client-server application that maintains a **live leaderboard** using sockets, multithreading, and SSL encryption.

---

## 🚀 Features

- 🔒 Secure communication using SSL/TLS  
- ⚡ Real-time leaderboard updates  
- 👥 Multi-client support using multithreading  
- 📊 Persistent leaderboard storage (JSON)  
- 🧠 Smart score update logic  
- 🌐 Auto server IP detection  
- 🔁 Continuous score streaming  

---

## 👨‍💻 Author

Meda Sahasra Siri
SRN: PES1UG24CS267

---

## 🖼️ Output Screenshots

### 💻 Client Output
![Client Output](./client-output.png)

### 🖥️ Server Output
![Server Output](./server-output.png)

> ⚠️ Make sure your image names match exactly:
> - `client-output.png`
> - `server-output.png`

---

## 🏗️ Project Structure


project/
│
├── server.py
├── client.py
├── leaderboard.json
│
├── server.crt
├── server.key
├── client.crt
├── client.key


---

## ⚙️ How It Works

### 🔹 Server
- Accepts secure client connections  
- Verifies client certificates  
- Maintains leaderboard  
- Broadcasts updates to all clients  

### 🔹 Client
- Connects securely to server  
- Sends random scores every 5 seconds  
- Receives live leaderboard updates  

---

## 📡 Communication Format

Client sends:


player_name,score,timestamp


---

## 🧪 Setup Instructions

### 1️⃣ Clone the Repository


git clone https://github.com/your-username/secure-leaderboard.git

cd secure-leaderboard


---

### 2️⃣ Generate SSL Certificates


openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key

openssl req -new -x509 -days 365 -nodes -out client.crt -keyout client.key


---

### 3️⃣ Run the Server


python3 server.py


---

### 4️⃣ Run the Client


python3 client.py


Enter player name when prompted.

---

## 📊 Sample Output


LIVE LEADERBOARD

AA → 425

---

## 🧠 Concepts Used

- Socket Programming (TCP)
- SSL/TLS Encryption
- Multithreading
- JSON Storage
- Real-time Broadcasting

---

## ⚠️ Notes

- Ensure all `.crt` and `.key` files are present  
- Works best on same network  
- Server runs on port `5001`  

---

## 🔮 Future Improvements

- 🌐 Web dashboard (React frontend)  
- 🗄️ Database integration  
- 🔐 Authentication system  
- ☁️ Cloud deployment  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub
