from tkinter import Tk, StringVar, N, S, E, W, Canvas, ttk, \
                    messagebox as msgbox
import math
import sys

class LazzarusGraphGUI():
    root: Tk
    canvas: Canvas
    coord_lbl: ttk.Label
    w_width: int
    w_height: int
    c_width: float
    c_height: float
    offsetx: float
    offsety: float
    f_sv: StringVar
    unit_size: int = 50
    initial_function: str

    def __init__(self, title: str="Title", width: int= 500, height: int=400, 
                 resize_x: bool= True, resize_y: bool = True,
                 initial_function: str=""):
        self.root = Tk()
        self.root.title(title)
        self.w_width = width
        self.w_height = height
        self.root.geometry(f"{self.w_width}x{self.w_height}")
        self.root.resizable(width=resize_x, height=resize_y)
        self.initial_function = initial_function
        self.setup_widgets()
        self.root.mainloop()

    def setup_widgets(self):
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=N+S+E+W)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # configuring canvas
        self.c_width = self.w_width-400
        self.c_height = self.w_height
        self.canvas = Canvas(mainframe, width=self.c_width, 
                             height=self.c_height, background="#FFF",
                             cursor="tcross")
        self.canvas.grid(column=0, row=0, sticky=N+S+E+W)

        self.offsetx: float = self.c_width/2
        self.offsety: float = self.c_height/2

        self.draw_canvas_axis_and_grid()

        # inputs
        self.f_sv = StringVar(value=self.initial_function)
        f_sv_entry = ttk.Entry(mainframe, width=30, textvariable=self.f_sv)
        ttk.Label(mainframe, text="f(x)=").grid(column=1, row=0)
        f_sv_entry.grid(column=2, row=0)
        f_sv_entry.focus()

        self.coord_lbl = ttk.Label(mainframe, text="(0,0)")
        self.coord_lbl.grid(column=4, row=0)

        ttk.Button(mainframe, text="Grafico", 
                   command=self.graphf).grid(column=3, row=0)
        self.root.bind("<Return>", self.graphf)
        self.canvas.bind("<Motion>", self.get_mouse_coord)

        if self.initial_function != "": self.graphf()

    def get_mouse_coord(self, event) -> None:
        """ Sets the coord_lbl text to the current mouse x and y position
         on the canvas """
        mouse_x, mouse_y = event.x, event.y
        x: float = (mouse_x-self.offsetx)/self.unit_size
        y: float = -(mouse_y-self.offsety)/self.unit_size

        # move the cursor lines
        self.canvas.coords("h_line", 
                           0, 
                           -y*self.unit_size+self.offsety,
                           self.c_width,
                           -y*self.unit_size+self.offsety,)
        self.canvas.coords("v_line", 
                           x*self.unit_size+self.offsetx, 
                           0,
                           x*self.unit_size+self.offsetx,
                           self.c_height,)
        

        self.coord_lbl.configure(text=f"({x}, {y})")

    def graphf(self, *args) -> None:
        self.canvas.delete("all")
        self.draw_canvas_axis_and_grid()
        
        f = ""
        try:
            f = self.f_sv.get()
        except ValueError: 
            pass

        if f == "": return

        f = self.clean_operators(f)

        f = f.replace("x", "x0") 
        f2 = f.replace("x0", "x1") 

        step: float=0.05
        x0: float = (-self.c_width/self.unit_size)-step
        stop: float = self.c_width/self.unit_size
        while x0 < stop-step:
            x0 += step
            try:
                # calculating the points used to draw the lines incrementally 
                # print(f"Function: {f}")
                y0: float = -eval(f)
                x1: float = x0 + step
                y1: float = -eval(f2)

                # calculating the distance between the points
                # to avoid weird jumps
                x_dist: float = (x1 - x0 )**2
                y_dist: float = (y0 - y1)**2
                dist: float = math.sqrt(x_dist + y_dist)
                if (abs(dist) > (self.c_height/10)) \
                   or (abs(dist) > (self.c_width/10)): 
                   continue
            except NameError as e:
                msgbox.showerror(message=str(e), title="Error")
                return
            except ValueError as e: # catching operations out of the domain
                continue
            except TypeError as e: 
                msgbox.showerror(message=str(e), title="Error")
                return
            except SyntaxError as e: 
                msgbox.showerror(message=str(e), title="Error")
                return
            except OverflowError:
                continue
            
            # print(f"Drawing line: ({x0}, {y0}) -> ({x1}, {y1})")
            self.canvas.create_line(x0*self.unit_size+self.offsetx, 
                                    y0*self.unit_size+self.offsety, 
                                    x1*self.unit_size+self.offsetx, 
                                    y1*self.unit_size+self.offsety, 
                                    fill="#0000FF")
    
    def draw_canvas_axis_and_grid(self) -> None:
        # drawing grid
        assert (self.c_width/2) % self.unit_size == 0, \
            msgbox.showerror(
                message=("The size of each unit must be divisible by "
                         "(width of canvas)/2"),
                title="size_unit error")
        
        assert (self.c_height/2) % self.unit_size == 0, \
            msgbox.showerror(
                message=("The size of each unit must be divisible by "
                         "(height of canvas)/2"),
                title="size_unit error")

        x: float = -self.c_width - self.unit_size
        while x < self.c_width:
            x += self.unit_size
            self.canvas.create_line(x, 0, x, self.c_height, fill="#EEE")

        y: float = -self.c_height - self.unit_size
        while y < self.c_height:
            y += self.unit_size
            self.canvas.create_line(0, y, self.c_width, y, fill="#EEE")
        
        # draw subgrid
        counter: int = 0
        substep: int = 2
        x: float = -self.c_width - (self.unit_size/substep)
        while x < self.c_width:
            x += (self.unit_size/substep)
            if counter % 2:
                self.canvas.create_line(x, 
                                        0, 
                                        x, 
                                        self.c_height, 
                                        fill="#EEE", 
                                        dash=1)
            counter += 1

        counter = 0
        y: float = -self.c_height - (self.unit_size/substep)
        while y < self.c_height:
            y += (self.unit_size/substep)
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
        while x < self.c_width:
            x += self.unit_size
            num += self.unit_size
            if num < 0 or num > 0:
                self.canvas.create_text(x, 
                                        (self.c_height/2)+10, 
                                        text=f"{int(num/self.unit_size)}", 
                                        fill="#777")
            else:
                # draw the 0 slightly offset to the left
                self.canvas.create_text(x-10, 
                                        (self.c_height/2)+10, 
                                        text=f"{int(num/self.unit_size)}", 
                                        fill="#777")
            
        # drawing numbers on the y axis
        y = 0
        num = (-self.c_height/2)
        while y < self.c_height:
            y += self.unit_size
            num += self.unit_size
            if num < 0 or num > 0:
                self.canvas.create_text((self.c_width/2)-10,
                                         y, 
                                         text=f"{int(-num/self.unit_size)}", 
                                         fill="#777")    

        half_w: float = self.c_width/2
        half_h: float = self.c_height/2
        self.canvas.create_line(half_w,
                                0, 
                                half_w,
                                self.c_height,
                                arrow="first",
                                fill="gray")
        self.canvas.create_line(0, 
                                half_h, 
                                self.c_width, 
                                half_h, 
                                arrow="last",
                                fill="gray")

        # drawing 
        self.canvas.create_line(half_w,
                                0, 
                                half_w,
                                self.c_height,
                                fill="#AAA",
                                tags="v_line")
        self.canvas.create_line(0, 
                                half_h, 
                                self.c_width, 
                                half_h,  
                                fill="#AAA",
                                tags="h_line")
    
    def clean_operators(self, f: str) -> str:
        f = f.replace("^", "**")
        f = f.replace("\\", "/")
        f = f.replace("tan", "math.tan")
        f = f.replace("atan", "math.atan")
        f = f.replace("arctg", "math.atan")
        f = f.replace("arctan", "math.atan")
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
            start = idx = 0
            while True:
                try:
                    idx = f.index("!", start)
                except ValueError:
                    # all the factorials have been found
                    break
                
                start = idx
                idx_s = idx_e = -1
                closed = 0 # number of closed parethesis
                # scanning the string backwards starting from the index of the
                # '!' character - 1
                for i in range(idx-1, -1, -1):
                    if idx_e == -1 and f[i] == ")": 
                        # end parenthesis found
                        idx_e = i
                        continue
                    
                    if idx_e != -1 and f[i] == ")": 
                        # encountered another closed parenthesis
                        closed += 1
                        continue

                    if closed == 0 and f[i] == "(": 
                        # there is an equal amount of opened an closed
                        # parenthesis
                        idx_s = i
                        break

                    if idx_s == -1 and f[i] == "(": 
                        # encountered another opened parhentesis
                        closed -= 1
                arg = f[idx_s:idx_e+1]
                # print(f"arg: {arg}")
                f = f.replace(f"{arg}!", 'math.gamma(' + arg + "+1)")
        # TODO: handle sin^n, cos^n
        return f

def main() -> None:
    args = sys.argv
    initial_function: str = ""
    if "--help" in args:
        print(f"Usage: python {args[0]} \"intial_function\"")
        print(f"Example: python {args[0]} \"sin(x)\"")
        exit(0)
    if len(args) > 1:
        initial_function = args[1]
        
    window_w: int = 1200
    window_h: int = window_w - 400
    LazzarusGraphGUI(title="LazzarusGraph", width=window_w, height=window_h, 
        resize_x=False, resize_y=False, initial_function=initial_function)

if __name__ == "__main__":
    main()