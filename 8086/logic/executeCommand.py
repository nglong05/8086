from logic.instructions.arithmetic import add, sub, mul, div, inc, dec
from logic.instructions.data_transfer import mov, lea
from logic.instructions.special import cmp, neg, handle_21h
import logic.values as values
import re

def prepare(statement):
    if statement.lower() in [".model", ".stack"]:
        print(f"get {statement} but skipped")
        return

    elif statement.lower() == ".data":
        print(f"got {statement} and change values.being_in_data_segment = 1")
        values.being_in_data_segment = '1'
    elif statement.lower() == ".code":
        print(f"got {statement} and change values.being_in_data_segment = 0")
        values.being_in_data_segment = '0'
    else:
        raise ValueError(f"what is this {statement}")

def execute_command(command):
    if not command:
        print(f"not get a command, process to return")
        return
    command = command.lower().replace(",", "")
    parts = command.split()
    instruction = parts[0] 

    # make sure nothing pop up
    values.is_screen = '0'
    values.is_userinput_21h = '0'

    # Handle directives
    if instruction.startswith('.'):
        print(f"got {instruction}, process to go to prepare func...")
        prepare(instruction)

    # Handle data segment
    elif values.being_in_data_segment == '1':
        if len(parts) < 3:
            raise ValueError(f"Invalid data declaration: {command}")

        # data parts
        data_name = parts[0]
        data_type = parts[1].lower()
        raw_value = " ".join(parts[2:])#.replace("'", "").replace("$", "")
        print(f"raw value is {raw_value}")
        
        #regex the data value
        if raw_value.startswith("'"):
            data_value = re.findall(r"'([^']*)'", raw_value)[0]
            print(f"its a string, data value is {data_value}")
        else: 
            if parts[2] == '?':
                print(f"get a ? input")
                values.codeData.append([data_name, data_type, "", 0])
                print(f"append [{data_name}|{data_type}|{"null"}|0] to the codeData value")
                return
            #string input
            pattern = r"dup\('\$'\)"
            if re.search(pattern, raw_value):
                print(f"get a string input")
                values.codeData.append([data_name, data_type, "", int(parts[2])])
                print(f"append [{data_name}|{data_type}|{"null"}|{int(parts[2])}] to the codeData value")
                return
            #hex or number
            raw_value = raw_value.replace("'", "")
            print(f"raw value is {raw_value}")
            value = raw_value.replace(",", "").split()
            print(f"value is {value}")
            data_value = ""
            for val in value:
                if val.endswith("$"):
                    data_value += val
                    print(f"data value is {data_value}")
                else:
                    data_value += chr(int(val, 16) if 'h' in val.lower() else int(val))
                    print(f"data value is {data_value}")
        
        #calulate the offset
        if data_type == "db":
            data_offset = len(data_value)
        elif data_type == "dw":
            data_offset = 2*len(data_value)
        else:
            print(f"What is this {data_type}, process to raise error")
            raise ValueError

        
        # Append as a list to codeData
        print(f"append [{data_name}|{data_type}|{data_value}|{data_offset}] to the codeData value")
        values.codeData.append([data_name, data_type, data_value, data_offset])
    
    elif instruction == "main":
        print(f"got {instruction}, process to return")
        return
    # data transfer
    elif instruction == 'mov':
        mov(parts[1], parts[2])
    elif instruction == 'lea':
        lea(parts[1], parts[2])

    #arithmetric
    elif instruction == 'add':
        add(parts[1], parts[2])
    elif instruction == 'sub':
        sub(parts[1], parts[2])
    elif instruction == 'mul':
        mul(parts[1])  
    elif instruction == 'div':
        div(parts[1])     
    elif instruction == 'inc':
        inc(parts[1])    
    elif instruction == 'dec':
        dec(parts[1])     

    #control transfer         
    elif instruction == 'neg':
        neg(parts[1])
    elif instruction == 'cmp':
        cmp(parts[1], parts[2])
    
    #int 21h
    elif instruction == 'int':
        if parts[1] == '21h':
            handle_21h()
        else:
            print(f':( this program dont support this {parts[1]}')

    #print("Registers:", registers)
    #print("Flags:", flags)
    print("debug: string command is:", command)
