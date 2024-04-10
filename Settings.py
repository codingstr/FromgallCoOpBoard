import os
from tkinter import ttk, Frame, Label, Button, VERTICAL, N, S, E, W, Entry, Toplevel

settings = [10, ["pc", "뉴비"], ["xbox", "엑박"]]

def refList(tree: ttk.Treeview) :
    for i in tree.get_children() :
        tree.delete(i)
    
    if (len(settings[1]) < len(settings[2])) :
        for wordIdx in range(len(settings[1])) :
            tree.insert('', 'end', values=(settings[1][wordIdx], settings[2][wordIdx]))
        for wordIdx in range(len(settings[1]), len(settings[2])) :
            tree.insert('', 'end', values=("", settings[2][wordIdx]))
    else :
        for wordIdx in range(len(settings[2])) :
            tree.insert('', 'end', values=(settings[1][wordIdx], settings[2][wordIdx]))
        for wordIdx in range(len(settings[2]), len(settings[1])) :
            tree.insert('', 'end', values=(settings[1][wordIdx], ""))

def openSettingsWindow() :

    # window settings
    global settingsWindow
    settingsWindow = Toplevel()
    settingsWindow.title("Settings")
    settingsWindow.geometry("500x550")
    settingsWindow.resizable(False, False)

    # Frame
    settingsFrame = Frame(settingsWindow)
    settingsFrame.pack(pady=10)

    # Refresh Time
    refTimeLbl = Label(settingsFrame, text="Refresh time (seconds)")
    refTimeLbl.grid(row=0, column=0)

    refTimeEnt = Entry(settingsFrame)
    refTimeEnt.grid(row=0, column=1)

    # refTimeBtn = Button(settingsFrame, text="Save", command=lambda: saveRefTime(refTimeEnt.get()))
    # refTimeBtn.grid(row=0, column=2, columnspan=2, pady=10)

    # White List
    wListLbl = Label(settingsFrame, text="White List(단어)")
    wListLbl.grid(row=1, column=0)

    wListEnt = Entry(settingsFrame)
    wListEnt.grid(row=1, column=1)

    wListBtn = Button(settingsFrame, text="Append", command=lambda: appendWhiteList(wListEnt.get(), tree))
    wListBtn.grid(row=1, column=2, columnspan=2, pady=10)

    wListDelEnt = Entry(settingsFrame)
    wListDelEnt.grid(row=2, column=1)

    wListDelBtn = Button(settingsFrame, text="Delete", command=lambda: delWhiteList(wListDelEnt.get(), tree))
    wListDelBtn.grid(row=2, column=2, columnspan=2, pady=10)

    # Black List
    bListLbl = Label(settingsFrame, text="Black List (단어)")
    bListLbl.grid(row=3, column=0)

    bListEnt = Entry(settingsFrame)
    bListEnt.grid(row=3, column=1)

    bListBtn = Button(settingsFrame, text="Append", command=lambda: appendBlackList(bListEnt.get(), tree))
    bListBtn.grid(row=3, column=2, columnspan=2, pady=10)

    bListDelEnt = Entry(settingsFrame)
    bListDelEnt.grid(row=4, column=1)

    bListDelBtn = Button(settingsFrame, text="Delete", command=lambda: delBlackList(bListDelEnt.get(), tree))
    bListDelBtn.grid(row=4, column=2, columnspan=2, pady=10)

    # treeview

    tree = ttk.Treeview(settingsFrame, columns=('White List', 'Black List'), displaycolumns=('White List', 'Black List'), show='headings')

    tree.heading('White List', text='White List')
    tree.heading('Black List', text='Black List')

    tree.grid(row=5, column=0, columnspan=4)

    # save button

    saveBtn = Button(settingsFrame, text="Save", command=lambda: saveSettings(refTimeEnt.get()))
    saveBtn.grid(row=6, column=0, columnspan=4, pady=10)

    notificateLbl = Label(settingsFrame, text="저장 및 새로고침 후 적용됩니다! (개선 예정)")
    notificateLbl.grid(row=7, column=0, columnspan=4, pady=10)

    # Load the settings
    loadSettings()
    refList(tree)
    refTimeEnt.insert(0, int(settings[0]))

    settingsWindow.mainloop()

def appendWhiteList(word, tree) :
    settings[1].append(word)
    refList(tree)

def appendBlackList(word, tree) :
    settings[2].append(word)
    refList(tree)

def delWhiteList(targetWord, tree) :
    for word in settings[1] :
        if targetWord == word :
            settings[1].remove(word)
            refList(tree)

def delBlackList(targetWord, tree) :
    for word in settings[2] :
        if targetWord == word :
            settings[2].remove(word)
            refList(tree)

def loadSettings() :
    global settings
    filename = "settings.txt"
    if os.path.exists(filename) :
        settings = [10, [], []]
        with open(filename, 'r', encoding='utf-8') as f :
            while True :
                line = f.readline()
                if line == "!White List\n" : break
                settings[0] = int(str(line)[:-1])
            while True :
                line = f.readline()
                if line == "!Black List\n" : break
                settings[1].append(str(line)[:-1])
            while True :
                line = f.readline()
                if line == "" : break
                settings[2].append(str(line)[:-1])

def saveSettings(refreshTime) :
    settings[0] = refreshTime
    filename = "settings.txt"
    with open(filename, "w", encoding='utf-8') as f :
        while True :
            f.write(str(settings[0]) + "\n")
            f.write("!White List\n")
            for word in settings[1] :
                f.write(word + "\n")
            f.write("!Black List\n")
            for word in settings[2] :
                f.write(word + "\n")
            break
    settingsWindow.destroy()