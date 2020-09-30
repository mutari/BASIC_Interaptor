import wx

class Display:

    def __init__(self, width, height):
        window=Tk()
        # add widgets here

        window.title('Hello Python')
        window.geometry("300x200+10+20")
        window.mainloop()