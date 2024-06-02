import ttkbootstrap as ttk
from decoder import Decoder
from encoder import Encoder
from tkinter import filedialog
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *
from sys import argv


class App(ttk.Window):
    def __init__(self, mode:int):
        if mode == 0:
            self.generator()
        else:
            self.decoder()
    def generator(self):
        super().__init__()
        self.title("二维码生成器")
        self.geometry("500x600")
        self.windowstyle = ttk.Style(theme='cosmo')
        self.windowstyle.configure('TLabel', font=('Helvetica', 16))
        self.windowstyle.configure('TButton', font=('Helvetica', 12), width=20)
        self.windowstyle.configure('TEntry', width=20)
        # 创建标签和输入框
        self.maintitle = ttk.Label(self, text="二维码生成器", font=('Helvetica', 24))
        self.maintitle.pack(pady=10)
        self.label = ttk.Label(self, text="请输入文本：")
        self.label.pack(pady=10)
        self.entry = ttk.Entry(self)
        self.entry.pack()
        # 创建生成按钮
        self.params = ttk.Label(self, text="设置：")
        self.params.pack(pady=10)
        self.drawerLabel = ttk.Label(self, text="绘制样式：")
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
        self.imageLabel = ttk.Label(self, text="设置图片路径（可选）：")
        self.image = ttk.Entry(self)
        self.image.pack(pady=5)
        # 设置区域
        self.button = ttk.Button(self, text="生成二维码", command=self.generate_qrcode)
        self.button.pack(pady=10)
        # 创建显示二维码的标签
        self.mainloop()
    def generate_qrcode(self):
        # 获取输入的文本
        text = self.entry.get()
        # 获取设置的参数
        drawer = self.drawer.get()
        colormask = self.colormask.get()
        image = self.image.get()
        # 创建二维码
        qr = Encoder()
        fname = filedialog.asksaveasfilename(title="保存图片", filetypes=(("PNG 文件", "*.png"), ("所有文件", "*.*")), defaultextension=".png")
        qr.generateQRcode(text, fname, eval(drawer+"()"), eval(colormask+"()"), image)
    def decoder(self):
        super().__init__()
        self.title("二维码解码器")
        self.geometry("500x600")
        self.windowstyle = ttk.Style(theme='cosmo')
        self.windowstyle.configure('TLabel', font=('Helvetica', 16))
        self.windowstyle.configure('TButton', font=('Helvetica', 12), width=20)
        self.windowstyle.configure('TEntry', width=20)
        # 创建标签和输入框
        self.maintitle = ttk.Label(self, text="二维码解码器", font=('Helvetica', 24))
        self.maintitle.pack(pady=10)
        self.label = ttk.Label(self, text="请输入图片路径：")
        self.label.pack(pady=10)
        self.entry = ttk.Entry(self)
        self.entry.pack()
        # 创建解码按钮
        self.button = ttk.Button(self, text="解码", command=self.decode_qrcode)
        self.button.pack(pady=10)
        # 创建显示二维码的标签
        self.content = ttk.ScrolledText(self)
        self.content.configure(state='disabled')
        self.content.pack(pady=10)
        # 运行
        self.mainloop()
    def decode_qrcode(self):
        # 获取输入的文本
        image = self.entry.get()
        # 解码二维码
        decoder = Decoder()
        content = decoder.decodeQRcode(image)
        self.content.config(state='normal')
        # 清空解码结果
        self.content.delete("1.0", ttk.END)
        # 显示解码结果
        self.content.insert(ttk.END, content)
        self.content.config(state='disabled')


if __name__ == "__main__":
    App(int(argv[1]))

