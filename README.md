# IDATA2304 - Assignment 3 - Socket Programming

## About
This project is part of the **IDATA2304 Computer Communication and Network Programming** course at NTNU.  
It implements a Smart TV system using **TCP sockets** in Python.

The assignment was divided into three parts:

---

### 🟩 Part 1 – Simple Smart TV Solution
- Implemented a **Smart TV server** (TCP) and a **remote control client**.  
- The TV can:
  - Be turned on/off  
  - Report power status  
  - Return the number of available channels  
  - Change and remember the current channel  
- Communication between the remote and TV is done via a **custom text-based application-layer protocol** (using commands like `ON`, `OFF`, `GET`, `SET`, etc.).

---

### 🟨 Part 2 – Refactoring
- Refactored the code to improve structure and readability.  
- Extracted the **TV logic** into a separate, communication-independent class (`SmartTv`).  
- Added separate modules for:
  - **Protocol parsing** (`TvProtocol.py`)  
  - **Command execution** (`TvCommands.py`)  
  - **Server handling** (`server.py`)  
  - **Client logic** (`remote.py`)  
- The protocol was designed to be easy to extend or modify without breaking other parts of the system.  
- Unit testing was optional and not implemented (time constraints, limited Python testing experience).

---

### 🟦 Part 3 – Multi-Client Support
- Extended the system to support **multiple remote clients simultaneously**.  
- Each client runs in a separate thread on the server.  
- Added **asynchronous event broadcasting**:
  - When one remote changes the channel, all other connected remotes receive a message like  
    `EVENT CHANNEL 3` to notify them immediately.  
- The client now includes a **background listener thread** to handle these incoming events while still allowing user input.

---

### 💻 Technologies Used
- **Language:** Python 3  
- **Libraries:** `socket`, `threading`, `queue`  
- **IDE:** Visual Studio Code

---

### Author
Ida Soldal — Computer Engineering Student, NTNU Ålesund
