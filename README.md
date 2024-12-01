## 8086 Microprocessor Emulator
This project simulates the basic operations of an 8086 microprocessor, providing a simple environment to write, execute, and analyze assembly language commands.

### How to Run
Make sure you have Python installed on your system.

Navigate to the project directory.

Run the main script with the following command:

`python main.py`

### Supported Commands
- Arithmetic Operations: ADD, SUB, MUL, DIV, INC, DEC
- Data Transfer Instructions: MOV, LEA
- Comparison and Negation: CMP, NEG
- Interrupt Handling (INT 21h), supported subfunctions: AH = 1, 2, 9, 10
### Execution Modes
- Execute a complete ASM code script.
- Step-by-step execution with "Run All" or "Next Step" options, allowing you to observe changes in registers and flags in real time.
### Registers and Flags
- View and monitor the values of 8 registers: AH, AL, BH, BL, CH, CL, DH, DL
- Observe the state of the flags as they update during execution.
### Interactive Visualization
Includes a simple animation setup.
