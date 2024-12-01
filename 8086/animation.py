import tkinter as tk


global duration
duration = 4000

path1 = [
    (860, 180),
    (860, 130),
    (900, 80),
    (999, 80),
    (999, 250),
    (999, 350),
    (999, 505),
    (935, 505),
    (867, 505),
]

subpath1 = [
    (945, 180),
    (945, 130),
    (900, 80),
    (999, 80),
    (999, 250),
    (999, 350),
    (999, 505),
    (935, 505),
    (867, 505),
]

path2 = [
    (867, 505),
    (775, 505),
]

subpath2 = [
    (867, 505),
    (837, 505),
    (837, 352),
    (644, 352),
    (644, 260),
    (670, 105),        
]

path3 = [
    (670, 105),
    (644, 260),
    (644, 352),
    (585, 352),
    (585, 470),
    (600, 500),
    (600, 510),
    (600, 510),
    (547, 510),
    (547, 350),
    (644, 350),
    (644, 260),
    (670, 105),   
]

subpath3 = [
    (670, 105),
    (644, 260),
    (644, 352), 
    (703, 352),
    (703, 470),    
    (600, 500),
    (600, 510),
    (600, 510),
    (547, 510),
    (547, 350),
    (644, 350),
    (644, 260),
    (670, 105),   
]


global stop_flag
def animate_data_transfer(canvas, path, color, callback=None):
    if len(path) < 2:
        # Handle single-point paths
        circle = canvas.create_oval(
            path[0][0] - 10, path[0][1] - 10,
            path[0][0] + 10, path[0][1] + 10,
            fill=color
        )
        canvas.coords(
            circle,
            path[0][0] - 10, path[0][1] - 10,
            path[0][0] + 10, path[0][1] + 10
        )
        if callback:
            canvas.after(0, callback)
        return

    circle = canvas.create_oval(
        path[0][0] - 10, path[0][1] - 10,
        path[0][0] + 10, path[0][1] + 10,
        fill=color
    )
    interval = 10
    total_frames = duration // interval
    total_segments = len(path) - 1

    def interpolate(start, end, progress):
        return start + (end - start) * progress

    def update_position(frame):
        if stop_flag:
            return
        
        nonlocal circle
        overall_progress = frame / total_frames

        if overall_progress >= 1.0:
            canvas.coords(
                circle,
                path[-1][0] - 10, path[-1][1] - 10,
                path[-1][0] + 10, path[-1][1] + 10
            )
            if callback:
                canvas.after(0, callback)
            return

        segment = int(overall_progress * total_segments)
        segment_progress = (overall_progress * total_segments) - segment

        start_x, start_y = path[segment]
        end_x, end_y = path[segment + 1]
        current_x = interpolate(start_x, end_x, segment_progress)
        current_y = interpolate(start_y, end_y, segment_progress)

        canvas.coords(
            circle,
            current_x - 10, current_y - 10,
            current_x + 10, current_y + 10
        )
        canvas.after(interval, update_position, frame + 1)

    update_position(0)

def load_image(canvas, image_path):
    img = tk.PhotoImage(file=image_path)
    canvas.create_image(500, 300, image=img, anchor="w")
    canvas.image = img  # Retain reference to prevent garbage collection

def animation(canvas):
    global stop_flag
    stop_flag = False

    # Sequence of animations with images
    def step1():
        load_image(canvas, "UI/a.png")
        animate_data_transfer(canvas, path1, "red", callback=step2)
        animate_data_transfer(canvas, subpath1,"red", callback=step2)
    
    def step2():
        load_image(canvas, "UI/mov1.png")
        animate_data_transfer(canvas, path2,"red", callback=step3)
        animate_data_transfer(canvas, subpath2,"red", callback=step3)
        animate_data_transfer(canvas, path1,"blue", callback=step3)
        animate_data_transfer(canvas, subpath1,"blue", callback=step3)

    def step3():
        load_image(canvas, "UI/mov2.png")
        animate_data_transfer(canvas, path1, "green", callback=step4)
        animate_data_transfer(canvas, subpath1,"green", callback=step4)
        animate_data_transfer(canvas, path2, "blue",callback=step4)
        animate_data_transfer(canvas, subpath2, "blue",callback=step4)
    def step4():
        load_image(canvas, "UI/mov3.png")
        animate_data_transfer(canvas, path2,"green", callback=step5)
    def step5():
        load_image(canvas, "UI/mov4.png")
        animate_data_transfer(canvas, path3,"brown", callback=step6)
        animate_data_transfer(canvas, subpath3,"brown", callback=step6)
    def step6():
        load_image(canvas, "UI/mov5.png")
        global stop_flag
        stop_flag = True

    step1()



def add_animation_button(canvas):
    button = tk.Button(canvas, text="Animate Data", command=lambda: animation(canvas))
    canvas.create_window(400, 100, anchor="nw", window=button)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("8086 Emulator with Animation")

    canvas = tk.Canvas(root, width=1100, height=600)
    canvas.pack()

    add_animation_button(canvas)

    root.mainloop()
