#Password Generator Window
main_font = ("Helvetica", 12, "bold")
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import IntVar
import string
from random import *
import time
import urllib.request #Used to dynamically request and use a window icon. Avoids packaging an ico with the exe.
import shelve
import sys

class passwordGenerator(ttk.Frame):
    #GUI Object and Functions.
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.passwordlabel = ""
        self.passwordGet = ""
        self.init_gui()
 
    def reset_text(self):
        mainText.set("Password Generator")

    def on_quit(self):
        #Exit Function.
        self.quit()
        
    def on_about(self):
        #Display about information.
        #Doesn't like being told to init_gui again. Time delay happens before the text is set. FIXED with after. Note above.
        mainText.set("Made By Tom Kuipers")
    
    def check_length(self, *args):
        #Data validation for the length input. Stops annoying people from entering strings or ridiculously large numbers in to the text box.
        #DONE 06/11/2016
        try:
            length = int(self.num1_entry.get())
        except (ValueError, UnboundLocalError):
            mainText.set("Enter a whole number!")
            self.after(3000, self.reset_text)

        try:
            if length <= 22:
                try:
                    self.generator(length)
                except UnboundLocalError:
                    print()
            else:
                mainText.set("No higher than 22 please!")
                self.after(3000, self.reset_text)
        except UnboundLocalError:
            print()
            
    def on_copy(self, *args):
        root.clipboard_clear()
        root.clipboard_append(self.answer_label.cget("text"))
        self.copy_window()

    def on_save(self, *args):
        self.passwordStorageWindow()        

    def generator(self, length):
        #Password Generator.
        self.answer_label['text'] = ""
        length = int(self.num1_entry.get())
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation
        #Checkbox Read
        try:
            validCharacters = []
            if lowerEnabled.get() == 1:
                lowercase = list(lowercase)
                for i in lowercase:
                    validCharacters.append(i)
            if upperEnabled.get() == 1:
                uppercase = list(uppercase)
                for i in uppercase:
                    validCharacters.append(i)
            if numbersEnabled.get() == 1:
                digits = list(digits)
                for i in digits:
                    validCharacters.append(i)
            if symbolsEnabled.get() == 1:
                symbols = list(symbols)
                for i in symbols:
                    validCharacters.append(i)
            password = "".join(choice(validCharacters) for x in range(length))
            self.passwordlabel.set(password)
            get_password()
           # self.answer_label['text'] = password
        except:
            mainText.set("Configure Settings!")
            self.after(3000, self.reset_text)
            self.get_password()

    def copy_window(self, *args):
        t = tk.Toplevel(self)
        t.wm_title("Password Generator")
        l = tk.Label(t, text="Copied to clipboard!", font="Helvetica 12 bold italic")
        l.pack(side="top", fill="both", expand=True, padx=50, pady=25)
        t.after(750, lambda: t.destroy()) #Lambda is a great way to do this; no extra function to call and can run a direct command.

    def save_password(self, passwordName, userName, password):
        print(passwordName, userName, password)
#        passwords = shelve.open("credentials", "c")
#        passwords["test"] = ["youtube.com", "test", "test123"]
#        passwords.sync()
#        print(passwords["test"])
#        passwords.close()

    def password_storage_wizard(self):
        wizard = password_wizard()
        wizard.title("Password Wizard")

    def get_password(self):
        self.passwordGet = self.passwordlabel.get()
        print(self.passwordGet)
        return self.passwordGet

    def init_gui(self):
        #Initiates GUI.
        self.root.title('Password Generator')
        self.root.option_add('*tearOff', 'FALSE')
        root.bind('<Return>', self.check_length)
        root.bind('<Control-c>', self.on_copy)

        #[Tkinter]Var variables to be changed throughout execution.
        global mainText
        global lowerEnabled
        global upperEnabled
        global numbersEnabled
        global symbolsEnabled
        global passwordlabel
        self.passwordlabel = StringVar()
        mainText = StringVar()
        lowerEnabled = IntVar()
        upperEnabled = IntVar()
        numbersEnabled = IntVar()
        symbolsEnabled = IntVar()

        mainText.set("Password Generator")
 
        self.grid(column=0, row=0, sticky='nsew')
 
        self.menubar = tkinter.Menu(self.root)
 
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
 
        self.menu_help = tkinter.Menu(self.menubar)
        self.menu_help.add_command(label='About', command=self.on_about)
        
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_help, label='Help')
 
        self.root.config(menu=self.menubar)
 
        self.num1_entry = ttk.Entry(self, width=5)
        self.num1_entry.grid(column=1, row = 2)
 
        self.gen_button = ttk.Button(self, text='Generate!',
                command=self.check_length)
        self.gen_button.grid(column=0, row=3, columnspan=4)
        
        self.copy_button = ttk.Button(self, text='Copy', command=self.on_copy)
        self.copy_button.grid(column=0, row=5, columnspan=4, sticky="w")

        self.save_button = ttk.Button(self, text='Save', command=self.password_storage_wizard)
        self.save_button.grid(column=1, row=5, columnspan=4, sticky="e")

        self.settings_frame = ttk.LabelFrame(self, text='Password Settings:', height=100)
        self.settings_frame.grid(column=0, row=6, columnspan=4, sticky='nesw')

        self.settings_frame2 = ttk.LabelFrame(self, height=10)
        self.settings_frame2.grid(column=1, row=6, columnspan=4, sticky='nesw')

        self.lowerletters = ttk.Checkbutton(self.settings_frame, text="Lower Letters", variable=lowerEnabled, onvalue=1, offvalue=0)
        self.lowerletters.pack(side='top', anchor='w')
        self.upperletters = ttk.Checkbutton(self.settings_frame, text="Upper Letters", variable=upperEnabled, onvalue=1, offvalue=0)
        self.upperletters.pack(side='bottom', anchor='w')
        self.numbers = ttk.Checkbutton(self.settings_frame2, text="Numbers", variable=numbersEnabled, onvalue=1, offvalue=0)
        self.numbers.pack(side='top', anchor='w')
        self.symbols = ttk.Checkbutton(self.settings_frame2, text="Symbols", variable=symbolsEnabled, onvalue=1, offvalue=0)

        self.answer_frame = ttk.LabelFrame(self, text='Generated Password:', height=100)
        self.answer_frame.grid(column=0, row=4, columnspan=4, sticky='nesw')
        self.answer_label = ttk.Label(self.answer_frame, text='', textvariable=self.passwordlabel)
        self.answer_label.grid(column=0, row=0)
        self.symbols.pack(side='bottom', anchor='w')
        
        self.changeableText = ttk.Label(self, text="Password Generator", textvariable=mainText, font="Helvetica 12 bold italic").grid(column=0, row=0, columnspan=4)
 
        # Labels that remain constant through execution.
        ttk.Label(self, text='Length of Password:').grid(column=0, row=2,
                sticky='w')
 
        ttk.Separator(self, orient='horizontal').grid(column=0,
                row=1, columnspan=4, sticky='ew')
 
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

#Encryption Algorithm
#class encryptionAlgorithm(self):