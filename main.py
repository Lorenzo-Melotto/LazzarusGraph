from tkinter import Tk, StringVar, N, S, E, W, Canvas, Label, ttk
import math
import numpy as np

class GUI():
    root: Tk
    canvas: Canvas
    err_lbl: Label
    w_width: int
    w_height: int
    c_width: float
    c_height: float
    f_sv: StringVar
    unit_size: int = 50

    def __init__(self, title: str="Title", width: int= 500, height: int=400):
        self.root = Tk()
        self.root.title(title)
        self.w_width = width
        self.w_height = height
        self.root.geometry(f"{self.w_width}x{self.w_height}")
        self.root.resizable(width=False, height=False)
        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=N+S+E+W)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # configuring canvas
        self.c_width = self.w_width-300
        self.c_height = self.w_height
        self.canvas = Canvas(mainframe, width=self.c_width, 
                             height=self.c_height, background="#FFF")
        self.canvas.grid(column=0, row=0, sticky=N+S+E+W)

        self.draw_canvas_axis_and_grid()

        # inputs
        self.f_sv = StringVar()
        f_sv_entry = ttk.Entry(mainframe, width=30, textvariable=self.f_sv)
        ttk.Label(mainframe, text="f(x)=").grid(column=1, row=0)
        f_sv_entry.grid(column=2, row=0)
        f_sv_entry.focus()

        ttk.Button(mainframe, text="Grafico", 
                   command=self.graphf).grid(column=3, row=0)
        self.root.bind("<Return>", self.graphf)

    def graphf(self, *args) -> None:
        self.canvas.delete("all")
        self.draw_canvas_axis_and_grid()
        f = ""
        try:
            f = self.f_sv.get()
        except ValueError: 
            pass

        f = self.clean_operators(f)
        # used to calculate the next point of the function
        f2 = f.replace("x", "x1") 

        # centering where the function will be drawn
        offsetx: float = self.c_width/2
        offsety: float = self.c_height/2

        step: float=0.008
        assert step <= 0.01, f"Step must be <= 0.01, \
            otherwise weird artifacts will appear (now is {step})"
        x: float = (-self.c_width/self.unit_size)-step
        stop: float = self.c_width/self.unit_size
        while x < stop-step:
            x += step
            try:
                # calculating the points used to draw the lines incrementally 
                # print(f"Function: {f}")
                y0: float = -eval(f)
                x1: float = x + step
                y1: float = -eval(f2)
            except ValueError: # catching operations out of the domain
                continue

            # calculating the distance between the points to avoid weird jumps
            x_dist: float = (x1 - x )**2
            y_dist: float = (y0 - y1)**2
            dist: float = math.sqrt(x_dist + y_dist)
            if abs(dist) > self.c_height: continue

            self.canvas.create_line(x*self.unit_size+offsetx, 
                                    y0*self.unit_size+offsety, 
                                    x1*self.unit_size+offsetx, 
                                    y1*self.unit_size+offsety, 
                                    fill="#0000FF")
    
    def draw_canvas_axis_and_grid(self) -> None:
        # drawing grid
        for x in np.arange(-self.c_width, self.c_width, self.unit_size):
            self.canvas.create_line(x, 0, x, self.c_height, fill="#EEE")

        for y in np.arange(-self.c_width, self.c_width, self.unit_size):
            self.canvas.create_line(0, y, self.c_width, y, fill="#EEE")
        
        # draw subgrid
        counter = 0
        for x in np.arange(-self.c_width, self.c_width, self.unit_size/2):
            if counter % 2:
                self.canvas.create_line(x, 
                                        0, 
                                        x, 
                                        self.c_height, 
                                        fill="#EEE", 
                                        dash=1)
            counter += 1

        counter = 0
        for y in np.arange(-self.c_width, self.c_width, self.unit_size/2):
            if counter % 2:
                self.canvas.create_line(0, 
                                        y, 
                                        self.c_width, 
                                        y, 
                                        fill="#EEE", 
                                        dash=1)
            counter += 1

        # drawing numbers on the x axis
        x = 0
        num = (-self.c_width/2)
        while x <= self.c_width:
            x += self.unit_size
            num += self.unit_size
            if num < 0 or num > 0:
                self.canvas.create_text(x, 
                                        (self.c_height/2)+10, 
                                        text=f"{int(num/self.unit_size)}", 
                                        fill="#777")
            else:
                self.canvas.create_text(x-10, 
                                        (self.c_height/2)+10, 
                                        text=f"{int(num/self.unit_size)}", 
                                        fill="#777")
            
        # drawing numbers on the y axis
        y = 0
        num = (-self.c_height/2)
        while y <= self.c_height:
            y += self.unit_size
            num += self.unit_size
            if num < 0 or num > 0:
                self.canvas.create_text((self.c_width/2)-10,
                                         y, 
                                         text=f"{int(-num/self.unit_size)}", 
                                         fill="#777")    

        self.canvas.create_line(self.c_width/2,
                                0, 
                                self.c_width/2,
                                self.c_height,
                                fill="gray")
        self.canvas.create_line(0, 
                                self.c_height/2, 
                                self.c_width, 
                                self.c_height/2, 
                                fill="gray")
    
    def clean_operators(self, f: str) -> str:
        f = f.replace("^", "**")
        f = f.replace("\\", "/")
        f = f.replace("tan", "math.tan")
        f = f.replace("tg", "math.tan")
        f = f.replace("sin", "math.sin")
        f = f.replace("sen", "math.sin")
        f = f.replace("cos", "math.cos")
        f = f.replace("e", "math.e")
        f = f.replace("pi", "math.pi")
        f = f.replace("log", "math.log10")
        f = f.replace("ln", "math.log")
        f = f.replace("sqrt", "math.sqrt")
        if "!" in f:
            idx = f.index("!")
            idx_s = idx_e = -1
            closed = 0
            for i in range(idx-1, -1, -1):
                if idx_e == -1 and f[i] == ")": 
                    idx_e = i
                    continue
                
                if idx_e != -1 and f[i] == ")": 
                    closed += 1
                    continue

                if closed == 0 and f[i] == "(": 
                    idx_s = i
                    break

                if idx_s == -1 and f[i] == "(": 
                    closed -= 1
            arg = f[idx_s:idx_e+1]
            f = f.replace(f"{arg}!", 'math.gamma(' + arg + "+1)")
        return f

def main() -> None:
    GUI(title="LazzarusGraph", width=1000, height=500)

if __name__ == "__main__":
    main()