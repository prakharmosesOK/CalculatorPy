import tkinter as tk

SPECIAL_BUTTON_BG = "#2796d6"
NORAL_BUTTON_BG = "#3a3a3a"
SPECIAL_BUTTON_FG = "#ffffff"
SPECIAL_BUTTON_ACTIVE_BG = "#4bb5f2"
NORMAL_BUTTON_ACTIVE_BG = "#5a5a5a"
BACKGROUND_COLOUR = "#141310"

class StandardCalculator:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=BACKGROUND_COLOUR, padx=10, pady=5)
        self.input_var = tk.StringVar()
        self.last_used = None

        # Computed display prior equals
        self.computed_display = tk.StringVar()
        self.computed_display_label = tk.Label(self.frame, textvariable=self.computed_display, font=("Arial", 12), bg=BACKGROUND_COLOUR, fg="white", anchor="e")
        self.computed_display_label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10)

        # Display
        self.display = tk.Entry(self.frame, textvariable=self.input_var, font=("Arial", 20), bd=0, justify="right", bg=BACKGROUND_COLOUR, fg="white", insertbackground="white")
        self.display.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=(0,10), ipady=5, ipadx=10)

        # Button layout
        self.buttons = [
            ['%', 'CE', 'C', '<-'],
            ['1/x', 'x²', '√x', '÷'],
            ['7', '8', '9', 'X'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]

        # Create buttons
        for r, row in enumerate(self.buttons):
            for c, char in enumerate(row):
                btn = tk.Button(self.frame,
                                text=char,
                                font=("Arial", 16),
                                bg=NORAL_BUTTON_BG if char not in ['=', 'C'] else SPECIAL_BUTTON_BG,
                                fg="white",
                                bd=0,
                                activebackground=NORMAL_BUTTON_ACTIVE_BG if char not in ['=', 'C'] else SPECIAL_BUTTON_ACTIVE_BG,
                                command=lambda ch=char: self.on_button_click(ch))
                btn.grid(row=r+2, column=c, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=10)
        
        # Grid Configuration
        for i in range(4):
            self.frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.frame.rowconfigure(i, weight=1)
    
    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.input_var.get())
                self.input_var.set(result)
            except Exception as e:
                self.input_var.set("Error")
        elif char == 'C':
            self.input_var.set("")
            self.computed_display.set("")
        elif char == '<-':
            current_text = self.input_var.get()
            self.input_var.set(current_text[:-1])
        elif char == 'CE':
            self.input_var.set("")
        elif char == '+/-':
            self.input_var.set(str(-float(self.input_var.get())))
        elif char == '1/x':
            try:
                result = 1 / float(self.input_var.get())
                self.input_var.set(result)
            except ZeroDivisionError:
                self.input_var.set("Error")
        elif char == 'x²':
            try:
                result = float(self.input_var.get()) ** 2
                self.input_var.set(result)
            except ValueError:
                self.input_var.set("Error")
        elif char == '√x':
            try:
                result = float(self.input_var.get()) ** 0.5
                self.input_var.set(result)
            except ValueError:
                self.input_var.set("Error")
        elif char == '%':
            try:
                result = float(self.input_var.get()) / 100
                self.input_var.set(result)
            except ValueError:
                self.input_var.set("Error")
        elif char in ['+', '-', 'X', '÷']:
            if self.computed_display.get() and self.computed_display.get()[-2] in ['+', '-', 'X', '÷']:
                self.computed_display.set(self.computed_display.get()[:-2] + char + " ")
            else:
                current_text = self.input_var.get()
                self.computed_display.set(current_text + " " + char + " ")
            self.last__used = char
        else:
            current_computed_text = self.computed_display.get()
            if current_computed_text and current_computed_text[-2] in ['+', '-', 'X', '÷']:
                self.input_var.set(char)
            elif current_computed_text:
                self.computed_display.set(current_computed_text + char)

    def get_frame(self):
        return self.frame