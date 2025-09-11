from TvProtocol import TvCommand, okResponse, errorResponse
from SmartTvLogic import SmartTv

def executeCommand(cmd: TvCommand, tv: SmartTv) -> str:
    """
    Execute a TvCommand on the SmartTv and return a response string.
    Uses OK/ERR messages, but now includes more helpful info in OK responses.
    """
    try:
        t = cmd.type

        if t == "ON":
            tv.turnOn()
            # Instead of just OK, also tell the user what happened
            return okResponse("TV is ON, channel " + str(tv.getCurrentChannel())) # Get current channel as a string

        if t == "OFF":
            tv.turnOff()
            return okResponse("TV is OFF")

        if t == "STATUS":
            return okResponse("ON" if tv.isOn() else "OFF") # Return ON or OFF status depending on TV state

        if t == "CHANNELS":
            return okResponse(f"Total channels: {tv.getNumberOfChannels()}")

        if t == "GET":
            return okResponse(f"Current channel: {tv.getCurrentChannel()}")

        if t == "SET":
            if cmd.arg is None:
                return errorResponse("Missing channel number!")
            tv.setChannel(cmd.arg)
            return okResponse(f"Channel set to {tv.getCurrentChannel()}")

        if t == "QUIT":
            return "BYE\n"

        return errorResponse("Unknown command!")

    except (RuntimeError, ValueError) as e: # Catch errors from SmartTv methods
        return errorResponse(str(e)) # Return the error message in the response
