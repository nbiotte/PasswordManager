import tkinter as tk
from model import application

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
mainWindow = tk.Tk()
mainWindow.geometry("738x500")
mainWindow.resizable(width=False, height=True)
mainWindow.title('Gestionnaire de mots de passe')
app = application.MainApplication(master=mainWindow)
app.mainloop()
