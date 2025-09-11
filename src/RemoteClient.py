import socket, sys # Import necessary modules. Socket for networking, sys for command-line arguments

def askUserForCommand(wFile, rFile, line: str) -> str: 
    # Helper function to send a command and get a response from the TV
    wFile.write(line + "\n")          # Write the command to the socket
    wFile.flush()                     # Flush to make sure it’s sent immediately
    reply = rFile.readline()          # Read the response from the socket
    return reply.strip() if reply else "" # Return the stripped response, or empty string if no reply

def printHelp():
    # Print instructions for the user
    print("Remote connected.")
    print("Available commands:")
    print("  on/off      - power the TV on or off")
    print("  up/down     - change channel")
    print("  get/status  - show current channel")
    print("  exit        - disconnect")

def handleChannelChange(k: str, wFile, rFile):
    # Helper to increment or decrement the channel safely
    st = askUserForCommand(wFile, rFile, "STATUS")
    if not st.endswith("ON"): 
        print("ERROR! TV is turned off."); return
    chs = askUserForCommand(wFile, rFile, "CHANNELS") # Total channels
    cur = askUserForCommand(wFile, rFile, "GET")      # Current channel
    try:
        C = int(chs.split()[-1]) # Parse number of channels
        n = int(cur.split()[-1]) # Parse current channel
    except Exception:
        print("ERROR! Cannot get channel info from TV."); return
    # Increment or decrement channel depending on command
    n = n + 1 if k in ("u","up") else n - 1
    if n < 1 or n > C:
        print("ERROR! Channel out of range."); return
    print(askUserForCommand(wFile, rFile, f"SET {n}"))

def handleUserLoop(wFile, rFile):
    # Main loop to interact with the user
    while True:
        k = input("> ").strip().lower() # Get user input, strip spaces, normalize to lowercase

        # QUIT / EXIT
        if k in ("e", "exit"):
            print(askUserForCommand(wFile, rFile, "QUIT"))
            break

        # ON / OFF
        elif k in ("o", "on"):
            st = askUserForCommand(wFile, rFile, "STATUS")
            cmd = "OFF" if st.endswith("ON") else "ON"
            print(askUserForCommand(wFile, rFile, cmd))
        elif k == "off":
            print(askUserForCommand(wFile, rFile, "OFF"))

        # CHANNEL UP / DOWN
        elif k in ("u","up","d","down"):
            handleChannelChange(k, wFile, rFile)

        # SHOW CHANNEL / STATUS
        elif k in ("g", "get", "status"):
            st = askUserForCommand(wFile, rFile, "STATUS")
            print(st)
            if st.endswith("ON"):
                print(askUserForCommand(wFile, rFile, "GET"))

        # UNKNOWN COMMAND
        else:
            print("ERROR! Unknown command.")

def runClientRemote(host: str, port: int): 
    # Connect to the TV server and start the remote interface
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a TCP socket
        s.connect((host, port)) # Connect to the server
        with s.makefile("r") as rFile, s.makefile("w") as wFile: # Create read/write file-like objects
            printHelp() # Show user instructions
            handleUserLoop(wFile, rFile) # Start the user interaction loop

if __name__ == "__main__":
    runClientRemote("localhost", 1238)
