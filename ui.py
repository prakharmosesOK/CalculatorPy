import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math

from modes.standard import StandardCalculator

# Constants
CALCULATOR_MODES = ["Standard", "Scientific", "Graphing", "Programmer", "Date_Calculation"]
CONVERTER_MODES = ["Length", "Weight", "Temperature", "Area", "Volume", "Speed", "Time", "Data_Storage"]
BUTTON_BG = "#141310"
BUTTON_ACTIVE_BG = "#3d3a30"

class CalculatorUI:
    def __init__(self, root):
        self.root = root

        # List of modes
        self.modes_list = {
            "Standard": StandardCalculator(root),
            # "Scientific": ScientificCalculator(root),
            # "Graphing": GraphingCalculator(root),
            # "Programmer": ProgrammerCalculator(root),
            # "Date_Calculation": DateCalculator(root),
            # "Length": LengthConverter(root),
            # "Weight": WeightConverter(root),
            # "Temperature": TemperatureConverter(root),
            # "Area": AreaConverter(root),
            # "Volume": VolumeConverter(root),
            # "Speed": SpeedConverter(root),
            # "Time": TimeConverter(root),
            # "Data_Storage": DataStorageConverter(root)
        }

        # Generate icons
        self.hamburger_icon = self.create_hamburger_icon()
        self.clock_icon = self.create_clock_icon()

        # Frame to hold everything
        mode_frame = tk.Frame(root, bg=BUTTON_BG)
        mode_frame.pack(fill="x", padx=10, pady=10)

        # Configure grid layout (3 columns)
        mode_frame.columnconfigure(0, weight=1)  # Left part
        mode_frame.columnconfigure(1, weight=0)  # Middle label
        mode_frame.columnconfigure(2, weight=1)  # Right part

        # Left: Mode Button + Label (inside another sub-frame)
        left_subframe = tk.Frame(mode_frame, bg=BUTTON_BG)
        left_subframe.grid(row=0, column=0, sticky="w")

        self.mode_var = tk.StringVar(value="Standard")  # Default mode
        self.mode_button = tk.Button(left_subframe,
                                    image=self.hamburger_icon,
                                    command=self.show_mode_menu,
                                    bd=0,
                                    bg=BUTTON_BG,
                                    activebackground=BUTTON_ACTIVE_BG,
                                    justify="center",
                                    cursor="hand2")
        self.mode_button.pack(side="left")

        self.mode_label = tk.Label(left_subframe,
                                text=self.mode_var.get(),
                                font=("Arial", 12),
                                bg=BUTTON_BG,
                                fg="white")
        self.mode_label.pack(side="left", padx=5)

        # Right: History Button
        self.history_button = tk.Button(mode_frame,
                                        image=self.clock_icon,
                                        command=lambda: print("History button clicked!"),
                                        bd=0,
                                        bg=BUTTON_BG,
                                        activebackground=BUTTON_ACTIVE_BG,
                                        justify="center",
                                        cursor="hand2")
        self.history_button.grid(row=0, column=2, sticky="e", padx=5)

        # Create a menu (hidden initially)
        self.mode_menu = tk.Menu(root,
                                 tearoff=0,
                                 bg="#2b2b29",
                                 fg="white",
                                 activebackground=BUTTON_ACTIVE_BG,
                                 activeforeground="white",
                                 bd=0,
                                 activeborderwidth=0,
                                 relief="groove"
                                )
        
        # Grouped Modes
        self.mode_menu.add_command(label="CALCULATOR", state="disabled", font=("Arial", 10, "bold"))
        for mode in CALCULATOR_MODES:
            self.mode_menu.add_command(label=mode, command=lambda m=mode: self.change_mode(m))

        self.mode_menu.add_command(label="", state="disabled")

        self.mode_menu.add_command(label="CONVERTER", state="disabled", font=("Arial", 10, "bold"))
        for mode in CONVERTER_MODES:
            self.mode_menu.add_command(label=mode, command=lambda m=mode: self.change_mode(m))

        # Loading the mode
        if self.mode_var.get() in self.modes_list:
            self.current_mode_ui = self.modes_list[self.mode_var.get()]
            self.current_mode_ui.get_frame().pack(fill="both", expand=True)

    def show_mode_menu(self):
        # Show the menu at the position of the button
        x = self.mode_button.winfo_rootx()
        y = self.mode_button.winfo_rooty() + self.mode_button.winfo_height()
        self.mode_menu.post(x, y)

    def change_mode(self, selected_mode):
        self.mode_var.set(selected_mode)
        self.mode_label.config(text=selected_mode)
        self.load_mode()

    def load_mode(self):
        # Remove current mode UI
        if self.current_mode_ui:
            self.current_mode_ui.get_frame().pack_forget()

        selected_mode = self.mode_var.get()

        # Load and display new one
        if selected_mode in self.modes_list:
            self.current_mode_ui = self.modes_list[selected_mode]
            self.current_mode_ui.get_frame().pack(fill="both", expand=True)

    def create_hamburger_icon(self):
        """Creates a simple hamburger menu icon using Pillow."""
        size = (30, 25)  # Image size
        img = Image.new("RGBA", size, (255, 255, 255, 0))  # Transparent background
        draw = ImageDraw.Draw(img)

        # Line properties
        line_width = 2
        spacing = 3
        color = "white"

        # Draw three horizontal lines
        for i in range(3):
            y = 5 + i * spacing * 2
            draw.line([(5, y), (22, y)], fill=color, width=line_width)

        return ImageTk.PhotoImage(img)
    
    def create_clock_icon(self):
        # Create image (25x25 with transparent background)
        size = (30, 25)
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Drawing parameters
        line_color = "white"
        line_width = 2

        # Arc for the circular arrow (clock rim)
        # Coordinates are in (left, top, right, bottom) format
        bbox = [2, 2, 23, 23]  # Defines the bounding box of the circle
        draw.arc(bbox, start=225, end=495, fill=line_color, width=line_width)

        # Clock center point
        center = (13, 12)

        # Clock hands
        draw.line([center, (12, 6)], fill=line_color, width=1)     # Hour hand (vertical)
        draw.line([center, (17, 13)], fill=line_color, width=1)    # Minute hand (angled)

        # Arrowhead at the end of arc (bottom-left side)
        arrow_tip = (3, 15)
        left = (3, 22)
        right = (8, 17.5)
        draw.polygon([arrow_tip, left, right], fill=line_color)

        return ImageTk.PhotoImage(image)