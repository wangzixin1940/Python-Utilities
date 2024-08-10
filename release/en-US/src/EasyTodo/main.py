import json
import tkinter as tk

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import Listbox
from tkinter import END as tk_END

import warnings
import os

os.chdir(os.path.dirname(__file__))
# Change the current working directory to the directory of the script


with open("data/todo_list.json", "r", encoding="utf-8") as f:
    todo = json.loads(f.read())  # type: dict["todos": list[str]]


class Todo_Operation:
    """操作待办事项的类"""
    def __init__(self):
        self.todo_list = todo["todos"]  # type: list[str]

    class Todo_Exception(Exception):
        """
        待办系统里发生的异常
        Args:
            text: str: 异常信息:
                格式为: <Exception>(<Error_Message>)，
                例如：KeyError("3")，ValueError("invalid literal for int() with base 10: 'q'")
        """
        def __init__(self, text: str):
            super().__init__()
            self.text = text

        def __str__(self):
            return self.text

    def add(self, text: str):
        """
        添加待办事项
        Args:
            text: 文本
        """
        self.todo_list.append(text)
        data = {"todos": self.todo_list}
        with open("data/todo_list.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def remove(self, number: int):
        """
        移除待办列表里的某个项
        Args:
            number: 序号

        Raises:
            Todo_Exception: 序号不存在引发Key Error
        """
        try:
            del self.todo_list[number]
            data = {"todos": self.todo_list}
            with open("data/todo_list.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
        except KeyError as err:  # 序号不存在引发Key Error
            raise self.Todo_Exception(repr(err))

    def view(self):
        """
        查看待办列表
        Returns:
            list: 待办列表

        Raises:
            Todo_Exception: 一切可能发生的异常
        """
        try:
            return list(self.todo_list)
        except Exception as err:
            raise self.Todo_Exception(repr(err))

    def modify(self, new: str, number: int):
        """
        修改待办列表里的某个项
        Args:
            new: str: 新的内容
            number: int: 序号
        Raises:
            Todo_Exception: 可能发生的任何错误
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
        self.title("Easy To Do")
        self.geometry("1230x850")
        self.resizable(True, True)
        self.iconbitmap("assets/favicon.ico")
        self.style_set = ttk.Style("cosmo")
        self.style_set.configure("TButton", font=("微软雅黑", 10, "normal"))
        self.TodoOperation = Todo_Operation()
        # 方法定义
        self.todo_list_frame = ttk.Frame(self)
        self.todo_list_frame.grid(column=0, row=0, sticky="nsew")
        # 用于盛放待办列表的 Frame
        self.logo_pic = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((300, 150)))
        self.logo_label = ttk.Label(self.todo_list_frame, image=self.logo_pic)
        self.logo_label.grid(columnspan=2, row=0)
        # Logo
        self.todo_list_view = Listbox(self.todo_list_frame, height=28, width=30)
        self.todo_list_view.grid(columnspan=2, rowspan=3)
        # 待办列表
        self.add_todo = ttk.Button(self.todo_list_frame, text="+ 添加待办", command=self.add_todo, width=15, bootstyle="success-outline")
        self.add_todo.grid(columnspan=2, row=5)
        # 添加待办按钮
        self.todo_view_frame = ttk.LabelFrame(self, text="待办内容")
        self.todo_view_frame.grid(column=1, row=0, sticky="nsew")
        # 用于盛放待办内容的 Frame
        self.todo_view = ttk.ScrolledText(self.todo_view_frame, height=35, width=75, state="disabled")
        self.todo_view.grid(columnspan=2, row=0)
        # 待办内容显示
        self.remove_button = ttk.Button(self.todo_view_frame, text="- 标记为完成并删除", width=15, bootstyle="danger-outline", command=self.remove_todo)
        self.remove_button.grid(column=0, row=1)
        # 删除待办按钮
        self.change_button = ttk.Button(self.todo_view_frame, text="✏️ 修改待办", width=15, bootstyle="primary-outline", command=self.change_todo)
        self.change_button.grid(column=1, row=1)
        # 修改待办按钮
        self.bind("<<ListboxSelect>>", self.selection_changed)
        # 绑定事件
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
        input_tk = ttk.Window(title="添加待办", themename="cosmo")
        input_tk.geometry("500x500")
        input_tk.resizable(False, False)
        input_tk.iconbitmap("assets/add.ico")
        input_tk.wm_attributes("-toolwindow", True)
        input_tk.wm_attributes("-topmost", True)
        # 创建输入窗体
        main_title = ttk.Label(input_tk, text="在下面添加你想添加的待办", font=("微软雅黑", 12))
        main_title.configure(background="#FFFFFF")
        main_title.grid(row=0, columnspan=2)
        # 标题
        input_text = ttk.ScrolledText(input_tk, state="normal", width=40, height=20)
        input_text.grid(rowspan=2, columnspan=2)
        # 输入框
        add_button = ttk.Button(input_tk, text="确定", width=10, bootstyle="success-outline", command=add)
        remove_button = ttk.Button(input_tk, text="取消", width=10, bootstyle="danger_outline", command=input_tk.destroy)
        add_button.grid(row=3, column=0)
        remove_button.grid(row=3, column=1)
        input_tk.mainloop()

    def remove_todo(self):
        index = self.listbox_selection_get()  # 获取所选
        self.TodoOperation.remove(index)
        self.initialize()

    def change_todo(self):
        def change():
            self.TodoOperation.modify(input_text.get("1.0", "end-1c"), self.listbox_selection_get())
            self.initialize()
            input_tk.destroy()
        input_tk = ttk.Window(title="更改待办", themename="cosmo")
        input_tk.geometry("500x500")
        input_tk.resizable(False, False)
        input_tk.iconbitmap("assets/modify.ico")
        input_tk.wm_attributes("-toolwindow", True)
        input_tk.wm_attributes("-topmost", True)
        # 创建输入窗体
        main_title = ttk.Label(input_tk, text="在下面更改", font=("微软雅黑", 12))
        main_title.configure(background="#FFFFFF")
        main_title.grid(row=0, columnspan=2)
        # 标题
        input_text = ttk.ScrolledText(input_tk, state="normal", width=40, height=20)
        input_text.grid(rowspan=2, columnspan=2)
        # 输入框
        modify_button = ttk.Button(input_tk, text="确定", width=10, bootstyle="success-outline", command=change)
        cancel_button = ttk.Button(input_tk, text="取消", width=10, bootstyle="danger_outline", command=input_tk.destroy)
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
