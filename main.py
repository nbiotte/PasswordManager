import tkinter as tk
from tkinter.messagebox import *
import json
from cryptography.fernet import Fernet
import base64


# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg='green')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.file = File()
        self.encrypter = Encrypter()
        self.pack()
        self.create_widgets_home()

    # Validate the password
    def validate(self, password):
        jsonDictionnary = self.file.getJson()
        if password == self.encrypter.decrypt(jsonDictionnary["MainPassword"]):
            self.delete_frame(self.frameHome)
            self.create_widgets_passwords()

    # Delete the frame
    def delete_frame(self, frame):
        frame.destroy()

    # create widgets for home page
    def create_widgets_home(self):
        self.frameHome = tk.Frame(root, bg='green')
        self.frameHome.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)

        password = tk.StringVar()
        password.set("toto")

        entry = tk.Entry(self.frameHome, textvariable=password, width=30)
        entry.pack(side=tk.TOP)

        btValidate = tk.Button(self.frameHome, text="Valider",
                               command=lambda: self.validate(password.get()))

        btValidate.pack(side=tk.TOP)

    def create_widgets_passwords(self):
        self.mainFrame = tk.Frame(root, bg='red')
        self.mainFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.framePasswords = ScrollableFrame(self.mainFrame, bg='green')
        self.framePasswords.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        jsonDictionnary = self.file.getJson()["Applications"]

        user = {}
        password = {}
        hasToDelete = {}
        for key in jsonDictionnary:
            framePassword = tk.Frame(self.framePasswords.scrollable_frame, bg='blue')
            framePassword.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
            label = tk.Label(framePassword, text=key, width=30)
            label.pack(side=tk.LEFT, padx=5, pady=5)

            user[key] = tk.StringVar()
            user[key].set(jsonDictionnary[key]["User"])
            entryUser = tk.Entry(framePassword, textvariable=user[key], width=30)
            entryUser.pack(side=tk.LEFT, padx=5, pady=5)

            password[key] = tk.StringVar()
            password[key].set(self.encrypter.decrypt(jsonDictionnary[key]["Password"]))
            entryPassword = tk.Entry(framePassword, textvariable=password[key], width=30)
            entryPassword.pack(side=tk.LEFT, padx=5, pady=5)

            hasToDelete[key] = tk.IntVar()
            checkBoxDelete = tk.Checkbutton(framePassword, text="Supprimer?", variable=hasToDelete[key],
                                            onvalue=1, offvalue=0)
            checkBoxDelete.pack(side=tk.RIGHT, padx=5, pady=5)

        newAccount = tk.StringVar()
        newAccount.set('Plateforme')
        entryNewAccount = tk.Entry(self.mainFrame, textvariable=newAccount, width=30)
        entryNewAccount.pack(side=tk.LEFT)

        btAddAccount = tk.Button(self.mainFrame, text="Ajouter un compte",
                                 command=lambda: self.addAccount(newAccount.get()))
        btAddAccount.pack(side=tk.LEFT)

        btModify = tk.Button(self.mainFrame, text="Enregistrer",
                             command=lambda: self.modifyAccounts(user, password))
        btModify.pack(side=tk.LEFT)

        btDelete = tk.Button(self.mainFrame, text="Supprimer",
                             command=lambda: self.deleteAccounts(hasToDelete))
        btDelete.pack(side=tk.LEFT)

        btModifyMainPassword = tk.Button(self.mainFrame, text="Modifier mot de passe principal",
                             command=self.modifyMainPassword)
        btModifyMainPassword.pack(side=tk.LEFT)

    def modifyAccounts(self, user, password):
        jsonDictionnaryAccounts = self.file.getJson()["Applications"]
        jsonDictionnary = self.file.getJson()

        for key in jsonDictionnaryAccounts:
            jsonDictionnaryAccounts[key]["User"] = user[key].get()
            jsonDictionnaryAccounts[key]["Password"] = self.encrypter.encrypt(password[key].get())

        jsonDictionnary["Applications"].update(jsonDictionnaryAccounts)

        self.file.setJson(jsonDictionnary)

    def addAccount(self, plateform):
        jsonDictionnaryAccounts = self.file.getJson()["Applications"]
        jsonDictionnary = self.file.getJson()

        newAccount = {plateform: {'User': 'default', 'Password': self.encrypter.encrypt('default')}}

        jsonDictionnaryAccounts.update(newAccount)
        jsonDictionnary["Applications"].update(jsonDictionnaryAccounts)

        self.setAndReloadFrame(jsonDictionnary)

    def deleteAccounts(self, hasToDelete):
        if askyesno('Validation', 'Êtes-vous sûr de vouloir faire ça?'):
            jsonDictionnary = self.file.getJson()

            for key in hasToDelete:
                if hasToDelete[key].get():
                    del jsonDictionnary["Applications"][key]

            self.setAndReloadFrame(jsonDictionnary)
            showinfo('Suppression', 'Suppression effectuée')

    def setAndReloadFrame(self, jsonDictionnary):
        self.file.setJson(jsonDictionnary)
        self.delete_frame(self.mainFrame)
        self.create_widgets_passwords()

    def modifyMainPassword(self):
        pass

class File:
    def getJson(self):
        with open('data/mdp.json') as file:
            return json.load(file)

    def setJson(self, data):
        with open('data/mdp.json', 'w') as file:
            json.dump(data, file, indent=4)


class Encrypter:
    key = b'Gg91BbmzEad1OyTOGF4wdQNWcmuOlNcvY4-rpHtK3YE='

    def bytesToString(self, dataBytes):
        str = dataBytes.decode('utf-8')
        return str

    def stringToBytes(self, dataString):
        dataBytes = bytes(dataString, 'UTF-8')
        return dataBytes

    def encrypt(self, data):
        bytes = self.stringToBytes(data)
        f = Fernet(self.key)
        data = f.encrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned

    def decrypt(self, data):
        bytes = self.stringToBytes(data)
        f = Fernet(self.key)
        data = f.decrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned


root = tk.Tk()
root.geometry("773x500")
root.resizable(width=False, height=True)
root.title('Gestionnaire de mots de passe')
app = Application(master=root)
app.mainloop()
