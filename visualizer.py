import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический Визуализатор")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2d2d2d")

        self.header_label = tk.Label(root, text="Визуализатор данных", font=("Helvetica", 16),
                                     bg="#2d2d2d", fg="white")
        self.header_label.pack(pady=10)

        self.control_frame = tk.Frame(root, bg="#2d2d2d")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.format_label = tk.Label(self.control_frame, text="Формат файла:", font=("Helvetica", 10), bg="#2d2d2d",
                                     fg="white")
        self.format_label.pack(pady=5)

        self.file_format = tk.StringVar(value="CSV")
        self.format_menu = tk.OptionMenu(self.control_frame, self.file_format, "CSV", "Excel")
        self.format_menu.config(width=15, font=("Helvetica", 10))
        self.format_menu.pack(pady=5)

        self.load_button = tk.Button(self.control_frame, text="Загрузить файл", command=self.load_file, font=("Helvetica", 10),
                                     bg="#4CAF50", fg="white", width=15, height=1)
        self.load_button.pack(pady=10)

        self.x_column_label = tk.Label(self.control_frame, text="X-столбец:", font=("Helvetica", 10), bg="#2d2d2d",
                                       fg="white")
        self.x_column_label.pack(pady=5)

        self.x_column_var = tk.StringVar()
        self.x_column_menu = tk.OptionMenu(self.control_frame, self.x_column_var, [])
        self.x_column_menu.pack(pady=5)

        self.y_column_label = tk.Label(self.control_frame, text="Y-столбец:", font=("Helvetica", 10), bg="#2d2d2d",
                                       fg="white")
        self.y_column_label.pack(pady=5)

        self.y_column_var = tk.StringVar()
        self.y_column_menu = tk.OptionMenu(self.control_frame, self.y_column_var, [])
        self.y_column_menu.pack(pady=5)

        self.switch_button = tk.Button(self.control_frame, text="Поменять X и Y", command=self.switch_columns,
                                       font=("Helvetica", 10), bg="#FF9800", fg="white", width=15, height=1)
        self.switch_button.pack(pady=10)

        self.chart_type_label = tk.Label(self.control_frame, text="Тип графика:", font=("Helvetica", 10), bg="#2d2d2d",
                                         fg="white")
        self.chart_type_label.pack(pady=5)

        self.chart_type_var = tk.StringVar(value="scatter")
        self.chart_type_menu = tk.OptionMenu(self.control_frame, self.chart_type_var, "scatter", "line")
        self.chart_type_menu.pack(pady=5)

        self.visualize_button = tk.Button(self.control_frame, text="Визуализировать", command=self.visualize_data,
                                          font=("Helvetica", 10), bg="#2196F3", fg="white", width=15, height=1)
        self.visualize_button.pack(pady=20)

        self.canvas_frame = tk.Frame(root, bg="black", width=600, height=600)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.data = None

    def load_file(self):
        file_format = self.file_format.get()
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")] if file_format == "CSV" else [("Excel Files", "*.xlsx")])

        if not file_path:
            messagebox.showwarning("Внимание", "Файл не выбран!")
            return

        try:
            self.data = pd.read_csv(file_path) if file_format == "CSV" else pd.read_excel(file_path)
            self.update_column_menu()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def update_column_menu(self):
        if self.data is not None:
            columns = self.data.columns.tolist()
            self.x_column_var.set(columns[0])
            self.y_column_var.set(columns[1])

            self.x_column_menu['menu'].delete(0, 'end')
            self.y_column_menu['menu'].delete(0, 'end')

            for col in columns:
                self.x_column_menu['menu'].add_command(label=col, command=lambda value=col: self.x_column_var.set(value))
                self.y_column_menu['menu'].add_command(label=col, command=lambda value=col: self.y_column_var.set(value))

    def switch_columns(self):
        current_x, current_y = self.x_column_var.get(), self.y_column_var.get()
        self.x_column_var.set(current_y)
        self.y_column_var.set(current_x)

    def visualize_data(self):
        if self.data is None:
            messagebox.showwarning("Ошибка", "Файл не загружен!")
            return

        x_column, y_column = self.x_column_var.get(), self.y_column_var.get()

        if x_column not in self.data.columns or y_column not in self.data.columns:
            messagebox.showwarning("Ошибка", "Неверно выбраны столбцы!")
            return

        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            if self.chart_type_var.get() == "scatter":
                sns.scatterplot(data=self.data, x=x_column, y=y_column, ax=ax)
            elif self.chart_type_var.get() == "line":
                sns.lineplot(data=self.data, x=x_column, y=y_column, ax=ax)

            ax.set_title(f"{self.chart_type_var.get().capitalize()} Graph")
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {e}")
