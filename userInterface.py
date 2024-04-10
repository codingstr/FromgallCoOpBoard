import Crawling
import Settings

import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Label, Button, VERTICAL, N, S, E, W
import webbrowser

Settings.loadSettings()

refTime = int(Settings.settings[0])
refTimeLeft = refTime

def enable_scrolling(event):
    canvas.bind_all("<MouseWheel>", on_mousewheel)

def disable_scrolling(event):
    canvas.unbind_all("<MouseWheel>")

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def autoRefresh() :
    global refTimeLeft
    global refTime

    autoRefTimeLbl.config(text="refresh in " + str(refTimeLeft) + " seconds")

    refTimeLeft -= 1
    if refTimeLeft <= 0 :
        refresh()

    root.after(1000, autoRefresh)

def refresh():
    global refTimeLeft
    global refTime

    # Delete existing rectangle groups
    for widget in frame.winfo_children():
        widget.destroy()


    # Create new rectangle groups
    startIdx = Crawling.getNewPosts()
    for post in list(reversed(Crawling.postsInfo)):

        isWhiteListed = False
        isBlackListed = False

        # White List Check
        if len(Settings.settings[1]) > 0 :
            for word in Settings.settings[1] :
                if word in post.title or word in post.content :
                    isWhiteListed = True
                    break
        
        # Black List Check
        if len(Settings.settings[2]) > 0 :
            for word in Settings.settings[2] :
                if word in post.title or word in post.content :
                    isBlackListed = True
                    break

        if isBlackListed :
            continue

        group = Frame(frame)
        group.grid(pady=10, sticky=E+W)

        contentWidth = 100
        infoWidth = 10

        rectangle1 = Frame(group, width=contentWidth,  bd=1, relief='solid')
        rectangle1.grid(row=0, column=0, padx=5, sticky=E+W)

        if isWhiteListed:
            Label(rectangle1, text=post.title, width=contentWidth, anchor='w', fg='orange').grid(row=0, column=0)
        else:
            Label(rectangle1, text=post.title, width=contentWidth, anchor='w').grid(row=0, column=0)
        Label(rectangle1, text="\n"+post.content, width=contentWidth, anchor='w', justify='left').grid(row=1, column=0)

        rectangle2 = Frame(group, width=infoWidth, bd=1, relief='solid')
        rectangle2.grid(row=0, column=1, padx=5, sticky=E+W)

        Label(rectangle2, text=post.writer, width=infoWidth).grid(row=0, column=0)
        Label(rectangle2, text=post.date, width=infoWidth).grid(row=1, column=0)
        postUrl = "https://gall.dcinside.com/mgallery/board/view/?id=fromsoftware&no=" + str(post.num)
        Button(rectangle2, text=post.num, width=infoWidth, command=lambda postUrl=postUrl: webbrowser.open(postUrl)).grid(row=2, column=0)

    # Update the scrollregion of the canvas after widgets are placed
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

    refTime = int(Settings.settings[0])
    refTimeLeft = refTime
    canvas.yview_moveto(0)
    print("refreshed!")

def openSetting() :
    Settings.openSettingsWindow()


Crawling.getNewPosts()

root = tk.Tk()

root.title("Fromgallery Co-Op Board")

# Set the main window size
root.geometry("1000x700")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Create a canvas and a vertical scrollbar
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='center')

# Pack everything
canvas.grid(row=0, column=0, sticky=N+S+E+W)
scrollbar.grid(row=0, column=1, sticky=N+S)

canvas.bind("<Enter>", enable_scrolling)
canvas.bind("<Leave>", disable_scrolling)

refButton = tk.Button(root, text="Refresh", command=refresh)
refButton.grid(row=1, column=0)

settingsButton = tk.Button(root, text="Settings", command=openSetting)
settingsButton.grid(row=1, column=1)

autoRefTimeLbl = tk.Label(root, text="refresh in " + str(refTimeLeft) + " seconds")
autoRefTimeLbl.grid(row=2, column=0)

notificationLbl = tk.Label(root, text="zuzione@gmail.com / https://github.com/codingstr")
notificationLbl.grid(row=3, column=0)

refresh()
autoRefresh()
root.mainloop()
