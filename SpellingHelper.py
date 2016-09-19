'''
This Module Generates the Actual GUI for
the Spelling Helper

This is used to help with spelling,
will look up words in a data base with
preloaded words

Author: Zachary Kirby
'''
from tkinter import *

from Textwork import TextObject, NamedText, SqlConnection

class MainWindow:

    def __init__(self, master):
        #Add Frames
        frame = Frame(master);frame.pack()

        #Initlize the Sql Connection
        self.connection = SqlConnection()
        self.connection.inilalize()

        #Initlize Text Connection
        self.master_text = TextObject()

        #Add Buttons
        self.addButton = Button(frame, text="Add", command=self.addText, width=10);self.addButton.grid(row=0,column=0,sticky=N+W, padx = 20)
        self.defineButton = Button(frame, text="Define", command=self.processText, width=10);self.defineButton.grid(row=0,column=2, stick=W, padx= 20)

        #Add Text manipulation
        self.textInput = Entry(frame, width=25);self.textInput.grid(row=0,column=1, sticky=W)
        self.textOutput = Text(frame, state=DISABLED, borderwidth=4, height=14, width=68, bg='lightblue',fg='darkblue', wrap=WORD);self.textOutput.grid(row=1,column=0,columnspan=3)

        #Bindings
        #self.get_dim(frame)
        self.textInput.bind("<Key>", self.speed_lookup)
        self.textInput.bind("<Return>", self.speed_return)

    def short_return(self, fr):
        '''Allows the user to use the
        return key to lookup words'''
        def key(event):
            print("pressed", repr(event.char))
        fr.bind('<Key>', key)

    def speed_lookup(self, event):
        '''Looks up similar characters'''
        current_input = self.textInput.get()
        if " " not in current_input:
            text = self.master_text.name_similarity(current_input)
        else:
            text = ""
        self.short_display_text(text)

    def speed_return(self, event):
        '''Easy access to defining words'''
        self.processText()

    def get_dim(self, fr):
        '''get the dimensions of the window'''
        def resize(event):
            print(event.char, event.height)
        fr.bind('<Configure>', resize)

    def addText(self):
        '''add text to the data base'''
        if len(self.textInput.get()) > 0:
            self.master_text.add_text(self.textInput.get())
        else:
            print("Nothing to process")

    def processText(self):
        '''search for definition in database, else
        search for it using the website'''
        input_text = self.textInput.get()

        if not self.specific_command(input_text):
            to_input = input_text.split()
            definition = NamedText(to_input)
            display_text = definition.text
            if display_text != '':
                self.short_display_text(definition.text)
            else:
                self.short_display_text(":( Nothing was found for {}".format(input_text))

    def specific_command(self, text):
        commands = ['-d', '-c']
        if text.startswith(commands[0]):
            which_data = int(text[3])
            self.short_display_text(self.connection.display(setting=which_data))
            return True
        elif text.startswith(commands[1]):
            which_data = int(text[3])
            self.short_display_text("Cleaning Data")
            self.connection.clean(setting=which_data)
            self.short_display_text("Data Cleaned")
            return True
        return False


    def short_display_text(self, text):
        '''allows text to be displayed'''
        assert isinstance(text, str), "Text must be of type string"
        self.textOutput.config(state=NORMAL)
        self.textOutput.delete("1.0", END)
        self.textOutput.insert(END, text)
        self.textOutput.config(state=DISABLED)

def main():
    '''run main loop for
    spelling GUI'''

    #Root Setup
    root = Tk()
    root.title("By Character Search Application")
    root.geometry("493x255")

    #Create window and run
    window = MainWindow(root)
    root.mainloop()
    window.connection.close()

if __name__ == '__main__': main()