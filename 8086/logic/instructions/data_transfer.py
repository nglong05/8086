from logic.values import flags, registers
from logic.updateFlags import update_flags
import logic.values as values

def mov(dest, src):
    # Check if the destination is a valid 8-bit register
    if dest in registers:
        # Handling register-to-register transfer for 8-bit registers
        if src in registers:
            # Copy value from source to destination as a hex string
            registers[dest] = registers[src]
        elif src.startswith("@"):
            print(f"got {src}, process to return")
            return
        elif src in [data[0] for data in values.codeData]:  # Check if `src` exists in codeData
            for data in values.codeData:
                if data[0] == src:
                    print(f"found {src} in codeData, process to update")
                    # Update the destination register with the data value as a hex string
                    registers[dest] = f"{data[2]:02X}"
                    break
        else:
            # Handle the case where src is a hex or decimal value or a character
            if src.endswith('h'):
                src_value = int(src[:-1], 16)  # Convert hex to int
            elif src.startswith("'") and src.endswith("'"):
                # Convert single character to its ASCII value
                src_value = ord(src[1])
            else:
                src_value = int(src)  # Treat as decimal
                print(f"src_value is {src_value}")

            # Ensure the value fits in 8 bits
            if src_value < 0 or src_value > 0xFF:
                print(f"Value out of range for 8-bit register: {src_value}")
                return

            # Move the value into the destination register as a hex string
            registers[dest] = f"{src_value:02X}"
        
        update_flags(int(registers[dest], 16), is_8bit=True)

    # Handle the case for 16-bit registers (like AX, BX, CX, DX)
    elif dest in ['ax', 'bx', 'cx', 'dx']:
        if dest == 'ax':
            dest_high, dest_low = 'ah', 'al'
        elif dest == 'bx':
            dest_high, dest_low = 'bh', 'bl'
        elif dest == 'cx':
            dest_high, dest_low = 'ch', 'cl'
        elif dest == 'dx':
            dest_high, dest_low = 'dh', 'dl'

        #handleing @
        if src.startswith("@"):
            print(f"got {src}, process to return")
            return
        
        # Handling register-to-register transfer for 16-bit registers
        if src in ['ax', 'bx', 'cx', 'dx']:
            if src == 'ax':
                src_high, src_low = 'ah', 'al'
            elif src == 'bx':
                src_high, src_low = 'bh', 'bl'
            elif src == 'cx':
                src_high, src_low = 'ch', 'cl'
            elif src == 'dx':
                src_high, src_low = 'dh', 'dl'

            # Copy values from source to destination as hex strings
            registers[dest_high] = registers[src_high]
            registers[dest_low] = registers[src_low]
        else:
            # Handle the case where src is a hex or decimal value
            if src.endswith('h'):
                src_value = int(src[:-1], 16)  # Convert hex to int
            else:
                src_value = int(src)  # Treat as decimal

            # Split the value into high and low bytes
            src_high_value = (src_value >> 8) & 0xFF  # Extract high byte
            src_low_value = src_value & 0xFF          # Extract low byte

            # Move the values into the destination register parts as hex strings
            registers[dest_high] = f"{src_high_value:02X}"
            registers[dest_low] = f"{src_low_value:02X}"
        
        # Combine the high and low parts into a 16-bit value and update flags
        combined_value = (int(registers[dest_high], 16) << 8) + int(registers[dest_low], 16)
        update_flags(combined_value, is_8bit=False)


    if dest in [data[0] for data in values.codeData]:  # Check if `dest` exists in codeData
        for data in values.codeData:
            if data[0] == dest:
                print(f"found {dest} in codeData, process to update")
                # Check if `src` is a register
                if src in values.registers:
                    src_value = int(values.registers[src], 16)  # Get value from the register
                # Check if `src` is a hexadecimal or decimal value
                elif src.endswith('h'):
                    src_value = int(src[:-1], 16)  # Convert hex to int
                elif src.isdigit():
                    src_value = int(src)  # Treat as decimal
                else:
                    print(f"Invalid source operand: {src}")
                    return
                print(f"src value is {src_value}")
                
                # Update `data_value` in codeData
                data[2] = src_value
                print(f"update data value to {src_value}")
                break
        else:
            print(f"Destination {dest} not found in codeData")


    else:
        print(f"No register like that: {dest}")
        return

    # # Print registers for debugging
    # if dest in registers:
    #     print(f"After MOV, {dest}: {registers[dest]}")
    # else:
    #     print(f"After MOV, {dest}: {registers[dest_high]}{registers[dest_low]}")

def lea(dest, src):
    if dest == "dx":
        print(f"got {src} in lea command, process...")
        values.leastr = src
        print(f"update values.leastr to {src}")
        offset = 0
        for nameData in values.codeData:
            offset += nameData[3]
            print(f"update offset: {offset}")
            if nameData[0] == src:
                print(f"dest now is {dest}")
                dest = offset - nameData[3]
                registers['dh'] = f"{(dest >> 8) & 0xFF:02X}"
                registers['dl'] = f"{dest & 0xFF:02X}"
                print(f"dh now is : {registers['dh']} and hl is {registers['dl']}")
        # int 21h 09
        if registers['ah'] == "09":
            print(f'determine its int21h 09')
            for nameData in values.codeData:
                if nameData[0] == src:
                    print(f"found you {src}, add to screen content")
                    values.screenContent += nameData[2].replace("$", "")
        # int 21h 10
        if registers['ah'] == "0A":
            print(f"got int21 10")
        
    else:
        print(f"cant lea this {dest}, process to raise error")
        raise ValueError
        