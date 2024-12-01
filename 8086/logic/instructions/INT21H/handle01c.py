from logic.values import registers
import logic.values as values

def update_screen_content():
    print("Function update_screen_content was called.")
    if registers['ah'] == '01':
        handle_01()
    if registers['ah'] == '02':
        handle_02()
    if registers['ah'] == '09':
        handle_09()

def handle_01():
    if len(values.userInput) > 1:
        raise ValueError("Invalid input: userInput must be 1 character.")
    values.screenContent += values.userInput
    registers['al'] = f"{ord(values.userInput):02x}"  # Convert to hex ASCII
def handle_02():
    values.screenContent += bytes.fromhex(registers['dl']).decode("ASCII")
def handle_09():
    print(f"got to handle_09 func")
def handle_10():
    print(f"go to handle 10")
