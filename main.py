import tkinter as tk
import json
from cryptography.fernet import Fernet
import base64


# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.file = File()
        self.encrypter = Encrypter()
        self.pack()
        self.create_widgets_home()

    # Validate the password
    def validate(self, password):
        if password == 'toto':
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
        entry.pack(side="top")

        btValidate = tk.Button(self.frameHome, text="Valider",
                               command=lambda: self.validate(password.get()))

        btValidate.pack(side="top")

    def create_widgets_passwords(self):
        self.framePasswords = tk.Frame(root, bg='green')
        self.framePasswords.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)

        jsonDictionnary = self.file.getJson()

        user = {}
        password = {}
        hasToDelete = {}
        for key in jsonDictionnary:
            framePassword = tk.Frame(self.framePasswords, bg='blue')
            framePassword.pack(side=tk.TOP)

            label = tk.Label(framePassword, text=key)
            label.pack(side="left")

            user[key] = tk.StringVar()
            user[key].set(jsonDictionnary[key]["User"])
            entryUser = tk.Entry(framePassword, textvariable=user[key], width=30)
            entryUser.pack(side="left")

            password[key] = tk.StringVar()
            password[key].set(self.encrypter.decrypt(jsonDictionnary[key]["Password"]))
            entryPassword = tk.Entry(framePassword, textvariable=password[key], width=30)
            entryPassword.pack(side="left")

            hasToDelete[key] = tk.IntVar()
            checkBoxDelete = tk.Checkbutton(framePassword, text="Supprimer?", variable=hasToDelete[key],
                                            onvalue=1, offvalue=0, height=5,
                                            width=20, )
            checkBoxDelete.pack()

        newAccount = tk.StringVar()
        newAccount.set('Plateforme')
        entryNewAccount = tk.Entry(self.framePasswords, textvariable=newAccount, width=30)
        entryNewAccount.pack(side="left")
        btAddAccount = tk.Button(self.framePasswords, text="Ajouter un compte",
                                 command=lambda: self.addAccount(newAccount.get()))

        btAddAccount.pack(side="left")

        btModify = tk.Button(self.framePasswords, text="Enregistrer",
                             command=lambda: self.modifyAccounts(user, password))

        btModify.pack(side="left")

        btDelete = tk.Button(self.framePasswords, text="Supprimer",
                             command=lambda: self.deleteAccounts(hasToDelete))

        btDelete.pack(side="left")

    def modifyAccounts(self, user, password):
        jsonDictionnary = self.file.getJson()

        for key in jsonDictionnary:
            jsonDictionnary[key]["User"] = user[key].get()
            jsonDictionnary[key]["Password"] = self.encrypter.encrypt(password[key].get())

        print(jsonDictionnary)
        self.file.setJson(jsonDictionnary)

    def addAccount(self, plateform):
        jsonDictionnary = self.file.getJson()
        newAccount = {plateform: {'User': 'default', 'Password': self.encrypter.encrypt('default')}}
        jsonDictionnary.update(newAccount)
        self.setAndReloadFrame(jsonDictionnary)

    def deleteAccounts(self, hasToDelete):
        jsonDictionnary = self.file.getJson()
        for key in hasToDelete:
            if hasToDelete[key].get():
                del jsonDictionnary[key]
        self.setAndReloadFrame(jsonDictionnary)

    def setAndReloadFrame(self, jsonDictionnary):
        self.file.setJson(jsonDictionnary)
        self.delete_frame(self.framePasswords)
        self.create_widgets_passwords()

class File:
    def getJson(self):
        with open('mdp.json') as file:
            return json.load(file)

    def setJson(self, data):
        with open('mdp.json', 'w') as file:
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
        print(data)
        bytes = self.stringToBytes(data)
        print(bytes)
        f = Fernet(self.key)
        data = f.encrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned

    def decrypt(self, data):
        print(data)
        bytes = self.stringToBytes(data)
        print(bytes)
        f = Fernet(self.key)
        data = f.decrypt(bytes)
        dataReturned = self.bytesToString(data)
        return dataReturned


root = tk.Tk()
root.geometry('1000x1000')
root.title('Gestionnaire de mots de passe')
app = Application(master=root)
app.mainloop()
