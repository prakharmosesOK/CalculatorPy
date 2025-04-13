from tkinter import Tk, PhotoImage
from ui import CalculatorUI

# Creating the window
root = Tk()
app = CalculatorUI(root)

# Adding title
root.title("Calculator")

# Adding icon
icon_image = PhotoImage(file="assets/logo.png")
root.iconphoto(False, icon_image)

# Adding size
root.geometry("450x550")
root.resizable(False, False)

# Adding background color
root.config(bg="#141310")

# Run application
root.mainloop()