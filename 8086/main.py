import tkinter as tk
from command import run_command, next_command, end_command
from logic.values import registers, flags
import logic.values as values
from animation import animation
from logic.instructions.INT21H.handle01c import update_screen_content
canvasSize = (1100, 600)


def highlight_current_line(entry, line_num):
    """Highlight the currently executed line in the Text widget."""
    # Remove previous highlight
    entry.tag_remove("highlight", "1.0", tk.END)
    
    # Add highlight to the specified line
    start = f"{line_num}.0"
    end = f"{line_num}.end"
    entry.tag_add("highlight", start, end)
    entry.tag_configure("highlight", background="yellow")

def show_setups(entry):
    """Display a window with predefined setups for user to select."""
    setups_window = tk.Toplevel(root)
    setups_window.title("Select a Predefined Setup")
    setups_window.geometry("400x300")
    
    tk.Label(setups_window, text="Select a setup:", font=("Arial", 12)).pack(pady=10)
    
    for description, commands in values.predefined_codes.items():
        # Pass both `description` and `commands` using `lambda` with default arguments
        tk.Button(
            setups_window,
            text=description,
            command=lambda cmds=commands: insert_code(entry, cmds, setups_window),
            width=40
        ).pack(pady=5)

def update_animation_button(canvas):
    global animation_button
    buttonOffset = 520
    if values.is_animation_running == '1':
        if 'animation_button' not in globals() or not animation_button.winfo_exists():
            # Create the animation button if it doesn't exist
            animation_button = tk.Button(canvas, text="Animation")
            animation_button.place(x=inputCoordinate[0] + 60, y=inputCoordinate[1] + buttonOffset + 35)
            animation_button.config(command=lambda: animation(canvas))
    else:
        # Destroy the button if animation is not running
        if 'animation_button' in globals() and animation_button.winfo_exists():
            animation_button.destroy()


def insert_code(entry, commands, window):
    """Insert the selected predefined commands into the text box."""
    for command in commands:
        entry.insert(tk.END, f"{command}\n")
    window.destroy()

    print("Checking commands...")
    if commands == values.predefined_codes["perform animation"]:
        values.is_animation_running = '1'
        print(f"Animation triggered: {values.is_animation_running}")
    else:
        values.is_animation_running = '0'

    # Update the animation button dynamically
    update_animation_button(entry.master)  # Pass the canvas


def reset_state(entry, update_display, emulate_button, next_button, end_button):
    # Reset registers
    for reg in registers:
        registers[reg] = "00" if len(reg) == 2 else "0000"

    # Reset flags
    for flag in flags:
        flags[flag] = 0 if flag != 'IF' else 1  # Default IF is 1

    # Reset state variables
    values.is_userinput_21h = '0'
    values.is_screen = '0'
    values.userInput = ''
    values.screenContent = ''
    values.being_in_data_segment = '0'
    values.codeData = []  # [data_name, type (db/dw), value, len]
    values.leastr = ''

    # Destroy screen widgets if they exist
    global output_box, label_output_box
    if 'output_box' in globals() and output_box.winfo_exists():
        output_box.destroy()
    if 'label_output_box' in globals() and label_output_box.winfo_exists():
        label_output_box.destroy()

    entry.delete("1.0", tk.END)
    update_display()
    emulate_button.place(x=inputCoordinate[0], y=inputCoordinate[1] + 520)
    next_button.place_forget()
    end_button.place_forget()

def draw_int21h():
    print(f"is screen is: {values.is_screen} and is input is {values.is_userinput_21h}")
    # create input for user
    if (values.is_screen == '1' and values.is_userinput_21h == '1'):
        inputint21hCoordinate = [270, 120]
        label = tk.Label(canvas, text="Input")
        text = tk.Text(canvas, width=20, height=2)
        button = tk.Button(canvas, text="Enter")
        # Place them as part of the canvas
        label_window = canvas.create_window(inputint21hCoordinate[0], inputint21hCoordinate[1], anchor="nw", window=label)
        text_window = canvas.create_window(inputint21hCoordinate[0], inputint21hCoordinate[1] + 20, anchor="nw", window=text)
        button_window = canvas.create_window( inputint21hCoordinate[0] + 167, inputint21hCoordinate[1] + 25, anchor="nw", window=button)

        def handle_input():
            values.userInput = text.get("1.0", "end-1c").strip()
            print(f"User input received in handle_input(): {values.userInput}")

            draw_screen(canvas)

            values.is_userinput_21h = '0'
            print(f"is_userinput_21h updated to {values.is_userinput_21h} after user input")
            draw_values(canvas)
            canvas.delete(label_window)
            canvas.delete(text_window)
            canvas.delete(button_window)

            next_button.place(x=inputCoordinate[0] + 40, y=inputCoordinate[1] + 520)
            end_button.place(x=inputCoordinate[0] + 110, y=inputCoordinate[1] + 520)
        

        button.config(command=handle_input)
        next_button.place_forget()
        end_button.place_forget()
    if (values.is_screen == '1' and values.is_userinput_21h == '0'):
            
            draw_screen(canvas)
            values.is_screen = '0'
            draw_values(canvas)
    print('aaaaaaaaaaaaaaaaaaaaaaaa')
    if (values.is_screen == '0' and values.is_userinput_21h == '1'):
        print(f"may be its int 21h 10")
        inputint21hCoordinate = [270, 120]
        label = tk.Label(canvas, text="Input")
        text = tk.Text(canvas, width=20, height=2)
        button = tk.Button(canvas, text="Enter")
        # Place them as part of the canvas
        label_window = canvas.create_window(inputint21hCoordinate[0], inputint21hCoordinate[1], anchor="nw", window=label)
        text_window = canvas.create_window(inputint21hCoordinate[0], inputint21hCoordinate[1] + 20, anchor="nw", window=text)
        button_window = canvas.create_window( inputint21hCoordinate[0] + 167, inputint21hCoordinate[1] + 25, anchor="nw", window=button)

        def handle_input():
            values.userInput = text.get("1.0", "end-1c").strip()
            print(f"User input received in handle_input(): {values.userInput}")

            for dataName in values.codeData:
                print(f"check {dataName[0]}")
                if dataName[0] == values.leastr:
                    dataName[2] += str(values.userInput)
                    print(f"Updated value for {dataName[0]}: {dataName[2]}")
            
            values.is_userinput_21h = '0'
            print(f"is_userinput_21h updated to {values.is_userinput_21h} after user input")
            draw_values(canvas)
            canvas.delete(label_window)
            canvas.delete(text_window)
            canvas.delete(button_window)

            next_button.place(x=inputCoordinate[0] + 40, y=inputCoordinate[1] + 520)
            end_button.place(x=inputCoordinate[0] + 110, y=inputCoordinate[1] + 520)
        

        button.config(command=handle_input)
        next_button.place_forget()
        end_button.place_forget()

def draw_input(canvas):
    global inputCoordinate
    inputCoordinate = [10, 10]
    # Label
    entry_label = tk.Label(canvas, text="Enter commands (one per line):")
    entry_label.place(x=inputCoordinate[0], y=inputCoordinate[1])
    # Input
    entry = tk.Text(canvas, width=30, height=30)
    entry.place(x=inputCoordinate[0], y=inputCoordinate[1] + 20)
    # Buttons
    buttonOffset = 520
    global emulate_button, next_button, end_button
    emulate_button = tk.Button(canvas, text="Emulate")
    emulate_button.place(x=inputCoordinate[0], y=inputCoordinate[1] + buttonOffset)

    next_button = tk.Button(canvas, text="Next step")
    next_button.place_forget()  # Initially hidden

    end_button = tk.Button(canvas, text="Run all")
    end_button.place_forget()  # Initially hidden

    reset_button = tk.Button(canvas, text="Reset")
    reset_button.place(x=inputCoordinate[0] + 160, y=inputCoordinate[1] + buttonOffset)

    # Add the Setups button
    setups_button = tk.Button(canvas, text="Setups", command=lambda: show_setups(entry))
    setups_button.place(x=inputCoordinate[0] + 0, y=inputCoordinate[1] + buttonOffset + 35)

    # #animation button
    # print(f"got here value is {values.is_animation_running}")
    # if values.is_animation_running == '1':
    #     animation_button = tk.Button(canvas, text="Animation")
    #     animation_button.place(x=inputCoordinate[0] + 60, y=inputCoordinate[1] + buttonOffset + 35)
    #     animation_button.config(command=lambda: animation(canvas))


    # Configure button commands
    emulate_button.config(command=lambda: run_command(entry, update_display, emulate_button, next_button, end_button, highlight_current_line))
    next_button.config(command=lambda: next_command(update_display, next_button, end_button, emulate_button, entry, highlight_current_line))
    end_button.config(command=lambda: end_command(update_display, next_button, end_button, emulate_button, root, entry, highlight_current_line))
    reset_button.config(command=lambda: reset_state(entry, update_display, emulate_button, next_button, end_button))

def draw_values(canvas):
    registerCoordinate = [270, 200]  
    flagsCoordinate = [270, 300]
    register_display = tk.Text(canvas, width=25, height=4)
    register_label = tk.Label(canvas, text= "Register hex values")
    register_display.place(x=registerCoordinate[0], y=registerCoordinate[1] + 21)
    register_label.place(x=registerCoordinate[0], y=registerCoordinate[1])
    register_display.insert(tk.END, f"AH: {registers['ah']}, AL: {registers['al']}\n")
    register_display.insert(tk.END, f"BH: {registers['bh']}, BL: {registers['bl']}\n")
    register_display.insert(tk.END, f"CH: {registers['ch']}, CL: {registers['cl']}\n")
    register_display.insert(tk.END, f"DH: {registers['dh']}, DL: {registers['dl']}\n")

    flags_display = tk.Text(canvas, width=25, height=8)
    flags_label = tk.Label(canvas, text= "Flag values")
    flags_display.place(x=flagsCoordinate[0], y=flagsCoordinate[1] + 21)
    flags_label.place(x=flagsCoordinate[0], y=flagsCoordinate[1])
    for flag, value in flags.items():
        flags_display.insert(tk.END, f"{flag}: {value}\n")

def draw_image(canvas):
    # Load image and place it
    img = tk.PhotoImage(file="UI/a.png")
    canvas.create_image(500, 300, image=img, anchor="w")
    canvas.image = img 

def draw_screen(canvas):
    global output_box, label_output_box

    # Check if screen should be drawn
    if values.is_screen == '0':  # Avoid recreating when reset
        print("Screen is disabled; skipping draw_screen.")
        return

    outputCoordinate = [270, 30]

    # Destroy previous instances if they exist
    if 'output_box' in globals() and output_box.winfo_exists():
        output_box.destroy()
    if 'label_output_box' in globals() and label_output_box.winfo_exists():
        label_output_box.destroy()

    # Create new screen widgets
    label_output_box = tk.Label(canvas, text="Screen")
    output_box = tk.Text(canvas, width=25, height=4, state=tk.NORMAL)
    label_output_box.place(x=outputCoordinate[0], y=outputCoordinate[1])
    output_box.place(x=outputCoordinate[0], y=outputCoordinate[1] + 20)

    # Update screen content
    update_screen_content()
    output_box.insert(tk.END, values.screenContent)
    print(f'Inserted "{values.screenContent}" to the screen.')

def update_display():
    
    draw_values(canvas)
    draw_int21h()

root = tk.Tk()
root.title("8086 Emulator")

canvas = tk.Canvas(root, width=canvasSize[0], height=canvasSize[1])
canvas.pack()


draw_input(canvas)
draw_image(canvas)  
draw_values(canvas)

update_display()

root.mainloop()