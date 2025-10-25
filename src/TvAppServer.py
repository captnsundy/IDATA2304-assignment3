import socket, sys, threading  # NEW in Part 3: threading added for multi-client support
from SmartTvLogic import SmartTv
from TvProtocol import parseCommand
from TvCommands import executeCommand

# ===============================================================
# NEW in Part 3 — Shared resources for handling multiple clients
# ===============================================================
clients = set()                  # NEW: keeps track of all connected client writers
clients_lock = threading.Lock()  # NEW: ensures thread-safe access to 'clients'
tv_lock = threading.Lock()       # NEW: prevents race conditions on shared SmartTv
# ===============================================================

def broadcastEvent(message: str, exclude=None):
    """
    NEW in Part 3: Broadcast an asynchronous EVENT message
    (e.g., 'EVENT CHANNEL 3') to all connected remotes,
    except the one that triggered the change.
    """
    dead = []
    with clients_lock:
        for w in list(clients):
            if w is exclude:
                continue
            try:
                w.write(message + "\n")
                w.flush()
            except Exception:
                dead.append(w)
        for w in dead:  # Remove disconnected writers
            clients.discard(w)

def handleClient(conn, tv: SmartTv): 
    # Handles communication with a connected remote.
    with conn, conn.makefile("r") as rFile, conn.makefile("w") as wFile:
        # NEW in Part 3: Register this client for future broadcasts
        with clients_lock:
            clients.add(wFile)
        try:
            for line in rFile:  # Read commands line by line
                command = parseCommand(line)  # Parse the incoming line

                # NEW in Part 3: Lock the TV so only one client changes it at a time
                with tv_lock:
                    reply = executeCommand(command, tv)

                    # NEW in Part 3: Detect channel changes and broadcast them
                    if reply.startswith("OK") and (
                        "Channel set to" in reply or "Current channel" in reply
                    ):
                        ch = tv.getCurrentChannel()
                        broadcastEvent(f"EVENT CHANNEL {ch}", exclude=wFile)

                # Send reply back to remote
                wFile.write(reply)
                wFile.flush()
                if reply == "BYE\n":  # QUIT command → close connection
                    break
        finally:
            # NEW in Part 3: Unregister client when it disconnects
            with clients_lock:
                clients.discard(wFile)
            print("Remote disconnected")

def startServerSocket(port: int):
    # Create, bind, and return a listening server socket.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("0.0.0.0", port))
    serverSocket.listen()  # NEW in Part 3: allow multiple simultaneous connections
    print(f"TV listening on port {port} (CTRL+C to stop)")
    return serverSocket

def runServer(port: int = 1238, channels: int = 5):
    # Run the SmartTv TCP server.
    tv = SmartTv(channels)
    with startServerSocket(port) as serverSocket:
        while True:  # NEW in Part 3: keep accepting new remotes indefinitely
            conn, addr = serverSocket.accept()
            print(f"Remote connected from {addr}")
            # NEW in Part 3: start a thread for each remote
            threading.Thread(
                target=handleClient, args=(conn, tv), daemon=True
            ).start()

if __name__ == "__main__":
    runServer(1238)
