import tkinter as tk
import sys
from tkinter.messagebox import *
from model import encrypter
from model import file

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

class MainApplication(tk.Frame):
    def __init__(self, master=None):
        self.window = master
        super().__init__(self.window)
        self.pack()
        self.window.withdraw()
        secondaryWindow = tk.Toplevel()
        secondaryWindow.geometry("200x100")
        secondaryWindow.resizable(width=False, height=True)
        secondaryWindow.title('Login')
        secondaryWindow.bind("<<Login>>", self.showMainWindow)
        secondaryWindow.bind("<<Close>>", sys.exit)
        app = loginApplication(master=secondaryWindow)
        app.mainloop()

    def showMainWindow(self, *args):
        self.window.deiconify()
        self.createMenuBar(self.window)
        self.file = file.File()
        self.encrypter = encrypter.Encrypter()
        self.createWidgetsPasswords()

    def createMenuBar(self, window):
        menuBar = tk.Menu(window)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Ajouter un compte", command=self.addAccount)
        fileMenu.add_command(label="Modifier le mot de passe principal", command=self.modifyMainPassword)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quitter", command=window.quit)
        menuBar.add_cascade(label="Fichier", menu=fileMenu)
        window.config(menu=menuBar)

    def createWidgetsPasswords(self):
        self.mainFrame = tk.Frame(self.window, bg='red')
        self.mainFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.passwordsFrame = ScrollableFrame(self.mainFrame, bg='green')
        self.passwordsFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        imgCopy = tk.PhotoImage(file="image/CopyToClipBoard.png")
        jsonDictionnary = self.file.getJson()["Applications"]

        user = {}
        password = {}
        hasToDelete = {}
        for key in jsonDictionnary:
            framePassword = tk.Frame(self.passwordsFrame.scrollable_frame, bg='blue')
            framePassword.pack(fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)
            label = tk.Label(framePassword, text=key, width=30)
            label.pack(side=tk.LEFT, padx=5, pady=5)

            user[key] = tk.StringVar()
            user[key].set(jsonDictionnary[key]["User"])
            entryUser = tk.Entry(framePassword, textvariable=user[key], width=30, justify='center')
            entryUser.pack(side=tk.LEFT, padx=5, pady=5)

            password[key] = tk.StringVar()
            password[key].set(self.encrypter.decrypt(jsonDictionnary[key]["Password"]))
            entryPassword = tk.Entry(framePassword, textvariable=password[key], show="*", width=30, justify='center')
            entryPassword.pack(side=tk.LEFT, padx=5, pady=5)

            hasToDelete[key] = tk.IntVar()
            checkBoxDelete = tk.Checkbutton(framePassword, variable=hasToDelete[key],
                                            onvalue=1, offvalue=0)
            checkBoxDelete.pack(side=tk.RIGHT, padx=5, pady=5)

            btCopyToClipBoard = tk.Button(framePassword, image=imgCopy,
                                 command=lambda key=key: self.CopyToClipBoard(key))
            btCopyToClipBoard.image = imgCopy
            btCopyToClipBoard.pack(side=tk.RIGHT, pady=5)

        btModify = tk.Button(self.mainFrame, text="Enregistrer",
                             command=lambda: self.modifyAccounts(user, password))
        btModify.pack(side=tk.LEFT, padx=50, pady=5)

        btDelete = tk.Button(self.mainFrame, text="Supprimer",
                             command=lambda: self.deleteAccounts(hasToDelete))
        btDelete.pack(side=tk.RIGHT, padx=50, pady=5)

    # Delete the frame
    def deleteFrame(self, frame):
        frame.destroy()

    def modifyAccounts(self, user, password):
        jsonDictionnaryAccounts = self.file.getJson()["Applications"]
        jsonDictionnary = self.file.getJson()

        for key in jsonDictionnaryAccounts:
            jsonDictionnaryAccounts[key]["User"] = user[key].get()
            jsonDictionnaryAccounts[key]["Password"] = self.encrypter.encrypt(password[key].get())

        jsonDictionnary["Applications"].update(jsonDictionnaryAccounts)

        self.file.setJson(jsonDictionnary)

    def deleteAccounts(self, hasToDelete):
        if askyesno('Validation', 'Êtes-vous sûr de vouloir faire ça?'):
            jsonDictionnary = self.file.getJson()

            for key in hasToDelete:
                if hasToDelete[key].get():
                    del jsonDictionnary["Applications"][key]

            self.file.setJson(jsonDictionnary)
            self.reloadFrame()
            showinfo('Suppression', 'Suppression effectuée')

    def CopyToClipBoard(self, key):
        jsonDictionnaryAccounts = self.file.getJson()["Applications"]

        self.window.clipboard_clear()
        self.window.clipboard_append(self.encrypter.decrypt(jsonDictionnaryAccounts[key]["Password"]))

    def reloadFrame(self, *args):
        if not args or type(args[0].widget) is tk.Toplevel:
            self.deleteFrame(self.mainFrame)
            self.createWidgetsPasswords()

    def modifyMainPassword(self):
        secondaryWindow = tk.Toplevel()
        secondaryWindow.geometry("200x200")
        secondaryWindow.resizable(width=False, height=True)
        secondaryWindow.title('Changer le mot de passe principal')
        secondaryWindow.grab_set()
        app = ChangeMainPasswordApplication(master=secondaryWindow)
        app.mainloop()

    def addAccount(self):
        secondaryWindow = tk.Toplevel()
        secondaryWindow.geometry("200x100")
        secondaryWindow.resizable(width=False, height=True)
        secondaryWindow.title('Ajouter un nouveau compte')
        secondaryWindow.bind("<Destroy>", self.reloadFrame)
        secondaryWindow.grab_set()
        app = addAccountApplication(master=secondaryWindow)
        app.mainloop()


class loginApplication(tk.Frame):
    def __init__(self, master=None):
        self.window = master
        super().__init__(self.window)
        self.file = file.File()
        self.encrypter = encrypter.Encrypter()
        self.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.createWidgetsHome()

    # create widgets for home page
    def createWidgetsHome(self):
        self.frameHome = tk.Frame(self.window, bg='green')
        # self.frameHome.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.frameHome.place(relx=.5, rely=.5, anchor="center")

        password = tk.StringVar()
        password.set("test")

        entry = tk.Entry(self.frameHome, textvariable=password, width=30, justify='center', show="*")
        entry.pack()

        btValidate = tk.Button(self.frameHome, text="Valider",
                               command=lambda: self.validatePassword(password.get()))

        btValidate.pack()

    # Validate the password
    def validatePassword(self, password):
        jsonDictionnary = self.file.getJson()
        if password == self.encrypter.decrypt(jsonDictionnary["MainPassword"]):
            self.window.event_generate("<<Login>>")
            self.window.destroy()

    def onClosing(self):
        self.window.event_generate("<<Close>>")
        self.window.destroy()


class ChangeMainPasswordApplication(tk.Frame):
    def __init__(self, master=None):
        self.window = master
        super().__init__(self.window)
        self.file = file.File()
        self.encrypter = encrypter.Encrypter()
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        jsonDictionnary = self.file.getJson()

        password = tk.StringVar()
        password.set(self.encrypter.decrypt(jsonDictionnary["MainPassword"]))
        entryPassword = tk.Entry(self.window, textvariable=password, justify='center')
        entryPassword.pack(side=tk.TOP, padx=5, pady=5)

        btModifyMainPassword = tk.Button(self.window, text="Modifier mot de passe principal",
                                         command=lambda: self.modifyPassword(password))
        btModifyMainPassword.pack(side=tk.BOTTOM)

    def modifyPassword(self, password):
        jsonDictionnary = self.file.getJson()

        newPassword = {"MainPassword": self.encrypter.encrypt(password.get())}

        jsonDictionnary.update(newPassword)

        self.file.setJson(jsonDictionnary)
        self.window.destroy()


class addAccountApplication(tk.Frame):
    def __init__(self, master=None):
        self.window = master
        super().__init__(self.window)
        self.file = file.File()
        self.encrypter = encrypter.Encrypter()
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        plateform = tk.StringVar()
        entryPlateform = tk.Entry(self.window, textvariable=plateform, width=50, justify='center')
        entryPlateform.pack(side=tk.TOP, padx=5, pady=5)

        btAddAccount = tk.Button(self.window, text="Ajouter le compte",
                                         command=lambda: self.addAccount(plateform))
        btAddAccount.pack(side=tk.BOTTOM)

    def addAccount(self, plateform):
        jsonDictionnaryAccounts = self.file.getJson()["Applications"]
        jsonDictionnary = self.file.getJson()

        newAccount = {plateform.get(): {'User': 'default', 'Password': self.encrypter.encrypt('default')}}

        jsonDictionnaryAccounts.update(newAccount)
        jsonDictionnary["Applications"].update(jsonDictionnaryAccounts)

        self.file.setJson(jsonDictionnary)
        self.window.destroy()
