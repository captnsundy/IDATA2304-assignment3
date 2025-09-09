# The SmartTv class represents a smart television with a specified number of channels.
# Like a real TV, it can be turned on and off, and you can change channels when it's on.
# This class only handles the logic of the TV, not the user interface.
# It does not depend on communication protocols, or any other classes in this project.
class SmartTv:
    def __init__(self, channels:int): # Self is the instance of the class, channels is the number of channels the TV has
        if channels <= 0: # Validate that the number of channels is greater than 0
            raise ValueError("Channels cannot be 0 or less.")
        self.on = False # TV is off by default
        self.channels = channels # Total number of channels based on user input
        self.current = 1 # Current channel starts at 1
        
    def isOn(self) -> bool: # Boolean method to check if the TV is on or off
        return self.on # Return the current state of the TV (on or off)
    
    def turnOn(self) -> None: # Method to turn the TV on, none return type
        self.on = True # Set the TV state to on
        
    def turnOff(self) -> None: # Method to turn the TV off, none return type
        self.on = False # Set the TV state to off
        
    def ensureIsOn(self): # Helper method to ensure the TV is on before performing actions
      if not self.on: # Check if the TV is off
        raise RuntimeError("TV is turned off.") # Raise an error if the TV is off when trying to perform an action
        
    def getNumberOfChannels(self) -> int: # Method to get the total number of channels, returns an integer
        self.ensureIsOn() # Ensure the TV is on before getting the number of channels
        return self.channels # Return the total number of channels
    
    def getCurrentChannel(self) -> int: # Method to get the current channel number, returns an integer
        self.ensureIsOn()
        return self.current # Return the current channel number
    
    def setChannel(self, channel:int) -> None:
        self.ensureIsOn()
        if channel < 1 or channel > self.channels: # Validate that the channel number is within the valid range [1, total channels]
            raise ValueError("Invalid channel. Channel is out of range.")
        self.current = channel # Set the current channel to the new channel number