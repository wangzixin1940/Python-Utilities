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
        print((pname.get(), combo.get()))
        if state == "Install":
            install_thread = threading.Thread(target=pacman.install, args=(pname.get(),))
            logger.info(install_thread.start())
            install_thread.join()
        elif state == "Uninstall":
            uninstall_thread = threading.Thread(target=pacman.uninstall, args=(pname.get(),))
            logger.info(uninstall_thread.start())
            uninstall_thread.join()
        elif state == "Update":
            update_thread = threading.Thread(target=pacman.update, args=(pname.get(),))
            logger.info(update_thread.start())
            update_thread.join()
        elif state == "List":
            list_thread = threading.Thread(target=pacman.list, args=())
            logger.info(list_thread.start())
            list_thread.join()
        elif state == "Download":
            location = easygui.diropenbox(msg="Select a folder to save the package", title="Python Package Manager")
            download_thread = threading.Thread(target=pacman.download, args=(pname.get(), location))
            logger.info(download_thread.start())
            download_thread.join()
    root = ttk.Window("Python Package Manager", "cosmo", size=(500, 500))
    root.iconbitmap("../../images/icon.ico")
    root.resizable(False, False)
    label = ttk.Label(root, width=30, text="Package Name : ")
    label.pack(pady=10)
    pname = ttk.Entry(root, width=30)
    pname.pack(pady=10)
    options = ["Install", "Download", "Uninstall", "List", "Update"]
    combo = ttk.Combobox(root, width=30, values=options)
    combo.pack(pady=10)
    button = ttk.Button(root, text="Submit", command=lambda: dispose(combo.get()))
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
        print(f"Downloading {pkgname} to {location}:pip download {pkgname} -d {location}")
        return subprocess.run(["pip", "download", pkgname, "-d", location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="gbk")
if __name__ == "__main__":
    main()