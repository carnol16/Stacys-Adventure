# openPicture_subprocess.py
# NOTE: tkinter imports are deferred to __main__ so this file is safe to
# import/bundle without tkinter present (the pygame build never runs this
# script directly — openPicture.openIMG is patched by pygame_terminal).
import sys


def openIMG(path):
    import tkinter as tk
    from PIL import Image, ImageTk

    root = tk.Tk()
    root.title("Current Location")

    pil = Image.open(path)
    tkimg = ImageTk.PhotoImage(pil)
    pil.close()  # Close PIL image to free memory

    label = tk.Label(root, image=tkimg)
    label.image = tkimg
    label.pack()

    root.mainloop()


if __name__ == "__main__":
    openIMG(sys.argv[1])

    
    


