# command.py
from logic.executeCommand import execute_command
import logic.values as values

commands = []
current_line = 0
inputCoordinate = [10, 10]  # Đảm bảo vị trí nút được đặt đúng cách

def run_command(entry, update_display, run_button, next_button, end_button, highlight_current_line):
    global commands, current_line
    commands = entry.get("1.0", "end-1c").strip().splitlines()
    current_line = 0
    print("Run command executed. Total commands:", len(commands))  # Kiểm tra số lệnh nhập vào
    if commands:
        next_command(update_display, next_button, end_button, run_button, entry, highlight_current_line)
        if len(commands) >= 1:
            # Hiển thị nút "Next" và "End"
            print("Showing Next and End buttons")  # Thông báo hiển thị nút
            next_button.place(x=inputCoordinate[0] + 40, y=inputCoordinate[1] + 520)
            end_button.place(x=inputCoordinate[0] + 110, y=inputCoordinate[1] + 520)
        # Ẩn nút "Run"
        run_button.place_forget()

def next_command(update_display, next_button, end_button, run_button, entry, highlight_current_line):
    global current_line
    if current_line < len(commands):
        highlight_current_line(entry, current_line + 1)
        command = commands[current_line].strip()
        print(f"          EXECUTING COMMAND {current_line + 1}/{len(commands)}: {command}")  # Hiển thị lệnh đang thực thi
        execute_command(command)
        update_display()
        current_line += 1
        if current_line >= len(commands):
            # Ẩn nút "Next" và "End", hiển thị nút "Run"
            print("All commands executed. Showing Run button.")  # Thông báo tất cả lệnh đã thực thi
            next_button.place_forget()
            end_button.place_forget()
            run_button.place(x=inputCoordinate[0], y=inputCoordinate[1] + 520)

def end_command(update_display, next_button, end_button, run_button, root, entry, highlight_current_line):
    global current_line

    def execute_until_user_input():
        
        global current_line

        while current_line < len(commands):
            command = commands[current_line].strip()
            print(f"Executing command {current_line + 1}/{len(commands)}: {command}")
            execute_command(command)
            update_display()

            # Check if user input is required
            if values.is_userinput_21h == '1':
                print("Pausing for user input...")
                next_button.place_forget()
                end_button.place_forget()
                run_button.place_forget()

                # Monitor for user input readiness
                root.after(100, wait_for_user_input)
                return  # Exit this function until input is ready

            current_line += 1

        # All commands executed, show Run button
        print("All commands executed. Showing Run button.")
        next_button.place_forget()
        end_button.place_forget()
        run_button.place(x=inputCoordinate[0], y=inputCoordinate[1] + 520)
        update_display()

    def wait_for_user_input():
        """Wait until the user has provided input."""
        if values.is_userinput_21h == '0':  # User input is complete
            global current_line
            current_line += 1
            next_command(update_display, next_button, end_button, run_button)
            print("User input received. Resuming execution...")
            execute_until_user_input()  # Resume execution
        else:
            root.after(100, wait_for_user_input)  # Keep waiting

    # Start executing commands
    execute_until_user_input()
