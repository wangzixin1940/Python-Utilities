import ttkbootstrap as ttk
from decoder import Decoder
from encoder import Encoder
from tkinter import filedialog
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
from sys import argv
from tkinter import messagebox as msgbox


class App(ttk.Window):
    def __init__(self, mode: int):
        if mode == 0:
            self.generator()
        else:
            self.decoder()

    def generator(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("500x600")
        self.windowstyle = ttk.Style(theme='cosmo')
        self.windowstyle.configure('TLabel', font=('Helvetica', 16))
        self.windowstyle.configure('TButton', font=('Helvetica', 12), width=20)
        self.windowstyle.configure('TEntry', width=20)
        # Create labels and input boxes
        self.maintitle = ttk.Label(
            self, text="QR Code Generator", font=(
                'Helvetica', 24))
        self.maintitle.pack(pady=10)
        self.label = ttk.Label(
            self,
            text="Please enter the text you want\nto encode: ",
            font=(
                "Helvetica",
                14))
        self.label.pack(pady=10)
        self.entry = ttk.Entry(self)
        self.entry.pack()
        # Create a build button
        self.params = ttk.Label(
            self, text="Settings: ", font=(
                "Helvetica", 14, "bold"))
        self.params.pack(pady=10)
        self.drawerLabel = ttk.Label(self, text="Draw Style: ")
        self.drawerLabel.pack(pady=5)
        self.drawers = [
            "CircleModuleDrawer",
            "GappedSquareModuleDrawer",
            "HorizontalBarsDrawer",
            "RoundedModuleDrawer",
            "SquareModuleDrawer",
            "VerticalBarsDrawer"
        ]
        self.colormasks = [
            "SolidFillColorMask",
            "RadialGradiantColorMask",
            "SquareGradiantColorMask",
            "HorizontalGradiantColorMask",
            "VerticalGradiantColorMask"
        ]
        self.drawer = ttk.Combobox(self, values=self.drawers)
        self.drawer.pack(pady=5)
        self.colormask = ttk.Combobox(self, values=self.colormasks)
        self.colormask.pack(pady=5)
        self.imageLabel = ttk.Label(
            self, text="Please Enter The Image Path (Optional): ")
        self.image = ttk.Entry(self)
        self.image.pack(pady=5)
        # Set the region
        self.button = ttk.Button(
            self,
            text="Generate",
            command=self.generate_qrcode)
        self.button.pack(pady=10)
        # Create a label that displays the QR Code
        self.mainloop()

    def generate_qrcode(self):
        # Get the entered text
        text = self.entry.get()
        # Get the parameters of the settings
        drawer = self.drawer.get()
        colormask = self.colormask.get()
        image = self.image.get()
        # Create a QR Code
        qr = Encoder()
        fname = filedialog.asksaveasfilename(title="Save QR Code As", filetypes=(
            ("PNG Files", "*.png"), ("All Files", "*.*")), defaultextension=".png")
        qr.generateQRcode(
            text,
            fname,
            eval(
                drawer +
                "()"),
            eval(
                colormask +
                "()"),
            image)

    def decoder(self):
        super().__init__()
        self.title("QR Code Decoder")
        self.geometry("500x600")
        self.windowstyle = ttk.Style(theme='cosmo')
        self.windowstyle.configure('TLabel', font=('Helvetica', 16))
        self.windowstyle.configure('TButton', font=('Helvetica', 12), width=20)
        self.windowstyle.configure('TEntry', width=20)
        # Create labels and input boxes
        self.maintitle = ttk.Label(
            self, text="QR Code Decoder", font=(
                'Helvetica', 24))
        self.maintitle.pack(pady=10)
        self.label = ttk.Label(
            self, text="Please enter the\nimage path (Optional): ")
        self.label.pack(pady=10)
        self.entry = ttk.Entry(self)
        self.entry.pack()
        # Create a decode button
        self.button = ttk.Button(
            self, text="Decode", command=self.decode_qrcode)
        self.button.pack(pady=10)
        # Create a label that displays the qr code
        self.content = ttk.ScrolledText(self)
        self.content.configure(state='disabled')
        self.content.pack(pady=10)
        # Run
        self.mainloop()

    def decode_qrcode(self):
        # Get the entered text
        image = self.entry.get()
        # Decode the QR Code
        decoder = Decoder()
        content = decoder.decodeQRcode(image)
        self.content.config(state='normal')
        # Clear the decoding result
        self.content.delete("1.0", ttk.END)
        # Displays the decoding result
        self.content.insert(ttk.END, content)
        self.content.config(state='disabled')


if __name__ == "__main__":
    try:
        App(int(argv[1]))
    except IndexError:
        msgbox.showerror("Error", "Please enter the mode (1 or 2)")
