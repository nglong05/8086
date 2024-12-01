from logic.values import flags, registers
from logic.updateFlags import update_flags
from logic.instructions.INT21H.handle01c import handle_01

def cmp(reg1, reg2):
    """Handle the CMP command - Compare two registers or a register and an immediate value."""
    if reg1 in registers:
        # Get the first operand value from registers
        operand1 = int(registers[reg1], 16)
        
        if reg2 in registers:
            # Get the second operand value from registers
            operand2 = int(registers[reg2], 16)
        else:
            try:
                # If reg2 is not a register, interpret it as an integer value
                operand2 = int(reg2)
            except ValueError:
                print(f"Invalid value for CMP: {reg2}")
                return

        # Perform the subtraction to compare (CMP is essentially a SUB without storing the result)
        result = operand1 - operand2

        # Use update_flags to set the flags
        is_8bit = reg1 in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']
        update_flags(result, operand1=operand1, operand2=operand2, operation='sub', is_8bit=is_8bit)

        print(f"After CMP, flags: {flags}")
    else:
        print(f"Invalid register: {reg1}")


def neg(register):
    # Check if the register is a valid 8-bit register
    if register.lower() in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']:
        # Retrieve the current 8-bit value and convert it to an integer
        value = int(registers[register.lower()], 16)
        negated_value = (-value) & 0xFF  # Perform two's complement negation and wrap around within 8 bits
        
        # Update the register
        registers[register.lower()] = f"{negated_value:02X}"
        
        # Update flags using the update_flags function
        update_flags(negated_value, operand1=value, operation='sub', is_8bit=True)
        
        print(f"After NEG, {register.upper()}: {registers[register.lower()]}")

    # Check if the register is a valid 16-bit register
    elif register.lower() in ['ax', 'bx', 'cx', 'dx']:
        # Split the 16-bit register into its high and low parts
        high, low = f"{register.lower()[0]}h", f"{register.lower()[0]}l"
        # Retrieve the current 16-bit value and convert it to an integer
        value = (int(registers[high], 16) << 8) + int(registers[low], 16)
        negated_value = (-value) & 0xFFFF  # Perform two's complement negation and wrap around within 16 bits
        
        # Update the high and low parts of the register
        registers[high] = f"{(negated_value >> 8) & 0xFF:02X}"
        registers[low] = f"{negated_value & 0xFF:02X}"
        
        # Update flags using the update_flags function
        update_flags(negated_value, operand1=value, operation='sub', is_8bit=False)
        
        print(f"After NEG, {register.upper()}: {registers[high]}{registers[low]}")
    
    else:
        print(f"No register like that: {register}")

import logic.values as values  # Import the module, not just the variable

def handle_21h():
    ah = values.registers.get('ah')
    print(f"debug ah variable: {ah}")
    if ah == "01":
        values.is_userinput_21h = '1'  # Update the shared state
        values.is_screen = '1'
        print(f"check is_userinput_21h in {__name__}: {values.is_userinput_21h}")
    elif ah == "02":
        #print(f"got here")
        values.is_screen = '1'
    elif ah == "09" :
        values.is_screen = '1'
    elif ah == "0A":
        values.is_userinput_21h = '1'
        print(f"got here")

