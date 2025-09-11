# The Tv Protocol defines how the remote will communicate with the TV.
# It uses simple commands with optional arguments.
# With this class we keep the protocol logic separate from the TV logic, making it easier to manage and extend.
from dataclasses import dataclass # Import dataclass for creating simple data structures
from typing import Optional # Import Optional for type hinting, so we can have arguments that can be None

@dataclass(frozen=True) # First we define a dataclass to represent a TV command.
class TvCommand:
    type: str # Type is stored as a string
    arg: Optional[int] = None # Argument is optional and can be an integer or None
    
def parseCommand(line: str) -> TvCommand: # Function to parse a command string into a TvCommand object. Easy to extend later.
    if not line: # Check if the input line is empty
        return TvCommand("UNKNOWN") # Return an UNKNOWN command if the line is empty
    parts = line.strip().split() # Split the line into parts based on whitespace
    if not parts: # Check if there are no parts after splitting
        return TvCommand("UNKNOWN") # Return an UNKNOWN command if there are no parts
    key = parts[0].upper() # Convert the first part to uppercase to standardize command keys
    if key in {"ON","OFF","STATUS","CHANNELS","GET","QUIT"}: # Check if the key is one of the known commands
        return TvCommand(key) # Return the command with the key and no argument
    if key == "SET" and len(parts) == 2: # Check if the command is SET and has exactly one argument
        try:# Try to convert the argument to an integer
            return TvCommand("SET", int(parts[1])) # Return the SET command with the integer argument
        except ValueError: # If conversion fails, handle the error
            return TvCommand("UNKNOWN")
    return TvCommand("UNKNOWN") # Return an UNKNOWN command if the command is not recognized

def okResponse(payload: Optional[str] = None) -> str: # Function to generate an OK response, optionally with a payload
    return "OK\n" if not payload else f"OK {payload}\n" # Return "OK" if no payload, otherwise return "OK" followed by the payload
    # Payload can be any string, such as a channel number or status message.

def errorResponse(reason: str) -> str: # Function to generate an ERROR response with a reason
    # An error response can happen for various reasons, such as invalid commands or actions that cannot be performed.
    return f"ERROR {reason}\n" # Return "ERROR" followed by the reason