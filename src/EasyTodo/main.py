import json
import tkinter as tk

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import Listbox
from tkinter import END as tk_END

import warnings
import os

os.chdir(os.path.dirname(__file__))
# Change the working directory to the current file's directory

with open("../../data/settings.json", "r") as settings:
    settings = settings.read()
    settings = json.loads(settings)
    # Read the settings file

with open("../../" + settings["language"], "r", encoding="utf-8") as ui_src_file:
    ui_src_file = ui_src_file.read()
    file_types = json.loads(ui_src_file)["filetypes"]  # type: dict[str: list[str]]
    ui = json.loads(ui_src_file)["externals"]["easyToDo"]  # type: dict[str: str]
    ui_src = json.loads(ui_src_file)  # type: dict[str: dict]

with open("data/todo_list.json", "r", encoding="utf-8") as f:
    todo = json.loads(f.read())  # type: dict["todos": list[str]]


class Todo_Operation:
    """Manipulate the class of to-dos"""
    def __init__(self):
        self.todo_list = todo["todos"]  # type: list[str]

    class Todo_Exception(Exception):
        """
        An exception occurred in the to-do system
        Args:
            text: str: Exception information
        Examples:
            KeyError("3")，ValueError("invalid literal for int() with base 10: 'q'")
        """
        def __init__(self, text: str):
            super().__init__()
            self.text = text

        def __str__(self):
            return self.text

    def add(self, text: str):
        """
        Add to-do
        Args:
            text: text of the to-do
        """
        self.todo_list.append(text)
        data = {"todos": self.todo_list}
        with open("data/todo_list.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def remove(self, number: int):
        """
        Remove an item from the to-do list
        Args:
            number: sequence number

        Raises:
            Todo_Exception: The sequence number does not exist to throw KeyError
        """
        try:
            del self.todo_list[number]
            data = {"todos": self.todo_list}
            with open("data/todo_list.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
        except KeyError as err:  # The sequence number does not exist to throw KeyError
            raise self.Todo_Exception(repr(err))

    def view(self):
        """
        View the to-do list
        Returns:
            list: To-do list

        Raises:
            Todo_Exception: Everything that can happen is abnormal
        """
        try:
            return list(self.todo_list)
        except Exception as err:
            raise self.Todo_Exception(repr(err))

    def modify(self, new: str, number: int):
        """
        Modify an item in the to-do list
        Args:
            new: str: New content
            number: int: sequence number

        Raises:
            Todo_Exception: Any errors that may occur
        """
        try:
            self.todo_list[number] = new
            data = {"todos": self.todo_list}
            with open("data/todo_list.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
        except Exception as err:
            raise self.Todo_Exception(repr(err))


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(ui["title"])
        self.geometry("1230x850")
        self.resizable(True, True)
        self.iconbitmap("assets/favicon.ico")
        self.style_set = ttk.Style("cosmo")
        self.style_set.configure("TButton", font=("Airal", 10, "normal"))
        self.TodoOperation = Todo_Operation()
        # Method definition
        self.todo_list_frame = ttk.Frame(self)
        self.todo_list_frame.grid(column=0, row=0, sticky="nsew")
        # A frame used to hold a to-do list
        self.logo_pic = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((300, 150)))
        self.logo_label = ttk.Label(self.todo_list_frame, image=self.logo_pic)
        self.logo_label.grid(columnspan=2, row=0)
        # Logo
        self.todo_list_view = Listbox(self.todo_list_frame, height=28, width=30)
        self.todo_list_view.grid(columnspan=2, rowspan=3)
        # To-do list view
        self.add_todo = ttk.Button(self.todo_list_frame, text=ui["add"], command=self.add_todo, width=15, bootstyle="success-outline")
        self.add_todo.grid(columnspan=2, row=5)
        # Add a to-do button
        self.todo_view_frame = ttk.LabelFrame(self, text=ui["content"])
        self.todo_view_frame.grid(column=1, row=0, sticky="nsew")
        # A frame used to hold to-do content
        self.todo_view = ttk.ScrolledText(self.todo_view_frame, height=35, width=75, state="disabled")
        self.todo_view.grid(columnspan=2, row=0)
        # To-do content view
        self.remove_button = ttk.Button(self.todo_view_frame, text=ui["delete"], width=15, bootstyle="danger-outline", command=self.remove_todo)
        self.remove_button.grid(column=0, row=1)
        # Delete the To-Do button
        self.change_button = ttk.Button(self.todo_view_frame, text=ui["modify"], width=15, bootstyle="primary-outline", command=self.change_todo)
        self.change_button.grid(column=1, row=1)
        # Modify the To-Do button
        self.bind("<<ListboxSelect>>", self.selection_changed)
        # Binding events
        self.initialize()
        self.mainloop()

    def initialize(self):
        todo_list = self.TodoOperation.view()
        self.todo_list_view.delete(0, tk_END)
        for i in range(len(todo_list)):
            self.todo_list_view.insert(i, todo_list[i])
        self.todo_list_view.selection_set(0)

    def add_todo(self):
        def add():
            self.TodoOperation.add(input_text.get("1.0", "end").strip())
            self.initialize()
            input_tk.destroy()
        input_tk = ttk.Window(title=ui["inputs"]["addMessage"], themename="cosmo")
        input_tk.geometry("500x500")
        input_tk.resizable(False, False)
        input_tk.iconbitmap("assets/add.ico")
        input_tk.wm_attributes("-toolwindow", True)
        input_tk.wm_attributes("-topmost", True)
        # Create an input form
        main_title = ttk.Label(input_tk, text=ui["inputs"]["addMessage"], font=("Airal", 12))
        main_title.configure(background="#FFFFFF")
        main_title.grid(row=0, columnspan=2)
        # Title
        input_text = ttk.ScrolledText(input_tk, state="normal", width=40, height=20)
        input_text.grid(rowspan=2, columnspan=2)
        # Entry
        add_button = ttk.Button(input_tk, text=ui["inputs"]["confirm"], width=10, bootstyle="success-outline", command=add)
        remove_button = ttk.Button(input_tk, text=ui["inputs"]["cancel"], width=10, bootstyle="danger_outline", command=input_tk.destroy)
        add_button.grid(row=3, column=0)
        remove_button.grid(row=3, column=1)
        input_tk.mainloop()

    def remove_todo(self):
        index = self.listbox_selection_get()  # Get the selection
        self.TodoOperation.remove(index)
        self.initialize()

    def change_todo(self):
        def change():
            self.TodoOperation.modify(input_text.get("1.0", "end-1c"), self.listbox_selection_get())
            self.initialize()
            input_tk.destroy()
        input_tk = ttk.Window(title=ui["inputs"]["modifyMessage"], themename="cosmo")
        input_tk.geometry("500x500")
        input_tk.resizable(False, False)
        input_tk.iconbitmap("assets/modify.ico")
        input_tk.wm_attributes("-toolwindow", True)
        input_tk.wm_attributes("-topmost", True)
        # Create an input form
        main_title = ttk.Label(input_tk, text=ui["inputs"]["modifyMessage"], font=("Airal", 12))
        main_title.configure(background="#FFFFFF")
        main_title.grid(row=0, columnspan=2)
        # Title
        input_text = ttk.ScrolledText(input_tk, state="normal", width=40, height=20)
        input_text.grid(rowspan=2, columnspan=2)
        # Entry
        modify_button = ttk.Button(input_tk, text=ui["inputs"]["confirm"], width=10, bootstyle="success-outline", command=change)
        cancel_button = ttk.Button(input_tk, text=ui["inputs"]["cancel"], width=10, bootstyle="danger_outline", command=input_tk.destroy)
        modify_button.grid(row=3, column=0)
        cancel_button.grid(row=3, column=1)
        input_tk.mainloop()

    def selection_changed(self, event):
        try:
            self.todo_view.configure(state="normal")
            self.todo_view.delete(1.0, ttk.END)
            self.todo_view.insert(1.0, self.TodoOperation.todo_list[self.listbox_selection_get()])
            self.todo_view.configure(state="disabled")
        except TypeError:
            pass
        return event

    def listbox_selection_get(self):
        try:
            if (self.TodoOperation.todo_list.index(
                    self.todo_list_view.selection_get())):
                return self.TodoOperation.todo_list.index(
                    self.todo_list_view.selection_get())
            return 0
        except tk.TclError as err:
            warnings.warn(repr(err), Warning)


if __name__ == "__main__":
    App()
