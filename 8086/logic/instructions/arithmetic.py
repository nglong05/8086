from logic.values import flags, registers
from logic.updateFlags import update_flags
import logic.values as values
# First group: ADD, SUB, CMP, AND, TEST, OR, XOR
# These types of operands are supported:
# REG: AX, BX, CX, DX, AH, AL, BL, BH, CH, CL, DH, DL, DI, SI, BP, SP.                      #todo
# memory: [BX], [BX+SI+7], variable, etc...
# immediate: 5, -24, 3Fh, 10001101b, etc...
# After operation between operands, result is always stored in first operand. 
# CMP and TEST instructions affect flags only and do not store a result (these instruction are used to make decisions during program execution).
# These instructions affect these flags only   CF, ZF, SF, OF, PF, AF.

def add(dest, src):
    if dest in registers:
        # add a reg
        if src in registers:
            operand1 = int(registers[dest], 16)
            operand2 = int(registers[src], 16)
            result = operand1 + operand2

            registers[dest] = f"{result & 0xFF:02X}"
        # add a number
        else:
            if src.endswith('h'):
                operand2 = int(src[:-1], 16)  # Convert hex to int
            else:
                operand2 = int(src)  # Treat as decimal

            operand1 = int(registers[dest], 16)
            result = operand1 + operand2
            registers[dest] = f"{result & 0xFF:02X}"

        update_flags(result, operand1=operand1, operand2=operand2, operation='add', is_8bit=True)

    # Handle 16-bit registers
    elif dest in ['ax', 'bx', 'cx', 'dx']:
        if dest == 'ax':
            dest_high, dest_low = 'ah', 'al'
        elif dest == 'bx':
            dest_high, dest_low = 'bh', 'bl'
        elif dest == 'cx':
            dest_high, dest_low = 'ch', 'cl'
        elif dest == 'dx':
            dest_high, dest_low = 'dh', 'dl'

        # add reg to reg
        if src in ['ax', 'bx', 'cx', 'dx']:
            if src == 'ax':
                src_high, src_low = 'ah', 'al'
            elif src == 'bx':
                src_high, src_low = 'bh', 'bl'
            elif src == 'cx':
                src_high, src_low = 'ch', 'cl'
            elif src == 'dx':
                src_high, src_low = 'dh', 'dl'

            operand1 = (int(registers[dest_high], 16) << 8) + int(registers[dest_low], 16)
            operand2 = (int(registers[src_high], 16) << 8) + int(registers[src_low], 16)
            result = operand1 + operand2

            # Perform the addition and handle 16-bit wraparound
            registers[dest_high] = f"{(result >> 8) & 0xFF:02X}"
            registers[dest_low] = f"{result & 0xFF:02X}"
        # add num to reg
        else:
            if src.endswith('h'):
                operand2 = int(src[:-1], 16)  # Convert hex to int
            else:
                operand2 = int(src)  # Treat as decimal

            operand1 = (int(registers[dest_high], 16) << 8) + int(registers[dest_low], 16)
            result = operand1 + operand2

            # Split the value into high and low bytes
            registers[dest_high] = f"{(result >> 8) & 0xFF:02X}"
            registers[dest_low] = f"{result & 0xFF:02X}"

        # Update flags for a 16-bit operation
        update_flags(result, operand1=operand1, operand2=operand2, operation='add', is_8bit=False)

    elif dest == "ds":
        print(f"i dont have time for this {dest}, process to return")
        return
    
    else:
        print(f"No register like that: {dest}")
        return

    # Debugging
    if dest in registers:
        print(f"After ADD, {dest}: {registers[dest]}")
    else:
        print(f"After ADD, {dest_high}: {registers[dest_high]}, {dest_low}: {registers[dest_low]}")

def sub(dest, src):
    # Check if the destination is a valid 8-bit register
    if dest in registers:
        if src in registers:
            # Convert values to integers, perform subtraction, and handle 8-bit wraparound
            operand1 = int(registers[dest], 16)
            operand2 = int(registers[src], 16)
            result = operand1 - operand2
            registers[dest] = f"{result & 0xFF:02X}"

            # Update flags for an 8-bit operation
            update_flags(result, operand1=operand1, operand2=operand2, operation='sub', is_8bit=True)
        elif src in [code[0] for code in values.codeData]:
            for code in values.codeData:
                if code[0] == src:
                    print(f"code[2] is {code[2]}")
                    operand1 = int(registers[dest], 16)
                    operand2 = ord(code[2])
                    
                    result = operand1 - operand2
                    registers[dest] = f"{result & 0xFF:02X}"

            return
        else:
            if src.endswith('h'):
                operand2 = int(src[:-1], 16)  # Convert hex to int
            else:
                operand2 = int(src)  # Treat as decimal

            operand1 = int(registers[dest], 16)
            result = operand1 - operand2
            registers[dest] = f"{result & 0xFF:02X}"

            # Update flags for an 8-bit operation
            update_flags(result, operand1=operand1, operand2=operand2, operation='sub', is_8bit=True)
    
    # Handle 16-bit registers
    elif dest in ['ax', 'bx', 'cx', 'dx']:
        if dest == 'ax':
            dest_high, dest_low = 'ah', 'al'
        elif dest == 'bx':
            dest_high, dest_low = 'bh', 'bl'
        elif dest == 'cx':
            dest_high, dest_low = 'ch', 'cl'
        elif dest == 'dx':
            dest_high, dest_low = 'dh', 'dl'

        # Handling register-to-register subtraction for 16-bit registers
        if src in ['ax', 'bx', 'cx', 'dx']:
            if src == 'ax':
                src_high, src_low = 'ah', 'al'
            elif src == 'bx':
                src_high, src_low = 'bh', 'bl'
            elif src == 'cx':
                src_high, src_low = 'ch', 'cl'
            elif src == 'dx':
                src_high, src_low = 'dh', 'dl'

            # Convert values to integers, perform subtraction, and handle 8-bit wraparound
            operand1 = (int(registers[dest_high], 16) << 8) + int(registers[dest_low], 16)
            operand2 = (int(registers[src_high], 16) << 8) + int(registers[src_low], 16)
            result = operand1 - operand2

            registers[dest_high] = f"{(result >> 8) & 0xFF:02X}"
            registers[dest_low] = f"{result & 0xFF:02X}"

            # Update flags for a 16-bit operation
            update_flags(result, operand1=operand1, operand2=operand2, operation='sub', is_8bit=False)
        else:
            if src.endswith('h'):
                operand2 = int(src[:-1], 16)  # Convert hex to int
            else:
                operand2 = int(src)  # Treat as decimal

            operand1 = (int(registers[dest_high], 16) << 8) + int(registers[dest_low], 16)
            result = operand1 - operand2

            # Split the result into high and low bytes
            registers[dest_high] = f"{(result >> 8) & 0xFF:02X}"
            registers[dest_low] = f"{result & 0xFF:02X}"

            # Update flags for a 16-bit operation
            update_flags(result, operand1=operand1, operand2=operand2, operation='sub', is_8bit=False)
    
    else:
        print(f"No register like that: {dest}")
        return

    # Debugging
    if dest in registers:
        print(f"After SUB, {dest}: {registers[dest]}")
    else:
        print(f"After SUB, {dest_high}: {registers[dest_high]}, {dest_low}: {registers[dest_low]}")

def mul(src):
    # If src is an 8-bit register
    if src in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']:
        # Perform an 8-bit multiplication
        al_value = int(registers['al'], 16)
        src_value = int(registers[src], 16)
        result = al_value * src_value

        # Update AX with the result (lower 8 bits in AL, upper 8 bits in AH)
        registers['al'] = f"{result & 0xFF:02X}"
        registers['ah'] = f"{(result >> 8) & 0xFF:02X}"

        # Update flags for an 8-bit operation
        update_flags(result, operand1=al_value, operand2=src_value, operation='mul', is_8bit=True)

        # Debugging
        print(f"After MUL, AX: {registers['ah']}{registers['al']}")
        return

    # Handle case for 16-bit registers (AX, BX, CX, DX)
    elif src in ['ax', 'bx', 'cx', 'dx']:
        if src == 'ax':
            src_high, src_low = 'ah', 'al'
        elif src == 'bx':
            src_high, src_low = 'bh', 'bl'
        elif src == 'cx':
            src_high, src_low = 'ch', 'cl'
        elif src == 'dx':
            src_high, src_low = 'dh', 'dl'

        # Perform a 16-bit multiplication
        ax_value = (int(registers['ah'], 16) << 8) + int(registers['al'], 16)
        src_value = (int(registers[src_high], 16) << 8) + int(registers[src_low], 16)
        result = ax_value * src_value

        # Update AX with the lower 16 bits of the result
        registers['ah'] = f"{(result >> 8) & 0xFF:02X}"
        registers['al'] = f"{result & 0xFF:02X}"

        # Update DX with the upper 16 bits of the result
        registers['dh'] = f"{(result >> 24) & 0xFF:02X}"
        registers['dl'] = f"{(result >> 16) & 0xFF:02X}"

        # Update flags for a 16-bit operation
        update_flags(result, operand1=ax_value, operand2=src_value, operation='mul', is_8bit=False)

        # Debugging
        print(f"After MUL, AX: {registers['ah']}{registers['al']}, DX: {registers['dh']}{registers['dl']}")
    else:
        print(f"No register like that: {src}")
        return

def div(src):
    # Handle division for 8-bit source registers
    if src in ['ah', 'al', 'bh', 'bl', 'ch', 'cl', 'dh', 'dl']:
        src_value = int(registers[src], 16)

        # Check for division by zero
        if src_value == 0:
            print("Division by zero error!")
            return

        # Retrieve the value in AX (combining AH and AL into a 16-bit value)
        ax_value = (int(registers['ah'], 16) << 8) + int(registers['al'], 16)

        # Perform the division
        quotient = ax_value // src_value  # Integer division
        remainder = ax_value % src_value  # Remainder

        # Check for quotient overflow
        if quotient > 0xFF:
            print("Quotient overflow error!")
            return

        # Update AL with the quotient and AH with the remainder
        registers['al'] = f"{quotient & 0xFF:02X}"
        registers['ah'] = f"{remainder & 0xFF:02X}"

        # Debugging
        print(f"After DIV, AL (Quotient): {registers['al']}, AH (Remainder): {registers['ah']}")
        return

    # Handle division for 16-bit source registers
    elif src in ['ax', 'bx', 'cx', 'dx']:
        if src == 'ax':
            src_value = (int(registers['ah'], 16) << 8) + int(registers['al'], 16)
        elif src == 'bx':
            src_value = (int(registers['bh'], 16) << 8) + int(registers['bl'], 16)
        elif src == 'cx':
            src_value = (int(registers['ch'], 16) << 8) + int(registers['cl'], 16)
        elif src == 'dx':
            src_value = (int(registers['dh'], 16) << 8) + int(registers['dl'], 16)
        else:
            print(f"No register like that: {src}")
            return

        # Check for division by zero
        if src_value == 0:
            print("Division by zero error!")
            return

        # Retrieve the 32-bit value in DX:AX
        dx_value = (int(registers['dh'], 16) << 8) + int(registers['dl'], 16)
        ax_value = (int(registers['ah'], 16) << 8) + int(registers['al'], 16)
        dividend = (dx_value << 16) + ax_value  # Combine DX and AX into a 32-bit value

        # Perform the division
        quotient = dividend // src_value  # Integer division
        remainder = dividend % src_value  # Remainder

        # Check for quotient overflow
        if quotient > 0xFFFF:
            print("Quotient overflow error!")
            return

        # Update AX with the quotient and DX with the remainder
        registers['ah'] = f"{(quotient >> 8) & 0xFF:02X}"  # High byte of AX
        registers['al'] = f"{quotient & 0xFF:02X}"          # Low byte of AX
        registers['dh'] = f"{(remainder >> 8) & 0xFF:02X}"  # High byte of DX
        registers['dl'] = f"{remainder & 0xFF:02X}"         # Low byte of DX

        # Debugging
        print(f"After DIV, AX (Quotient): {registers['ah']}{registers['al']}, DX (Remainder): {registers['dh']}{registers['dl']}")
    else:
        print(f"No register like that: {src}")
        return


def inc(register):
    global flags  # Ensure we are modifying the global flags dictionary

    # Check if the register is a valid 8-bit register
    if register in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']:
        value = int(registers[register], 16)
        new_value = (value + 1) & 0xFF  # Wrap around for 8-bit overflow
        registers[register] = f"{new_value:02X}"

        # Update flags
        flags['ZF'] = new_value == 0  # Zero Flag
        flags['SF'] = (new_value & 0x80) != 0  # Sign Flag (MSB is 1 for negative numbers)
        flags['PF'] = bin(new_value).count('1') % 2 == 0  # Parity Flag (even number of 1-bits)
        flags['OF'] = (value == 0x7F)  # Overflow Flag (set if incrementing 0x7F causes overflow)

        print(f"After INC, {register.upper()}: {registers[register]}, Flags: {flags}")

    # Check if the register is a valid 16-bit register
    elif register in ['ax', 'bx', 'cx', 'dx']:
        high, low = f"{register[0]}h", f"{register[0]}l"
        value = (int(registers[high], 16) << 8) + int(registers[low], 16)
        new_value = (value + 1) & 0xFFFF  # Wrap around for 16-bit overflow
        registers[high] = f"{(new_value >> 8) & 0xFF:02X}"
        registers[low] = f"{new_value & 0xFF:02X}"

        # Update flags
        flags['ZF'] = new_value == 0  # Zero Flag
        flags['SF'] = (new_value & 0x8000) != 0  # Sign Flag (MSB is 1 for negative numbers)
        flags['PF'] = bin(new_value & 0xFF).count('1') % 2 == 0  # Parity Flag (only lower byte checked)
        flags['OF'] = (value == 0x7FFF)  # Overflow Flag (set if incrementing 0x7FFF causes overflow)

        print(f"After INC, {register.upper()}: {registers[high]}{registers[low]}, Flags: {flags}")

    else:
        print(f"No register like that: {register}")


def dec(register):
    global flags  # Ensure we are modifying the global flags dictionary

    # Check if the register is a valid 8-bit register
    if register in ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh']:
        value = int(registers[register], 16)
        new_value = (value - 1) & 0xFF  # Wrap around for 8-bit underflow
        registers[register] = f"{new_value:02X}"

        # Update flags
        flags['ZF'] = new_value == 0  # Zero Flag
        flags['SF'] = (new_value & 0x80) != 0  # Sign Flag (MSB is 1 for negative numbers)
        flags['PF'] = bin(new_value).count('1') % 2 == 0  # Parity Flag (even number of 1-bits)
        flags['OF'] = (value == 0x80)  # Overflow Flag (set if decrementing 0x80 causes overflow)

        print(f"After DEC, {register.upper()}: {registers[register]}, Flags: {flags}")

    # Check if the register is a valid 16-bit register
    elif register in ['ax', 'bx', 'cx', 'dx']:
        high, low = f"{register[0]}h", f"{register[0]}l"
        value = (int(registers[high], 16) << 8) + int(registers[low], 16)
        new_value = (value - 1) & 0xFFFF  # Wrap around for 16-bit underflow
        registers[high] = f"{(new_value >> 8) & 0xFF:02X}"
        registers[low] = f"{new_value & 0xFF:02X}"

        # Update flags
        flags['ZF'] = new_value == 0  # Zero Flag
        flags['SF'] = (new_value & 0x8000) != 0  # Sign Flag (MSB is 1 for negative numbers)
        flags['PF'] = bin(new_value & 0xFF).count('1') % 2 == 0  # Parity Flag (only lower byte checked)
        flags['OF'] = (value == 0x8000)  # Overflow Flag (set if decrementing 0x8000 causes overflow)

        print(f"After DEC, {register.upper()}: {registers[high]}{registers[low]}, Flags: {flags}")

    else:
        print(f"No register like that: {register}")

