import socket, sys, threading, queue  # NEW in Part 3: threading + queue for async messages

def askUserForCommand(wFile, replyQueue, line: str) -> str: 
    # Helper function to send a command and wait for a response from the TV
    wFile.write(line + "\n")
    wFile.flush()
    try:
        # NEW in Part 3: wait for next normal reply from receiver thread
        return replyQueue.get(timeout=10.0)
    except queue.Empty:
        return "ERROR! No response from TV."

def receiverLoop(rFile, replyQueue):
    """
    NEW in Part 3:
    Background thread that continuously listens for messages from the TV.
    - 'EVENT ...' lines are asynchronous notifications (printed immediately).
    - 'OK' / 'ERR' / 'BYE' lines are normal command replies, pushed into a queue.
    """
    while True:
        line = rFile.readline()
        if not line:
            print("Connection closed by TV.")
            break
        msg = line.strip()
        if msg.startswith("EVENT"):
            # NEW in Part 3: asynchronous event notification
            print(f"\n< {msg}")  # Show event on a new line
            print("> ", end="", flush=True)
        else:
            # Normal response to a user command → queue it for main loop
            replyQueue.put(msg)

def printHelp():
    # Print instructions for the user
    print("Remote connected.")
    print("Available commands:")
    print("  on/off      - power the TV on or off")
    print("  up/down     - change channel")
    print("  get/status  - show current channel")
    print("  exit        - disconnect")

def handleChannelChange(k: str, wFile, replyQueue):
    # Helper to increment or decrement the channel safely
    st = askUserForCommand(wFile, replyQueue, "STATUS")
    if not st.endswith("ON"):
        print("ERROR! TV is turned off."); return
    chs = askUserForCommand(wFile, replyQueue, "CHANNELS")
    cur = askUserForCommand(wFile, replyQueue, "GET")
    try:
        C = int(chs.split()[-1])
        n = int(cur.split()[-1])
    except Exception:
        print("ERROR! Cannot get channel info from TV."); return
    n = n + 1 if k in ("u", "up") else n - 1
    if n < 1 or n > C:
        print("ERROR! Channel out of range."); return
    print(askUserForCommand(wFile, replyQueue, f"SET {n}"))

def handleUserLoop(wFile, replyQueue):
    # Main loop to interact with the user
    while True:
        k = input("> ").strip().lower()

        if k in ("e", "exit"):
            print(askUserForCommand(wFile, replyQueue, "QUIT"))
            break
        elif k in ("o", "on"):
            st = askUserForCommand(wFile, replyQueue, "STATUS")
            cmd = "OFF" if st.endswith("ON") else "ON"
            print(askUserForCommand(wFile, replyQueue, cmd))
        elif k == "off":
            print(askUserForCommand(wFile, replyQueue, "OFF"))
        elif k in ("u", "up", "d", "down"):
            handleChannelChange(k, wFile, replyQueue)
        elif k in ("g", "get", "status"):
            st = askUserForCommand(wFile, replyQueue, "STATUS")
            print(st)
            if st.endswith("ON"):
                print(askUserForCommand(wFile, replyQueue, "GET"))
        else:
            print("ERROR! Unknown command.")

def runClientRemote(host: str, port: int):
    # Connect to the TV server and start the remote interface
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        with s.makefile("r") as rFile, s.makefile("w") as wFile:
            printHelp()
            # NEW in Part 3: create a queue and start a receiver thread
            replyQueue = queue.Queue()
            threading.Thread(
                target=receiverLoop, args=(rFile, replyQueue), daemon=True
            ).start()
            handleUserLoop(wFile, replyQueue)

if __name__ == "__main__":
    runClientRemote("localhost", 1238)
