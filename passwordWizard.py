# Password Generator V1.9 08/12/2016 14:51
# Tom Kuipers
# Version Notes: Fixed URL ico downoad. Finished check box validation!
# Known issues: The about button renders everything unresponisve, reload required. Suspicion is that I'm not properly returning from the about function. WAS FIXED.
# Something interesting I found, the GUI won't update dynamically, every time you want to add a widget while the program is running you have to re-initialize the Tkinter GUI class. <-- I take that back, just use a textvariable in your label and a StringVar. For everything else though, it still stands.
# TO-DO: Implement data import using shelve. Implement AES encryption with PyCrypto
# Direction of Project: Implement another Tkinter window with a table, allowing you to store passwords and give a friendly name. Implement AES 256-bit encryption for that table. (Need to look in to storage file type).
#
# NOTE: time.sleep() is of no use in Tkinter. It is very linear in the way that what it does is halts the program for x seconds and then resumes. [widget].after(ms, function) is much better as Tkinter runs it in another thread, so the program still functions while things get updated in the background.
# NOTE: For the checkboxes, if I can make a set of if statements and add states to the checkboxes (True or False) then I can generate the passwords
#       so that if the state is true, ammend one big command and parse it the algorithm. Going to take time, so will be tested in checkboxes.py.
# NOTE: Tkinter allows for frame stacking. You can toggle which frame to display and it requires a controller for which you can 

#Main font to be used. This is kind of like CSS, declaring a default rule and then displaying the GUI by options set by a variable.

#

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

#Password Wizard
class password_wizard(tkinter.Tk, passwordGenerator):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo, PageThree, PageFour, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageOne")

    def get_page(self, page_class):
        return self.frames[page_class]

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class PageOne(tkinter.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Password Entry Wizard.\n Press next to continue", font=main_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tkinter.Button(self, text="Next", command=lambda: controller.show_frame("PageTwo"))
        button2 = tkinter.Button(self, text="Exit")
        button1.pack()
        button2.pack(side="bottom", anchor="s")

class PageTwo(tkinter.Frame):

    def submitdata(self, controller):
        namevar = self.name.get()
        print(namevar)
        controller.show_frame("PageThree")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter a name:", font=main_font)
        label.pack(side="top", fill="x", pady=10)
        self.name = ttk.Entry(self, width=14)
        self.name.pack()
        button1 = tkinter.Button(self, text="Next", command=lambda: controller.show_frame("PageThree"))
        button2 = tkinter.Button(self, text="Exit")
        button1.pack()
        button2.pack(side="bottom", anchor="s")

class PageThree(tkinter.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter a username:", font=main_font)
        label.pack(side="top", fill="x", pady=10)
        self.username = ttk.Entry(self, width=14)
        self.username.pack()
        button1 = tkinter.Button(self, text="Next", command=lambda: controller.show_frame("PageFour"))
        button2 = tkinter.Button(self, text="Exit")
        button1.pack()
        button2.pack(side="bottom", anchor="s")

class PageFour(tkinter.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Confirm Password?", font=main_font)
        label.pack(side="top", fill="x", pady=10)
        
        password = ttk.Entry(self, width=14)
        button1 = tkinter.Button(self, text="Next", command=lambda: controller.show_frame("PageFive"))
        button2 = tkinter.Button(self, text="Exit")
        button1.pack()
        button2.pack(side="bottom", anchor="s")

class PageFive(tkinter.Frame):

    def submit_data(self, controller):
        page2 = self.controller.get_page("PageTwo")
        name = page2.name.get()
        print(name)
        page3 = self.controller.get_page("PageThree")
        username = page3.username.get()
        print(username)
        password = passwordGenerator.get_password(passwordGenerator)
        print(password)        

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Confirm?", font=main_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tkinter.Button(self, text="Get Data", command=lambda: self.submit_data(controller))
        button1.pack()
        button2 = tkinter.Button(self, text="Exit")
        button2.pack(side="bottom", anchor="s")
 
if __name__ == '__main__':
    root = tkinter.Tk()
    passwordGenerator(root)
    #opener=urllib.request.build_opener()
    #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    #urllib.request.install_opener(opener)

    #url='https://physionx.co.uk/favicon.ico'
    #try:
    #    root.iconbitmap(urllib.request.urlretrieve(url))
    #except urllib.error.URLError:
     #   print("No internet connection. Won't fetch window icon.")
    root.mainloop()

			
