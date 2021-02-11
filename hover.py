import tkinter as tk
class Hover(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget):
        self.widget = widget
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        self.widget.config(bg='#c28e1a')
    def close(self, event=None):
        self.widget.config(bg='#ecb22e')
             