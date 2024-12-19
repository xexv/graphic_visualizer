import tkinter as tk
from visualizer import DataVisualizer

def main():
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
