import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from Extensions import loading, tooltip, hover
import threading

from Extensions import twitter
import validators
import socket

from Extensions import ocr, preprocess, PolarityScore
import pickle
#=========================Main Window=============================
class App:
    def __init__(self, master): 
        
        primary = '#ffffff' #181818
        foreground = '#222222' #ffffff
        gray = '#e0e0e0' #3d3d3d
        
        w = 900 # window width
        h = 650 # window height

        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen    

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2) 

        master.iconbitmap("images/logo_img.ico")
        self.master = master
        self.master.title("Sentiment247")
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master.configure(background=primary)
        self.master.resizable(False,False)

        """def getstarted(event=None):
            for widget in self.master.winfo_children():
                widget.destroy()
            def continue_():"""
            
        #=============Top Frame========================
        self.top_frame = tk.Frame(self.master,width=823,height=80,bg=primary,relief='flat',bd=0)
        self.top_frame.place(relx=0.078,rely=0)
        #=============Main Frame=======================
        self.main_frame = tk.Frame(self.master,width=820,height=570,bg=gray)
        self.main_frame.place(relx=0.085,rely=0.12)
        #===============Navigation Frame===============
        self.nav_frame = tk.Frame(self.master,bg=primary,width=80,height=650,relief='groove',bd=2)
        self.nav_frame.place(relx=0,rely=0)

        self.lbl = tk.Label(self.nav_frame,bg=primary,text='___________',fg=gray)
        self.lbl.place(relx=0.07,rely=0.09)
        self.logo = tk.PhotoImage(file='images/logo_img.png')
        self.logo_lbl = tk.Label(self.nav_frame,bg=primary,image=self.logo)
        self.logo_lbl.place(relx=0,rely=0,width=73,height=70)
        self.nav_btn = tk.PhotoImage(file='images/nav_btn.png')
        self.logo_lbl = tk.Label(self.nav_frame,bg=primary,image=self.nav_btn)
        self.logo_lbl.place(relx=0,rely=0.157)
        
        def is_connected():
            try:
                # connects to the host and tells us if the host is actually reachable
                socket.create_connection(("1.1.1.1", 53))
                return True
            except OSError:
                pass
            return False

        def polarity_widgets(content):
            for w in self.main_frame.winfo_children():
                w.destroy()
            # Text Widget
            self.text_box = tk.Text(self.main_frame,font=('normal',10),bg=primary,fg=foreground,relief='groove',bd=1)
            self.text_box.place(relx=0.17,rely=0.07,width=520,height=200)
            self.text_box.insert(tk.END,content)
            def submit():
                content = self.text_box.get("1.0",'end-1c') # The content of the text box
                if content == "":
                    messagebox.showerror("Entry error","You can not perform sentiment analysis on an empty text box")
                elif type(content) == int:
                    messagebox.showerror("Entry error","You can not perform sentiment analysis on a number")
                else:
                    polarity_scorer(content)
            # Submit Button
            self.submit = tk.Button(self.main_frame,text='Submit',bg='#ecb22e',fg=primary,font=('normal',8,'bold'),bd=0,command=submit)
            self.submit.place(relx=0.685,rely=0.45,width=100,height=30)
            hover.Hover(self.submit)
            #========Positive Frame======
            self.pos_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
            self.pos_frame.place(relx=0.17,rely=0.65)
            # Positive Image
            self.happy_img = tk.PhotoImage(file='images/happy.png')
            self.happy_lbl = tk.Label(self.pos_frame,bg=primary,image=self.happy_img)
            self.happy_lbl.place(relx=0.26,rely=0.05)
            # Positive Label
            self.positive_lbl = tk.Label(self.pos_frame,text='Positive',font=('normal',9,'bold'),fg='#008000',bg='#9de19d')
            self.positive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
            # Positive Percentage
            self.positive_per = tk.Label(self.pos_frame,text='0%',font=('normal',10,'bold'),bg=primary,fg=foreground)
            self.positive_per.place(relx=0.43,rely=0.7)
            #========Neutral Frame========
            self.neu_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
            self.neu_frame.place(relx=0.41,rely=0.65)
            # Neutral Image
            self.neutral_img = tk.PhotoImage(file='images/neutral.png')
            self.neutral_lbl = tk.Label(self.neu_frame,bg=primary,image=self.neutral_img)
            self.neutral_lbl.place(relx=0.26,rely=0.05)
            # Neutral Label
            self.neutral_lbl = tk.Label(self.neu_frame,text='Neutral',font=('normal',9,'bold'),fg='#ffca18',bg='#fbe6a2')
            self.neutral_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
            # Neutral Percentage
            self.neutral_per = tk.Label(self.neu_frame,text='0%',font=('normal',10,'bold'),bg=primary,fg=foreground)
            self.neutral_per.place(relx=0.43,rely=0.7)
            #========Negative Frame======
            self.neg_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
            self.neg_frame.place(relx=0.64,rely=0.65)
            # Negative Image
            self.negative_img = tk.PhotoImage(file='images/sad.png')
            self.negative_lbl = tk.Label(self.neg_frame,bg=primary,image=self.negative_img)
            self.negative_lbl.place(relx=0.26,rely=0.05)
            # Negative Label
            self.negative_lbl = tk.Label(self.neg_frame,text='Negative',font=('normal',9,'bold'),fg='#ec1c24',bg='#f6a4a8')
            self.negative_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
            # Negative Percentage
            self.negative_per = tk.Label(self.neg_frame,text='0%',font=('normal',10,'bold'),bg=primary,fg=foreground)
            self.negative_per.place(relx=0.43,rely=0.7)

            # Disable Frame Content By Defalult
            for w in self.pos_frame.winfo_children(): # Positive Frame
                w.configure(state=tk.DISABLED)
            for w in self.neu_frame.winfo_children(): # Neutral Frame
                w.configure(state=tk.DISABLED)
            for w in self.neg_frame.winfo_children(): # Negative Frame
                w.configure(state=tk.DISABLED)                 
                
        def depressive_widgets(content):
            # Remove every widget that stands in your way
            for w in self.main_frame.winfo_children():
                w.destroy()
            # Text Widget
            self.text_box = tk.Text(self.main_frame,font=('normal',10),bg=primary,fg=foreground,relief='groove',bd=1)
            self.text_box.place(relx=0.17,rely=0.07,width=520,height=200)
            self.text_box.insert(tk.END,content)
            
            def submit():
                content = self.text_box.get("1.0",'end-1c') # The content of the text box
                if content == "":
                    messagebox.showerror("Entry error","You can not perform sentiment analysis on an empty text box")
                elif type(content) == int:
                    messagebox.showerror("Entry error","You can not perform sentiment analysis on a number")
                else:
                    for w in self.main_frame.winfo_children():
                        w.place_forget()
                    # Label for the loader gif
                    load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                    load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                    
                    def clean():
                        processed = preprocess.CleanMessage(content)
                        if processed != "":
                            load_lbl.unload()
                            load_lbl.place_forget()
                            depressive_scorer(processed)                               
                        else:
                            pass                            
                    def load():
                        load_lbl.load('images/load.gif')
                    threading.Thread(target=clean).start()
                    threading.Thread(target=load).start() 
            # Submit Button
            self.submit = tk.Button(self.main_frame,text='Submit',bg='#ecb22e',fg=primary,font=('normal',8,'bold'),bd=0,command=submit)
            self.submit.place(relx=0.682,rely=0.45,width=100,height=30)
            hover.Hover(self.submit)
            #========Positive Frame======
            self.pos_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
            self.pos_frame.place(relx=0.28,rely=0.65)
            # Positive Image
            self.happy_img = tk.PhotoImage(file='images/happy.png')
            self.happy_lbl = tk.Label(self.pos_frame,bg=primary,image=self.happy_img)
            self.happy_lbl.place(relx=0.26,rely=0.05)
            # Positive Label
            self.positive_lbl = tk.Label(self.pos_frame,text='Positive',font=('normal',9,'bold'),fg='#008000',bg='#9de19d')
            self.positive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
            # Positive Percentage
            self.positive_per = tk.Label(self.pos_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
            self.positive_per.place(relx=0.415,rely=0.7)
            #========Depressive Frame======
            self.dep_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
            self.dep_frame.place(relx=0.53,rely=0.65)
            # Depressive Image
            self.depressive_img = tk.PhotoImage(file='images/sad.png')
            self.depressive_lbl = tk.Label(self.dep_frame,bg=primary,image=self.depressive_img)
            self.depressive_lbl.place(relx=0.26,rely=0.05)
            # Depressive Label
            self.depressive_lbl = tk.Label(self.dep_frame,text='Depressive',font=('normal',9,'bold'),fg='#ec1c24',bg='#f6a4a8')
            self.depressive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
            # Depressive Percentage
            self.depressive_per = tk.Label(self.dep_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
            self.depressive_per.place(relx=0.415,rely=0.7)
        
            # Disable Frame Content By Defalult
            for w in self.pos_frame.winfo_children(): # Positive Frame
                w.configure(state=tk.DISABLED)
            for w in self.dep_frame.winfo_children(): # Depressive Frame
                w.configure(state=tk.DISABLED) 

        def polarity_scorer(content):
            """This Function is will assign polaity scores to thier
            respective labels and configuring size of frames when scores are calculated"""
            
            result = PolarityScore.sentiment(content) # A dictionary of sentiment scores
            
            values = list(result.values()) # Create a list of values(scores)
            # Create a new dictionary and convert the decimal values to percentage values 
            new_dict = {'negative':int(values[0]*100),
                        'neutral':int(values[1]*100),
                        'positive':int(values[2]*100)}
            
            # Enable the Frames
            for w in self.pos_frame.winfo_children(): # Positive Frame
                w.configure(state=tk.NORMAL)
            for w in self.neu_frame.winfo_children(): # Neutral Frame
                w.configure(state=tk.NORMAL)
            for w in self.neg_frame.winfo_children(): # Negative Frame
                w.configure(state=tk.NORMAL)

            new_values = list(new_dict.values()) # Create a new list of values(scores)
            self.negative_per.configure(text=str(new_values[0])+'%') # Configure the negative value
            self.neutral_per.configure(text=str(new_values[1])+'%') # Configure the neutral value
            self.positive_per.configure(text=str(new_values[2])+'%') # Configure the positive value

            max_value = max(new_values) # Get the maximum value from the list
            max_index = new_values.index(max_value) # Get the index of the highest value in the list
            if max_index == 0: # If the maximum value is the negative
                self.neg_frame.configure(width=150,height=190)
                self.neu_frame.configure(width=130,height=170)
                self.pos_frame.configure(width=130,height=170)
                for w in self.pos_frame.winfo_children(): # Positive Frame
                    w.configure(state=tk.DISABLED)
                for w in self.neu_frame.winfo_children(): # Neutral Frame
                    w.configure(state=tk.DISABLED)
            elif max_index == 1: # If the maximum value is the neutral
                self.neu_frame.configure(width=150,height=190)
                self.neg_frame.configure(width=130,height=170)
                self.pos_frame.configure(width=130,height=170)
                for w in self.pos_frame.winfo_children(): # Positive Frame
                    w.configure(state=tk.DISABLED)
                for w in self.neg_frame.winfo_children(): # Negative Frame
                    w.configure(state=tk.DISABLED)
            elif max_index == 2: # If the maximum value is the positive
                self.pos_frame.configure(width=150,height=190)
                self.neg_frame.configure(width=130,height=170)
                self.neu_frame.configure(width=130,height=170)
                for w in self.neg_frame.winfo_children(): # Negative Frame
                    w.configure(state=tk.DISABLED)
                for w in self.neu_frame.winfo_children(): # Neutral Frame
                    w.configure(state=tk.DISABLED)
        
        def depressive_scorer(content):

            vectorizer = pickle.load(open('vectorizer.pickle','rb'))
            model = pickle.load(open('classifier.pickle','rb'))
            pred = model.predict_proba(vectorizer.transform([content]))[0]

            # Create a new dictionary and convert the decimal values to percentage values 
            new_dict = {'positive':round(pred[0]*100),
                        'depressive':round(pred[1]*100)}

            # Enable Frames
            self.text_box.place(relx=0.17,rely=0.07,width=520,height=200)
            self.submit.place(relx=0.682,rely=0.45,width=100,height=30)
            self.clear.place(relx=0.547,rely=0.45,width=100,height=30)
            self.pos_frame.place(relx=0.28,rely=0.65)
            self.dep_frame.place(relx=0.53,rely=0.65)
            
            for w in self.pos_frame.winfo_children(): # Positive Frame
                w.configure(state=tk.NORMAL)
            for w in self.dep_frame.winfo_children(): # Depressive Frame
                w.configure(state=tk.NORMAL)
                
            new_values = list(new_dict.values()) # Create a new list of values(scores)
            self.positive_per.configure(text=str(new_values[0])+'%') # Configure the positive value
            self.depressive_per.configure(text=str(new_values[1])+'%') # Configure the depressive value

            max_value = max(new_values) # Get the maximum value from the list
            max_index = new_values.index(max_value) # Get the index of the highest value in the list
            if max_index == 0: # If the maximum value is the positive
                self.dep_frame.configure(width=130,height=170)
                self.pos_frame.configure(width=150,height=190)
                for w in self.dep_frame.winfo_children(): # Depressive Frame
                    w.configure(state=tk.DISABLED)
            elif max_index == 1: # If the maximum value is the depressive
                self.dep_frame.configure(width=150,height=190)
                self.pos_frame.configure(width=130,height=170)
                for w in self.pos_frame.winfo_children(): # Depressive Frame
                    w.configure(state=tk.DISABLED)

        def text():
            # Configure Colour
            self.text_btn.configure(bg=gray)
            self.doc_btn.configure(bg=primary)
            self.voice_btn.configure(bg=primary)
            self.link_btn.configure(bg=primary)
            # Configure Position
            self.text_btn.place_configure(relx=0.13)
            self.doc_btn.place_configure(relx=0.10)
            self.voice_btn.place_configure(relx=0.10)
            self.link_btn.place_configure(relx=0.10)
            self.logo_lbl.place_configure(relx=0,rely=0.157)
            # Remove every widget that stands in your way
            for w in self.main_frame.winfo_children():
                w.destroy()
            for w in self.top_frame.winfo_children():
                w.destroy()
                
            #=============Polarity and Depression functions===========
            def polarity():
                self.btn_lbl.place(relx=0,rely=0.87)
                self.pol_btn.configure(fg=foreground)
                self.dep_btn.configure(fg=gray)
                # Remove every widget that stands in your way
                for w in self.main_frame.winfo_children():
                    w.destroy()
                # Text Widget
                self.text_box = tk.Text(self.main_frame,font=('normal',10),bg=primary,fg=foreground,relief='groove',bd=1)
                self.text_box.place(relx=0.17,rely=0.07,width=520,height=200)
                # Place Holder for text widget
                self.text_box.insert(tk.END,'Type something here...')
                self.text_box.bind("<FocusIn>", lambda args: self.text_box.delete("1.0",tk.END))

                def submit():
                    content = self.text_box.get("1.0",'end-1c') # The content of the text box
                    if content == "":
                        messagebox.showerror("Entry error","You can not perform sentiment analysis on an empty text box")
                    elif type(content) == int:
                        messagebox.showerror("Entry error","You can not perform sentiment analysis on a number")
                    else:
                        polarity_scorer(content)
                # Submit Button
                self.submit = tk.Button(self.main_frame,text='Submit',bg='#ecb22e',fg=primary,font=('normal',8,'bold'),bd=0,command=submit)
                self.submit.place(relx=0.682,rely=0.45,width=100,height=30)
                hover.Hover(self.submit)
                # Clear Button
                self.clear = tk.Button(self.main_frame,text='Clear',bg='#eed8a6',fg=primary,font=('normal',8,'bold'),bd=0,command=polarity)
                self.clear.place(relx=0.547,rely=0.45,width=100,height=30)
                #========Positive Frame======
                self.pos_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
                self.pos_frame.place(relx=0.17,rely=0.65)
                # Positive Image
                self.happy_img = tk.PhotoImage(file='images/happy.png')
                self.happy_lbl = tk.Label(self.pos_frame,bg=primary,image=self.happy_img)
                self.happy_lbl.place(relx=0.26,rely=0.05)
                # Positive Label
                self.positive_lbl = tk.Label(self.pos_frame,text='Positive',font=('normal',9,'bold'),fg='#008000',bg='#9de19d')
                self.positive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
                # Positive Percentage
                self.positive_per = tk.Label(self.pos_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
                self.positive_per.place(relx=0.415,rely=0.7)
                #========Neutral Frame========
                self.neu_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
                self.neu_frame.place(relx=0.41,rely=0.65)
                # Neutral Image
                self.neutral_img = tk.PhotoImage(file='images/neutral.png')
                self.neutral_lbl = tk.Label(self.neu_frame,bg=primary,image=self.neutral_img)
                self.neutral_lbl.place(relx=0.26,rely=0.05)
                # Neutral Label
                self.neutral_lbl = tk.Label(self.neu_frame,text='Neutral',font=('normal',9,'bold'),fg='#ffca18',bg='#fbe6a2')
                self.neutral_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
                # Neutral Percentage
                self.neutral_per = tk.Label(self.neu_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
                self.neutral_per.place(relx=0.415,rely=0.7)
                #========Negative Frame======
                self.neg_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
                self.neg_frame.place(relx=0.64,rely=0.65)
                # Negative Image
                self.negative_img = tk.PhotoImage(file='images/sad.png')
                self.negative_lbl = tk.Label(self.neg_frame,bg=primary,image=self.negative_img)
                self.negative_lbl.place(relx=0.26,rely=0.05)
                # Negative Label
                self.negative_lbl = tk.Label(self.neg_frame,text='Negative',font=('normal',9,'bold'),fg='#ec1c24',bg='#f6a4a8')
                self.negative_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
                # Negative Percentage
                self.negative_per = tk.Label(self.neg_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
                self.negative_per.place(relx=0.415,rely=0.7)

                # Disable Frame Content By Defalult
                for w in self.pos_frame.winfo_children(): # Positive Frame
                    w.configure(state=tk.DISABLED)
                for w in self.neu_frame.winfo_children(): # Neutral Frame
                    w.configure(state=tk.DISABLED)
                for w in self.neg_frame.winfo_children(): # Negative Frame
                    w.configure(state=tk.DISABLED)            
            # Detect Polarity Button    
            self.pol_btn = tk.Button(self.top_frame,text='Detect Polarity',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=foreground,bd=0,command=polarity)
            self.pol_btn.place(relx=0.02,rely=0.64,width=410)

            def depression():
                self.btn_lbl.place(relx=0.51,rely=0.87)
                self.pol_btn.configure(fg=gray)
                self.dep_btn.configure(fg=foreground)  
                
                # Remove every widget that stands in your way
                for w in self.main_frame.winfo_children():
                    w.destroy()
                # Text Widget
                self.text_box = tk.Text(self.main_frame,font=('normal',10),bg=primary,fg=foreground,relief='groove',bd=1)
                self.text_box.place(relx=0.17,rely=0.07,width=520,height=200)
                # Place Holder for text widget
                self.text_box.insert(tk.END,'Type something here...')
                self.text_box.bind("<FocusIn>", lambda args: self.text_box.delete("1.0",tk.END))
            
                def submit():
                    content = self.text_box.get("1.0",'end-1c') # The content of the text box
                    if content == "":
                        messagebox.showerror("Entry error","You can not perform sentiment analysis on an empty text box")
                    elif type(content) == int:
                        messagebox.showerror("Entry error","You can not perform sentiment analysis on a number")
                    else:
                        for w in self.main_frame.winfo_children():
                            w.place_forget()
                        # Label for the loader gif
                        load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                        load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                        
                        def clean():
                            processed = preprocess.CleanMessage(content)
                            if processed != "":
                                load_lbl.unload()
                                load_lbl.place_forget()
                                depressive_scorer(processed)                               
                            else:
                                pass                            
                        def load():
                            load_lbl.load('images/load.gif')
                        threading.Thread(target=clean).start()
                        threading.Thread(target=load).start() 
                # Submit Button
                self.submit = tk.Button(self.main_frame,text='Submit',bg='#ecb22e',fg=primary,font=('normal',8,'bold'),bd=0,command=submit)
                self.submit.place(relx=0.682,rely=0.45,width=100,height=30)
                hover.Hover(self.submit)
                # Clear Button
                self.clear = tk.Button(self.main_frame,text='Clear',bg='#eed8a6',fg=primary,font=('normal',8,'bold'),bd=0,command=depression)
                self.clear.place(relx=0.547,rely=0.45,width=100,height=30)
                #========Positive Frame======
                self.pos_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
                self.pos_frame.place(relx=0.28,rely=0.65)
                # Positive Image
                self.happy_img = tk.PhotoImage(file='images/happy.png')
                self.happy_lbl = tk.Label(self.pos_frame,bg=primary,image=self.happy_img)
                self.happy_lbl.place(relx=0.26,rely=0.05)
                # Positive Label
                self.positive_lbl = tk.Label(self.pos_frame,text='Positive',font=('normal',9,'bold'),fg='#008000',bg='#9de19d')
                self.positive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
                # Positive Percentage
                self.positive_per = tk.Label(self.pos_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
                self.positive_per.place(relx=0.415,rely=0.7)
                #========Depressive Frame======
                self.dep_frame = tk.Frame(self.main_frame,width=130,height=170,bg=primary,relief='raised',bd=1)
                self.dep_frame.place(relx=0.53,rely=0.65)
                # Depressive Image
                self.depressive_img = tk.PhotoImage(file='images/sad.png')
                self.depressive_lbl = tk.Label(self.dep_frame,bg=primary,image=self.depressive_img)
                self.depressive_lbl.place(relx=0.26,rely=0.05)
                # Depressive Label
                self.depressive_lbl = tk.Label(self.dep_frame,text='Depressive',font=('normal',9,'bold'),fg='#ec1c24',bg='#f6a4a8')
                self.depressive_lbl.place(relx=0.24,rely=0.5,width=70,height=20)
                # Depressive Percentage
                self.depressive_per = tk.Label(self.dep_frame,text='0%',font=('normal',10,'bold'),fg=foreground,bg=primary)
                self.depressive_per.place(relx=0.415,rely=0.7)
            
                # Disable Frame Content By Defalult
                for w in self.pos_frame.winfo_children(): # Positive Frame
                    w.configure(state=tk.DISABLED)
                for w in self.dep_frame.winfo_children(): # Depressive Frame
                    w.configure(state=tk.DISABLED) 
            # Detect Polarity Button
            self.dep_btn = tk.Button(self.top_frame,text='Detect Depression',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=gray,bd=0,command=depression)
            self.dep_btn.place(relx=0.5,rely=0.64,width=410)

            self.btn = tk.PhotoImage(file='images/btn_img.png')
            self.btn_lbl = tk.Label(self.top_frame,bg=primary,image=self.btn)
            self.btn_lbl.place(relx=0.01,rely=0.87)

            polarity() # Run the polarity function on start       
        # Text Button 
        self.text = tk.PhotoImage(file='images/text_img.png')
        self.text_btn = tk.Button(self.nav_frame,bg=gray,image=self.text,activebackground=primary,bd=0,command=text)
        self.text_btn.place(relx=0.1,rely=0.16,width=67,height=50)
        tooltip.CreateToolTip(self.text_btn,'Type text')

        def doc():
            # Configure Colour
            self.text_btn.configure(bg=primary)
            self.doc_btn.configure(bg=gray)
            self.voice_btn.configure(bg=primary)
            self.link_btn.configure(bg=primary)
            # Configure Position
            self.text_btn.place_configure(relx=0.10)
            self.doc_btn.place_configure(relx=0.13)
            self.voice_btn.place_configure(relx=0.10)
            self.link_btn.place_configure(relx=0.10)
            self.logo_lbl.place_configure(relx=0,rely=0.248)
            # Remove every widget that stands in your way
            for w in self.main_frame.winfo_children():
                w.destroy()
            for w in self.top_frame.winfo_children():
                w.destroy()
            #=============Polarity and Depression functions===========
            def polarity():
                self.btn_lbl.place(relx=0,rely=0.87)
                self.pol_btn.configure(fg=foreground)
                self.dep_btn.configure(fg=gray)
                # Remove every widget that stands in your way
                for w in self.main_frame.winfo_children():
                    w.destroy()
                def openfile():
                    # Open a window to select text document file
                    filepath = filedialog.askopenfilename(initialdir='Documents',title='Open a Document',filetypes=(("Text Document","*.txt"),("PNG Files","*.png"),("JPEG Files","*.jpg")))
                    # Open file through file path and read it's content
                    if filepath[-3:] == 'txt':
                        with open(filepath) as file_:
                            content = file_.read()
                            polarity_widgets(content)
                    elif filepath[-3:] == 'jpg' or filepath[-3:] == 'png':
                        for w in self.main_frame.winfo_children():
                            w.place_forget() 
                        # Label for the loader gif
                        load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                        load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                            
                        def clean():
                            img = ocr.get_image(filepath)
                            img = ocr.get_grayscale(img)
                            img = ocr.thresholding(img)
                            img = ocr.noise_removal(img)
                            content = ocr.ocr_core(img)
                            if content != "":
                                load_lbl.unload()
                                load_lbl.place_forget()
                                # Call the function to display the text
                                polarity_widgets(content)                               
                            else:
                                pass                            
                        def load():
                            load_lbl.load('images/load.gif')
                        threading.Thread(target=clean).start()
                        threading.Thread(target=load).start() 
                    else:
                        messagebox.showerror("File Error","Please Try Again!")
                                       
                self.info_frame = tk.Frame(self.main_frame,bg=primary,width=500,height=150,relief='groove',bd=2)
                self.info_frame.place(relx=0.2,rely=0.1)
                
                self.image = tk.PhotoImage(file='images/image.png')
                self.doc_img = tk.PhotoImage(file='images/document.png')
                self.img_lbl = tk.Label(self.info_frame,bg=primary,image=self.image,bd=0,state=tk.DISABLED)
                self.img_lbl.place(relx=0.35,rely=0.05,width=70,height=70)
                self.doc_lbl = tk.Label(self.info_frame,bg=primary,image=self.doc_img,bd=0,state=tk.DISABLED)
                self.doc_lbl.place(relx=0.50,rely=0.05,width=70,height=70)

                self.upload_lbl = tk.Label(self.info_frame,text='Upload your image or text files',\
                    font=('arial',10,'bold'),fg=foreground,bg=primary,bd=0)
                self.upload_lbl.place(relx=0.3,rely=0.60)
                self.upload_lbl2 = tk.Label(self.info_frame,text='Image and text files must\ncontain texts to be extracted from',\
                    font=('normal',9),fg=foreground,bg=primary,bd=0)
                self.upload_lbl2.place(relx=0.32,rely=0.75)
                
                self.attach_btn = tk.Button(self.main_frame,text='Choose Files',font=('arial',11,'bold'),\
                    fg=foreground,bg='#ecb22e',activebackground=gray,bd=0,command=openfile)
                self.attach_btn.place(relx=0.41,rely=0.40,width=160,height=35)
                Hover(self.attach_btn)
            self.pol_btn = tk.Button(self.top_frame,text='Detect Polarity',font=('arial',9,'bold'),\
                bg=primary,activebackground=primary,fg=foreground,bd=0,command=polarity)
            self.pol_btn.place(relx=0.02,rely=0.64,width=410)

            def depression():
                self.btn_lbl.place(relx=0.51,rely=0.87)
                self.pol_btn.configure(fg=gray)
                self.dep_btn.configure(fg=foreground)
                # Remove every widget that stands in your way
                for w in self.main_frame.winfo_children():
                    w.destroy()
                
                def openfile():
                    # Open a window to select text document file
                    filepath = filedialog.askopenfilename(initialdir='Documents',title='Open a Document',filetypes=(("Text Document","*.txt"),("PNG Files","*.png"),("JPEG Files","*.jpg")))
                    # Open file through file path and read it's content
                    if filepath[-3:] == 'txt':
                        with open(filepath) as file_:
                            content = file_.read()
                            depressive_widgets(content)
                    elif filepath[-3:] == 'jpg' or filepath[-3:] == 'png':
                        for w in self.main_frame.winfo_children():
                            w.place_forget() 
                        # Label for the loader gif
                        load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                        load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                            
                        def clean():
                            img = ocr.get_image(filepath)
                            img = ocr.get_grayscale(img)
                            img = ocr.thresholding(img)
                            img = ocr.noise_removal(img)
                            content = ocr.ocr_core(img)
                            if content != "":
                                load_lbl.unload()
                                load_lbl.place_forget()
                                # Call the function to display the text
                                depressive_widgets(content)                              
                            else:
                                pass                            
                        def load():
                            load_lbl.load('images/load.gif')
                        threading.Thread(target=clean).start()
                        threading.Thread(target=load).start() 
                    else:
                        messagebox.showerror("File Error","Please Try Again!")

                self.info_frame = tk.Frame(self.main_frame,bg=primary,width=500,height=150,relief='groove',bd=2)
                self.info_frame.place(relx=0.2,rely=0.1)
                
                self.image = tk.PhotoImage(file='images/image.png')
                self.doc_img = tk.PhotoImage(file='images/document.png')
                self.img_lbl = tk.Label(self.info_frame,bg=primary,image=self.image,bd=0,state=tk.DISABLED)
                self.img_lbl.place(relx=0.35,rely=0.05,width=70,height=70)
                self.doc_lbl = tk.Label(self.info_frame,bg=primary,image=self.doc_img,bd=0,state=tk.DISABLED)
                self.doc_lbl.place(relx=0.50,rely=0.05,width=70,height=70)

                self.upload_lbl = tk.Label(self.info_frame,text='Upload your image or text files',\
                    font=('arial',10,'bold'),fg=foreground,bg=primary,bd=0)
                self.upload_lbl.place(relx=0.3,rely=0.60)
                self.upload_lbl2 = tk.Label(self.info_frame,text='Image and text files must\ncontain texts to be extracted from',\
                    font=('normal',9),fg=foreground,bg=primary,bd=0)
                self.upload_lbl2.place(relx=0.32,rely=0.75)
                
                self.attach_btn = tk.Button(self.main_frame,text='Choose Files',font=('arial',11,'bold'),\
                    fg=foreground,bg='#ecb22e',activebackground=gray,bd=0,command=openfile)
                self.attach_btn.place(relx=0.41,rely=0.40,width=160,height=35)
                Hover(self.attach_btn)
            self.dep_btn = tk.Button(self.top_frame,text='Detect Depression',font=('arial',9,'bold'),\
                bg=primary,activebackground=primary,fg=gray,bd=0,command=depression)
            self.dep_btn.place(relx=0.5,rely=0.64,width=410)

            self.btn = tk.PhotoImage(file='images/btn_img.png')
            self.btn_lbl = tk.Label(self.top_frame,bg=primary,image=self.btn)
            self.btn_lbl.place(relx=0.01,rely=0.87)

            polarity() # Run the polarity function on start
        # Attach Document Button 
        self.doc = tk.PhotoImage(file='images/doc_img.png')           
        self.doc_btn = tk.Button(self.nav_frame,bg=primary,image=self.doc,activebackground=primary,bd=0,command=doc)
        self.doc_btn.place(relx=0.1,rely=0.25,width=67,height=50)
        tooltip.CreateToolTip(self.doc_btn,'Attach document')

        def voice():
            # Configure Colour
            self.text_btn.configure(bg=primary)
            self.doc_btn.configure(bg=primary)
            self.voice_btn.configure(bg=gray)
            self.link_btn.configure(bg=primary)
            # Configure Position
            self.text_btn.place_configure(relx=0.10)
            self.doc_btn.place_configure(relx=0.10)
            self.voice_btn.place_configure(relx=0.13)
            self.link_btn.place_configure(relx=0.10)
            self.logo_lbl.place_configure(relx=0,rely=0.338)
            # Remove every widget that stands in your way
            for w in self.main_frame.winfo_children():
                w.destroy()
            for w in self.top_frame.winfo_children():
                w.destroy()
            #=============Polarity and Depression functions===========
            def polarity():
                self.btn_lbl.place(relx=0,rely=0.87)
                self.pol_btn.configure(fg=foreground)
                self.dep_btn.configure(fg=gray)

                self.bug_img = tk.PhotoImage(file='images/coming soon.png')
                self.comingsoon = tk.Label(self.main_frame,image=self.bug_img,bg=gray,bd=0)
                self.comingsoon.place(relx=0.3,rely=0.2,width=300,height=200)

                self.comingsoon_info = tk.Label(self.main_frame,text='Coming Soon!!!',fg=foreground,bg=gray,font=('arial',20,'bold'))
                self.comingsoon_info.place(relx=0.36,rely=0.55)
                self.comingsoon_info2 = tk.Label(self.main_frame,text="We would let you know when this feature is up.",fg=foreground,bg=gray,font=('normal',10))
                self.comingsoon_info2.place(relx=0.32,rely=0.613)

            self.pol_btn = tk.Button(self.top_frame,text='Detect Polarity',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=foreground,bd=0,command=polarity)
            self.pol_btn.place(relx=0.02,rely=0.64,width=410)

            def depression():
                self.btn_lbl.place(relx=0.51,rely=0.87)
                self.pol_btn.configure(fg=gray)
                self.dep_btn.configure(fg=foreground)
            self.dep_btn = tk.Button(self.top_frame,text='Detect Depression',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=gray,bd=0,command=depression)
            self.dep_btn.place(relx=0.5,rely=0.64,width=410)

            self.btn = tk.PhotoImage(file='images/btn_img.png')
            self.btn_lbl = tk.Label(self.top_frame,bg=primary,image=self.btn)
            self.btn_lbl.place(relx=0.01,rely=0.87)

            polarity() # Run the polarity function on start
        # Voice Record Button 
        self.voice = tk.PhotoImage(file='images/voice_img.png')
        self.voice_btn = tk.Button(self.nav_frame,bg=primary,image=self.voice,activebackground=primary,bd=0,command=voice)
        self.voice_btn.place(relx=0.1,rely=0.34,width=67,height=50)
        tooltip.CreateToolTip(self.voice_btn,'Voice record')

        def link():
            # Configure Colour
            self.text_btn.configure(bg=primary)
            self.doc_btn.configure(bg=primary)
            self.voice_btn.configure(bg=primary)
            self.link_btn.configure(bg=gray)
            # Configure Position
            self.text_btn.place_configure(relx=0.10)
            self.doc_btn.place_configure(relx=0.10)
            self.voice_btn.place_configure(relx=0.10)
            self.link_btn.place_configure(relx=0.13)
            self.logo_lbl.place_configure(relx=0,rely=0.428)
            # Remove every widget that stands in your way
            for w in self.main_frame.winfo_children():
                w.destroy()
            for w in self.top_frame.winfo_children():
                w.destroy()
            
            def link_widgets():
                # Create Entry Box to accept url link
                self.url_ent = tk.Entry(self.main_frame,font=('normal',10),fg='gray60',bg=primary,relief='groove',bd=1)
                self.url_ent.place(relx=0.185,rely=0.07,width=520,height=30)   
                # Place Holder for text widget
                self.url_ent.insert(tk.END,'Enter url link to social media post...')
                self.url_ent.bind("<FocusIn>", lambda args: (self.url_ent.delete("0",tk.END),self.url_ent.configure(fg=foreground)))
                self.url_ent.bind("<FocusOut>", lambda args: (self.url_ent.insert(tk.END,'Enter url link to social media post...'),self.url_ent.configure(fg='gray60')))
     
                def search():
                    url = self.url_ent.get()

                    social_media = ["linkedin","twitter","facebook","instagram"]
                    if any(sm in url for sm in social_media) and validators.url(url):
                        for w in self.main_frame.winfo_children():
                            w.destroy()
                        # GET text from the twitter url
                        if "twitter" in url: # If the url is a twitter url
                            # Label for the loader gif
                            load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                            load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                            def get_tweet():
                                content = ""
                                content = twitter.get_text(url) # the get_text method from twitter module retuns tweet text                                                
                                if content != "":
                                    load_lbl.unload()  
                                    if self.btn_lbl.winfo_rootx() == 311:                               
                                        # Call the function to display the text for polarity
                                        polarity_widgets(content)   
                                    else:
                                        # Call the function to display the text for depression
                                        depressive_widgets(content)                                  
                            def load():                                       
                                load_lbl.load('images/load.gif')
                            threading.Thread(target=get_tweet).start()
                            threading.Thread(target=load).start()                                   
                        else:
                            pass               
                    else:
                        messagebox.showerror("Url Error","You entered an invalid URL\nMust be Facebook, Instagram, LinkedIn or Twitter URL")                       
                # Submit Button
                self.submit = tk.Button(self.main_frame,text='Search',bg='#ecb22e',fg=primary,font=('normal',8,'bold'),bd=0,command=search)
                self.submit.place(relx=0.695,rely=0.145,width=100,height=30)
                hover.Hover(self.submit)
                self.main_frame.bind("<Return>",search)
            
            #=============Polarity and Depression functions===========
            def polarity():
                for w in self.main_frame.winfo_children():
                    w.destroy()
                self.btn_lbl.place(relx=0,rely=0.87)
                self.pol_btn.configure(fg=foreground)
                self.dep_btn.configure(fg=gray)

                # Label for the loader gif
                load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                
                def check_connection():
                    if is_connected(): # If there is internet connection
                        load_lbl.unload()
                        link_widgets()
                    else: 
                        load_lbl.unload()
                        self.lbl_404 = tk.PhotoImage(file='images/error-404.png')
                        self.tryagain = tk.Button(self.main_frame,image=self.lbl_404,text='Try again',compound='top',font=('arial',9,'bold'),bg=gray,activebackground=gray,fg=foreground,bd=0,command=link)
                        self.tryagain.place(relx=0.46,rely=0.38)
                def load():
                    load_lbl.load('images/load.gif')
                threading.Thread(target=check_connection).start()
                threading.Thread(target=load).start() 
            self.pol_btn = tk.Button(self.top_frame,text='Detect Polarity',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=foreground,bd=0,command=polarity)
            self.pol_btn.place(relx=0.02,rely=0.64,width=410)

            def depression():
                for w in self.main_frame.winfo_children():
                    w.destroy()
                self.btn_lbl.place(relx=0.51,rely=0.87)
                self.pol_btn.configure(fg=gray)
                self.dep_btn.configure(fg=foreground)

                # Label for the loader gif
                load_lbl = loading.ImageLabel(self.main_frame,bg=gray)
                load_lbl.place(relx=0.45,rely=0.37,width=70,height=70)
                
                def check_connection():
                    if is_connected(): # If there is internet connection
                        load_lbl.unload()
                        link_widgets()
                    else: 
                        load_lbl.unload()
                        self.lbl_404 = tk.PhotoImage(file='images/error-404.png')
                        self.tryagain = tk.Button(self.main_frame,image=self.lbl_404,text='Try again',compound='top',font=('arial',9,'bold'),bg=gray,activebackground=gray,fg=foreground,bd=0,command=link)
                        self.tryagain.place(relx=0.46,rely=0.38)
                def load():
                    load_lbl.load('images/load.gif')
                threading.Thread(target=check_connection).start()
                threading.Thread(target=load).start() 
            self.dep_btn = tk.Button(self.top_frame,text='Detect Depression',font=('arial',9,'bold'),bg=primary,activebackground=primary,fg=gray,bd=0,command=depression)
            self.dep_btn.place(relx=0.5,rely=0.64,width=410)

            self.btn = tk.PhotoImage(file='images/btn_img.png')
            self.btn_lbl = tk.Label(self.top_frame,bg=primary,image=self.btn)
            self.btn_lbl.place(relx=0.01,rely=0.87)
            
            polarity() # Run the polarity function
         # Attach Document Button    
        # Social media link Button 
        self.link = tk.PhotoImage(file='images/link_img.png')
        self.link_btn = tk.Button(self.nav_frame,bg=primary,image=self.link,activebackground=primary,bd=0,command=link)
        self.link_btn.place(relx=0.1,rely=0.43,width=67,height=50)
        tooltip.CreateToolTip(self.link_btn,'Social media post')
            
        text() # Run the text function on start

        def toggle():
            
            if self.toggle_btn['image'] == 'pyimage12':
                self.toggle_btn.configure(image=self.light)
            else:
                self.toggle_btn.configure(image=self.dark)
        self.light = tk.PhotoImage(file='images/toggle_light.png')
        self.dark = tk.PhotoImage(file='images/toggle_dark.png')
        self.toggle_btn = tk.Button(self.nav_frame,bg=primary,activebackground=primary,image=self.dark,bd=0,command=toggle)
        self.toggle_btn.place(relx=0.20,rely=0.93)

        """# Label for the loader gif
        load_lbl = loading.ImageLabel(self.master,bg=primary)
        load_lbl.place(relx=0.45,rely=0.40,width=70,height=70)
        load_lbl.load('images/load.gif')
        self.loading = tk.Label(self.master,text='Getting things ready...',fg=foreground,bg=primary,font=('normal',9))
        self.loading.place(relx=0.425,rely=0.49)
        self.master.after(1000, continue_) # Load for 5000 milliseconds and call the continue function when done
        # Home Page
        self.bg_img = tk.PhotoImage(file='images/bg.png')
        self.bg = tk.Label(self.master,image=self.bg_img,bg=primary)
        self.bg.place(relx=0,rely=0)
        self.ill_img = tk.PhotoImage(file='images/home_illustration.png')
        self.illustration = tk.Label(self.master,image=self.ill_img,bg=primary)
        self.illustration.place(relx=0.35,rely=0.2)
        self.sentiment_lbl = tk.Label(self.master,text='SENTIMENT',fg=foreground,bg=primary,font=('Constantia',35,'bold'))
        self.sentiment_lbl.place(relx=0.04,rely=0.25)
        self.sentiment_lbl = tk.Label(self.master,text='247',fg='#ecb22e',bg=primary,font=('Constantia',35,'bold'))
        self.sentiment_lbl.place(relx=0.35,rely=0.25)
        self.sentiment_info = tk.Label(self.master,text='Our sentiment analysis tool allows you to',fg=foreground,bg=primary,font=('normal',13))
        self.sentiment_info.place(relx=0.04,rely=0.37)
        self.sentiment_info2 = tk.Label(self.master,text='conviniently dectect the emotional tone',fg=foreground,bg=primary,font=('normal',13))
        self.sentiment_info2.place(relx=0.04,rely=0.405)
        self.sentiment_info3 = tk.Label(self.master,text='behind text data by dictating polarity and',fg=foreground,bg=primary,font=('normal',13))
        self.sentiment_info3.place(relx=0.04,rely=0.437)
        self.sentiment_info4 = tk.Label(self.master,text='determining depression.',fg=foreground,bg=primary,font=('mormal',13))
        self.sentiment_info4.place(relx=0.04,rely=0.470)
        
        # Get Started Button
        self.getstarted = tk.Button(self.master,text='Get Started',font=('mormal',9,'bold'),fg='#3f3d56',bg='#ecb22e',activebackground=primary,bd=0,command=getstarted)
        self.getstarted.place(relx=0.04,rely=0.56,width=150,height=35)
        self.getstarted.focus() # Focus on this button when the program starts
        Hover(self.getstarted)
        self.getstarted.bind("<Return>",getstarted) # Bind the return(enter) key to the get started function"""

if __name__=='__main__':
    root = tk.Tk() 

    app = App(root)
    
    root.mainloop()