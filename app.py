import tkinter as tk
from controllers.main_controller import MainController

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Job Fair Registration (MVC Demo)")
    root.geometry("1000x700")
    app = MainController(root)
    app.start()
    root.mainloop()
