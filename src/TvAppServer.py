import socket, sys # Import necessary modules. Socket for networking, sys for command-line arguments
from SmartTvLogic import SmartTv
from TvProtocol import parseCommand
from TvCommands import executeCommand

def handleClient(conn, tv: SmartTv): 
    # Handle communication with a connected remote.
    with conn, conn.makefile("r") as rFile, conn.makefile("w") as wFile:
        for line in rFile: # Read commands line by line
            command = parseCommand(line) # Parse the incoming line into a TvCommand
            reply = executeCommand(command, tv) # Execute the command on the SmartTv
            wFile.write(reply) # Send reply back to remote
            wFile.flush() 
            if reply == "BYE\n": # QUIT command → close connection
                break

def startServerSocket(port: int):
    # Create, bind, and return a listening server socket.
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set socket options to reuse address
    serverSocket.bind(("0.0.0.0", port))  # Bind to all interfaces on the specified port
    serverSocket.listen(1)  # Listen for incoming connections, with a backlog of 1
    print(f"TV listening on port {port} (CTRL+C to stop)")
    return serverSocket

def runServer(port: int = 1238, channels: int = 5):
    # Run the SmartTv TCP server.
    tv = SmartTv(channels) # Create the SmartTv logic
    with startServerSocket(port) as serverSocket: # Start the server socket
        conn, addr = serverSocket.accept() # Accept one client
        print(f"Remote connected from {addr}")
        handleClient(conn, tv) # Delegate work to handler
        print("Remote disconnected")

if __name__ == "__main__":
    # Default port 1238
    runServer(1238)
