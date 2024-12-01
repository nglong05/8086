from logic.values import registers, flags

def update_flags(result, operand1=None, operand2=None, operation=None, is_8bit=True):
    # Mask based on the bit size (8-bit or 16-bit)
    max_value = 0xFF if is_8bit else 0xFFFF

    # Unsigned overflow check
    flags['CF'] = 1 if (result > max_value) or (result < 0) else 0

    # Zero Flag (ZF) - Set if the result is zero
    flags['ZF'] = 1 if (result & max_value) == 0 else 0

    # Sign Flag (SF) - Set if the most significant bit is 1 (indicating a negative result in signed context)
    if is_8bit:
        flags['SF'] = 1 if (result & 0x80) != 0 else 0
    else:
        flags['SF'] = 1 if (result & 0x8000) != 0 else 0

    # Overflow Flag (OF) - Set if there is a signed overflow
    if operation in ['add', 'sub'] and operand1 is not None and operand2 is not None:
        if operation == 'add':
            if is_8bit:
                flags['OF'] = 1 if ((operand1 & 0x80) == (operand2 & 0x80)) and ((result & 0x80) != (operand1 & 0x80)) else 0
            else:
                flags['OF'] = 1 if ((operand1 & 0x8000) == (operand2 & 0x8000)) and ((result & 0x8000) != (operand1 & 0x8000)) else 0
        elif operation == 'sub':
            if is_8bit:
                flags['OF'] = 1 if ((operand1 & 0x80) != (operand2 & 0x80)) and ((result & 0x80) == (operand2 & 0x80)) else 0
            else:
                flags['OF'] = 1 if ((operand1 & 0x8000) != (operand2 & 0x8000)) and ((result & 0x8000) == (operand2 & 0x8000)) else 0
    else:
        flags['OF'] = 0

    # Parity Flag (PF) - Set if there is an even number of 1 bits in the lowest byte of the result
    flags['PF'] = 1 if bin(result & 0xFF).count('1') % 2 == 0 else 0

    # Auxiliary Flag (AF) - Set if there is an unsigned overflow for the lower nibble (4 bits)
    if operand1 is not None and operand2 is not None and operation in ['add', 'sub']:
        flags['AF'] = 1 if ((operand1 & 0xF) + (operand2 & 0xF)) > 0xF else 0
    else:
        flags['AF'] = 0

    # Note: IF and DF flags are not automatically updated and are typically managed manually
