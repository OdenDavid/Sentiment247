import tkinter as tk

class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 2
        y += self.widget.winfo_rooty() + 50
        # creates a toplevel window
        self.top = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.top.wm_overrideredirect(True)
        self.top.wm_geometry("+%d+%d" % (x, y))
        lbl = tk.Label(self.top, text=self.text, justify='left',
                        background='#ffffff', relief='solid', borderwidth=1,
                        font=("arial", "8", "normal"))
        lbl.pack(ipadx=1)
    def close(self, event=None):
        if self.top:
            self.top.destroy()        