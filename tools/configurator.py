import json
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox as msgbox

os.chdir(os.path.dirname(__file__))
config = open("../data/theme.json")
settings = json.load(config)
config.close()

def main():
    global root
    if not(settings["theme"] == "pride"):
        root = ttk.Window(themename=settings["theme"])
    else:
        root = ttk.Window(themename="cosmo")
        root.iconbitmap("../images/pride.ico")
    root.title("Configurator")
    root.geometry("400x500")
    style = ttk.Style()
    root.resizable(False, False)
    title = ttk.Label(root, text="Configurator", font=("Arial", 20))
    title.pack(pady=10)
    button1 = ttk.Button(root, text="Button1", command=lambda: msgbox.showinfo("Button1", "Button1 被点击！"), bootstyle=(PRIMARY, OUTLINE))
    button1.pack(pady=10)
    button2 = ttk.Button(root, text="Button2", command=lambda: msgbox.showinfo("Button2", "Button2 被点击！"), bootstyle=(SUCCESS, OUTLINE))
    button2.pack(pady=10)
    info_button = ttk.Button(root, text="Info", command=lambda: msgbox.showinfo("Info Button", "一个消息！"), bootstyle=(INFO, OUTLINE))
    info_button.pack(pady=10)
    warning_button = ttk.Button(root, text="Warning", command=lambda: msgbox.showwarning("Warning Button", "一个警告！"), bootstyle=(WARNING, OUTLINE))
    warning_button.pack(pady=10)
    error_button = ttk.Button(root, text="Error", command=lambda: msgbox.showerror("Error Button", "一个错误！"), bootstyle=(DANGER, OUTLINE))
    error_button.pack(pady=10)
    # --------------------------------------- #
    themes = style.theme_names()
    themes.append("pride")
    theme_label = ttk.Label(root, text="主题：", font=("Arial", 15))
    theme_label.pack(side=LEFT)
    theme_combo = ttk.Combobox(root, values=themes, font=("Arial", 15))
    theme_combo.set(settings["theme"])
    theme_combo.pack(padx=10, side=LEFT)
    def change_theme(event):
        theme_cbo_value = theme_combo.get()
        if theme_cbo_value == "pride":
            root.iconbitmap("../images/pride.ico")
            theme_cbo_value = "cosmo"
        else :
            root.iconbitmap("../images/icon.ico")
        style.theme_use(theme_cbo_value)
        theme_combo.selection_clear()
        save_changes()
    theme_combo.bind('<<ComboboxSelected>>', change_theme)
    def save_changes():
        settings["theme"] = theme_combo.get()
        with open("../data/theme.json", "w") as f:
            json.dump(settings, f)
        print("[INFO] 主题已保存。")
    root.mainloop()

if __name__ == "__main__":
    main()
