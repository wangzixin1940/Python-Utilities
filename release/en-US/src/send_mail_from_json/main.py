from send import Send
import ttkbootstrap as ttk
from tkinter import filedialog as fdg
from tkinter import messagebox as msgbox


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title("Send Mail From JSON")
        self.geometry("400x300")
        self.resizable(False, False)
        self.style_set = ttk.Style("cosmo")
        self.style_set.configure("TButton", font=("Arial", 14), width=20)
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        self.main_title = ttk.Label(
            self, text="Send Mail From JSON", font=(
                "Arial", 20))
        self.main_title.pack(pady=10)
        self.json_file = ttk.StringVar(value="Choose File")
        self.choose_file_button = ttk.Button(
            self,
            textvariable=self.json_file,
            command=self.choose_file,
            bootstyle="primary-outline")
        self.choose_file_button.pack(pady=10)
        self.send_button = ttk.Button(
            self,
            text="Send",
            command=self.send_mail,
            bootstyle="success-outline")
        self.send_button.pack(pady=10)

    def choose_file(self):
        self.json_file.set(
            fdg.askopenfilename(
                filetypes=[
                    ("JSON Files", "*.json")]))

    def send_mail(self):
        if (self.json_file.get() != "Choose File"):
            Send(self.json_file.get())
            msgbox.showinfo("Complete", "Email sent successfully!")
        else:
            msgbox.showerror("Error", "Please choose a file!")


if __name__ == "__main__":
    App()
