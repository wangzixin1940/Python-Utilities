import ttkbootstrap as ttk
import os
import subprocess
import easygui
import logging
import datetime
import threading

os.chdir(os.path.dirname(__file__))

logging.basicConfig(
                filename=f"../../logs/{datetime.date.today()}.log",
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("PACMAN")

def main():
    def dispose(state):
        if state == "Install":
            install_thread = threading.Thread(target=pacman.install, args=(pname.get(),))
            progressbar.start()
            logger.info(install_thread.start())
            install_thread.join()
            progressbar.stop()
        elif state == "Uninstall":
            uninstall_thread = threading.Thread(target=pacman.uninstall, args=(pname.get(),))
            progressbar.start()
            logger.info(uninstall_thread.start())
            uninstall_thread.join()
            progressbar.stop()
        elif state == "Update":
            update_thread = threading.Thread(target=pacman.update, args=(pname.get(),))
            progressbar.start()
            logger.info(update_thread.start())
            update_thread.join()
            progressbar.stop()
        elif state == "List":
            list_thread = threading.Thread(target=pacman.list, args=())
            progressbar.start()
            logger.info(list_thread.start())
            list_thread.join()
            progressbar.stop()
        elif state == "Download":
            location = easygui.diropenbox(msg="Select a folder to save the package", title="Python Package Manager")
            download_thread = threading.Thread(target=pacman.download, args=(pname.get(), location))
            progressbar.start()
            logger.info(download_thread.start())
            download_thread.join()
            progressbar.stop()
    root = ttk.Window("Python Package Manager", "cosmo", size=(500, 500))
    root.iconbitmap("../../images/icon.ico")
    root.resizable(False, False)
    label = ttk.Label(root, width=15, text="Package Name : ")
    label.grid(row=0, column=0, padx=10, pady=20)
    pname = ttk.Entry(root, width=25)
    pname.grid(row=0, column=1, padx=10, pady=20)
    # options = ["Install", "Download", "Uninstall", "List", "Update"]
    radio_parent = ttk.IntVar()
    install = ttk.Radiobutton(root, text='Install', value=0, variable=radio_parent)
    download = ttk.Radiobutton(root, text='Download', value=1, variable=radio_parent)
    uninstall = ttk.Radiobutton(root, text='Uninstall', value=2, variable=radio_parent)
    list = ttk.Radiobutton(root, text='List', value=3, variable=radio_parent)
    update = ttk.Radiobutton(root, text='Update', value=4, variable=radio_parent)
    radio_parent.set(0)
    install.grid(row=1, column=0, padx=10, pady=10)
    download.grid(row=1, column=1, padx=10, pady=10)
    uninstall.grid(row=2, column=0, padx=10, pady=10)
    list.grid(row=2, column=1, padx=10, pady=10)
    update.grid(row=3, column=0, padx=10, pady=10)
    # combo = ttk.Combobox(root, width=30, values=options)
    # combo.pack(pady=10)
    # button = ttk.Button(root, text="Submit", command=lambda: dispose(combo.get()))
    button = ttk.Button(root, text="Submit", command=lambda: dispose(radio_parent.get()))
    button.grid(row=4, column=0, columnspan=2)
    progressbar = ttk.Progressbar(root, length=200, mode="indeterminate", orient=ttk.HORIZONTAL)
    # 进度条对象
    progressbar['maximum'] = 100
    # 设置最大值为100
    progressbar['value'] = 0
    # 设置目前数值为0
    progressbar.grid(row=5, column=0, columnspan=128, padx=10, pady=10)
    root.mainloop()

class pacman():
    def install(pkgname):
        print(f"Installing {pkgname}:pip install {pkgname}")
        return subprocess.run(["pip", "install", pkgname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
    def uninstall(pkgname):
        print(f"Uninstalling {pkgname}:pip uninstall {pkgname}")
        return subprocess.run(["pip", "uninstall", pkgname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
    def update(pkgname):
        print(f"Updating {pkgname}:pip install -U {pkgname}")
        return subprocess.run(["pip", "install", "-U", pkgname], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
    def list():
        print(f"Listing :pip list")
        return subprocess.run(["pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
    def download(pkgname, location):
        print(f"Downloading {pkgname} to {location}:pip download {pkgname} -d \"{location}\"")
        return subprocess.run(["pip", "download", pkgname, "-d","\"" ,location, "\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
if __name__ == "__main__":
    main()