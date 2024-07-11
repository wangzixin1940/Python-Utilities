import math
import ttkbootstrap as ttk
from tkinter import messagebox as msgbox
from tkinter import Frame as tk_Frame

class Calculator(ttk.Window):
    def __init__(self):
        super().__init__()
        self.Buttons = [
            ["%", "CE", "C", "⏏"],
            ["1/x", "x^y", "2√x", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]
        self.signs = ["%", "1/x", "x^y", "2√x", "/", "*", "-", "+", "±"]
        self.functions = ["CE", "C", "±", "=", "⏏"]
        self.data = []
        self.title("Calculator")
        self.geometry("450x500")
        self.resizable(False, False)
        self.previous_type = None
        self.create_widgets()
    
    def create_widgets(self):
        self.result = tk_Frame(self, width=450, height=100)
        self.result.configure(bg="#F3F3F3")
        self.result.grid(column=0, row=0, columnspan=4, padx=5, pady=5)
        self.result_value = ttk.StringVar(value="".join(self.data))
        self.result_show = ttk.Label(self.result, textvariable=self.result_value, font=("Airal", 20), anchor="e")
        self.result_show.grid(column=0, row=0, columnspan=4, padx=5, pady=5)
        self.button_frame = ttk.Frame(self, width=400, height=500)
        self.button_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=5)
        # Create buttons
        for i, row in enumerate(self.Buttons):
            for j, button_text in enumerate(row):
                button = ttk.Button(self.button_frame, text=button_text, width=7, command=lambda text=button_text: self.button_click(text), bootstyle="primary-outline")
                button.grid(row=i, column=j, padx=5, pady=5)
    
    def button_click(self, text):
        if (text in self.functions): # Functions
            match text:
                case "CE":
                    self.data.remove(self.data[-1])
                    self.result_value.set("".join(self.data))
                case "C":
                    self.data = []
                    self.result_value.set("".join(self.data))
                case "⏏":
                    if (msgbox.askyesno("Quit", "OK to quit?")):
                        self.destroy()
                case "±":
                    if self.data[-1] in self.signs:
                        msgbox.showerror("Error", "The positive and negative nature of the symbol cannot be changed!\nOr enter the number first and then change the positive and negative of the symbol.")
                    else:
                        self.data[-1] = str(-float(self.data[-1]))
                        self.result_value.set("".join(self.data))
                case "=":
                    try:
                        self.data = [str(eval("".join(self.data)))]
                        self.result_value.set("".join(self.data))
                    except Exception as err:
                        msgbox.showerror("Error", "Expression error！\n{}".format(repr(err)))
            self.previous_type = "function"
        elif (text in self.signs): # Signs
            match text:
                case "1/x":   
                    self.data[-1] = "1/"+str(self.data[-1])
                    self.result_value.set("".join(self.data))
                case "%":
                    self.data[-1] = str(float(self.data[-1])/100)
                    self.result_value.set("".join(self.data))
                case "x^y":
                    self.append("**")
                case "2√x":
                    self.data[-1] = str(float(math.sqrt(float(self.data[-1]))))
                case _:
                    self.data.append(text)
            self.previous_type = "sign"
        else: # Numbers
            if (self.previous_type == "number"):
                self.data[-1] = self.data[-1] + text
            else:
                self.data.append(text)
            self.result_value.set("".join(self.data))
            self.previous_type = "number"


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
