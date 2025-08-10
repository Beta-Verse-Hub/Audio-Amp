#-- Imports --#
from tkinter import *
from PIL import Image as pilImage, ImageTk as pilImageTk
from time import sleep
from threading import Thread
import AudioManupulator


#-- Global Variables --#
global playMusic, ampSwitch
playMusic = False
ampSwitch = False


#-- Functions --#
def toggle_switch(switchButton):
    """
    Toggles the switch button between on and off states.

    Parameters
    ----------
    switchButton : tkinter.Button
        The switch button to toggle.

    Notes
    -----
    This function toggles the switch button between on and off states by
    updating the image of the button and the global variable `ampSwitch`.
    """
    global ampSwitch
    global switchImage
    global switchIndicator

    if ampSwitch:
        switchImage = pilImage.open("Assets/offSwitch.png")
        switchImage = switchImage.resize((96, 192))
        switchImage = pilImageTk.PhotoImage(switchImage)

        switchButton.config(image=switchImage)
        switchButton.image = switchImage

        switchIndicator.create_oval(40, 40, 80, 80, fill="#007700")

        ampSwitch = False
    else:
        switchImage = pilImage.open("Assets/onSwitch.png")
        switchImage = switchImage.resize((96, 192))
        switchImage = pilImageTk.PhotoImage(switchImage)

        switchButton.config(image=switchImage)
        switchButton.image = switchImage

        switchIndicator.create_oval(40, 40, 80, 80, fill="#00FF00")

        ampSwitch = True

def increaseBoostFactor(amount, factor):
    """
    Increases the boost factor for a given frequency range by a given amount.

    Parameters
    ----------
    amount : float
        The amount to increase the boost factor by.
    factor : str
        The frequency range to increase the boost factor for. Must be one of "bass", "mid", or "treble".

    Notes
    -----
    This function updates the boost factor for the given frequency range and
    updates the corresponding text entry box.
    """
    global midEntry, bassEntry, trebleEntry

    if factor == "bass":
        AudioManupulator.bass_boost_factor += amount
        bassEntry.delete(0, END)
        bassEntry.insert(0, AudioManupulator.bass_boost_factor)

    elif factor == "mid":
        AudioManupulator.mid_boost_factor += amount
        midEntry.delete(0, END)
        midEntry.insert(0, AudioManupulator.mid_boost_factor)

    elif factor == "treble":
        AudioManupulator.treble_boost_factor += amount
        trebleEntry.delete(0, END)
        trebleEntry.insert(0, AudioManupulator.treble_boost_factor)
    
    elif factor == "gain":
        AudioManupulator.gain_boost_factor += amount
        gainEntry.delete(0, END)
        gainEntry.insert(0, AudioManupulator.gain_boost_factor)

def play():
    """
    Sets the global variable `playMusic` to `True`.

    Notes
    -----
    This function is used to indicate that music playback should begin.
    """

    global playMusic
    playMusic = True

def mainThread():
    """
    Main thread that listens for the global variable `playMusic` to be set to
    `True`. When this happens, the thread plays the audio file "World of
    Terminal.wav" using the `AudioManupulator` module and sets `playMusic` to
    `False` again. The thread sleeps for 0.1 seconds between each check of the
    global variable.

    Notes
    -----

    This thread is used to control the playback of the audio file. When the
    user presses the play button, the `playMusic` variable is set to `True` and
    this thread plays the audio file. The thread continues to run in the
    background and listen for the `playMusic` variable to be set to `True`
    again. When the user closes the window, the thread exits since the window
    no longer exists.
    """
    global playMusic
    while root.winfo_exists():
        if playMusic:
            AudioManupulator.play("World of Terminal.wav")
            playMusic = False
        sleep(0.1)


#-- Main Window --#
root = Tk()
root.title("Audio Amplifier")
root.resizable(False, False)
window_width = 1300
window_height = 700
root.geometry(f"{window_width}x{window_height}+0+0")


#-- Thread --#
mainAudioThread = Thread(target=mainThread, daemon=True)
mainAudioThread.start()


#-- Frames --#
rectangle = Frame(root, bg="grey")
rectangle.place(relx=0, rely=0, relwidth=1, relheight=1)

rectangle2 = Frame(root, bg="#383838")
rectangle2.place(relx=325/window_width, rely=400/window_height, relwidth=650/window_width, relheight=250/window_height)

upperSectionSize = (325, 50)
rectangle3 = Frame(root, bg="#383838")
rectangle3.place(relx=upperSectionSize[0]/window_width, rely=upperSectionSize[1]/window_height, relwidth=650/window_width, relheight=150/window_height)

rectangle4 = Frame(root, bg="#383838")
rectangle4.place(relx=50/window_width, rely=50/window_height, relwidth=150/window_width, relheight=600/window_height)

rectangle5 = Frame(root, bg="#383838")
rectangle5.place(relx=1100/window_width, rely=50/window_height, relwidth=150/window_width, relheight=600/window_height)


#-- Buttons --#

# Play
playButton = Button(rectangle3, text="Play", font=("Arial", 15), command=play)
playButton.place(relx=265/upperSectionSize[0], rely=17/upperSectionSize[1], relwidth=200/window_width, relheight=250/window_height)

# Stop
stopButton = Button(rectangle3, text="Stop", font=("Arial", 15), command=AudioManupulator.stop)
stopButton.place(relx=200/upperSectionSize[0], rely=17/upperSectionSize[1], relwidth=200/window_width, relheight=250/window_height)


#-- Boost Buttons --#

# Mid
increaseMidButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(0.1, "mid"))
increaseMidButton.place(x=25,y=60)

decreaseMidButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-0.1, "mid"))
decreaseMidButton.place(x=25,y=140)

# Bass
increaseBassButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(0.1, "bass"))
increaseBassButton.place(x=145,y=60)

decreaseBassButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-0.1, "bass"))
decreaseBassButton.place(x=145,y=140)

# Treble
increaseTrebleButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(0.1, "treble"))
increaseTrebleButton.place(x=265,y=60)

decreaseTrebleButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-0.1, "treble"))
decreaseTrebleButton.place(x=265,y=140)

# Gain
increaseGainButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(0.1, "gain"))
increaseGainButton.place(x=385,y=60)

decreaseGainButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-0.1, "gain"))
decreaseGainButton.place(x=385,y=140)


#-- Sliders --#
masterVolumeSlider = Scale(rectangle4, from_=2.0, to=0.0, resolution=0.1, orient=VERTICAL, length=300, bg="#383838", fg="white", highlightthickness=0)
masterVolumeSlider.place(x=45, y=285)


#-- Labels --#
appName = Label(rectangle, text="Audio Amp", font=("Arial", 30))
appName.place(relx=530/window_width, rely=300/window_height)

# Master Volume
db2Label = Label(rectangle4, text="2+ db", font=("Arial", 10), bg="#383838", fg="white")
db2Label.place(x=90, y=285, width=35, height=20)

db1Label = Label(rectangle4, text="1+ db", font=("Arial", 10), bg="#383838", fg="white")
db1Label.place(x=90, y=425, width=35, height=20)

db0Label = Label(rectangle4, text="0+ db", font=("Arial", 10), bg="#383838", fg="white")
db0Label.place(x=90, y=565, width=35, height=20)


#-- Switches --#
switchImage = pilImage.open("Assets/offSwitch.png")
switchImage = switchImage.resize((96, 192))
switchImage = pilImageTk.PhotoImage(switchImage)

startSwitch = Button(rectangle5, image=switchImage, highlightthickness=0)
startSwitch.config(command=lambda: toggle_switch(startSwitch))
startSwitch.place(x=27, y=350, width=96, height=192)

overloadSwitchImage = pilImage.open("Assets/offSwitch.png")
overloadSwitchImage = overloadSwitchImage.resize((64, 128))
overloadSwitchImage = pilImageTk.PhotoImage(overloadSwitchImage)

overloadLabel = Button(rectangle2, image=overloadSwitchImage, highlightthickness=0)
overloadLabel.place(x=500, y=56, width=64, height=128)


#-- Indicators --#
overloadIndicator = Canvas(rectangle5, width=120, height=120, bg="#383838", highlightthickness=0)
overloadIndicator.create_oval(40, 40, 80, 80, fill="#770000")
overloadIndicator.place(x=15,y=155)

switchIndicator = Canvas(rectangle5, width=120, height=120, bg="#383838", highlightthickness=0)
switchIndicator.create_oval(40, 40, 80, 80, fill="#007700")
switchIndicator.place(x=15,y=15)

volumeIndicator = Canvas(rectangle4, width=30, height=250, bg="#383838", highlightthickness=0)
volumeIndicator.create_oval(0, 0, 30, 30, fill="#770000")
volumeIndicator.create_oval(0, 50, 30, 80, fill="#777700")
volumeIndicator.create_oval(0, 100, 30, 130, fill="#777700")
volumeIndicator.create_oval(0, 150, 30, 180, fill="#007700")
volumeIndicator.create_oval(0, 200, 30, 230, fill="#007700")
volumeIndicator.place(x=60,y=30)

#-- Entry Boxes --#

# Mid
midEntry = Entry(rectangle2, font=("Arial", 15), width=8)
midEntry.insert(0, AudioManupulator.mid_boost_factor)
midEntry.place(x=25,y=105)

# Bass
bassEntry = Entry(rectangle2, font=("Arial", 15), width=8)
bassEntry.insert(0, AudioManupulator.bass_boost_factor)
bassEntry.place(x=145,y=105)

# Treble
trebleEntry = Entry(rectangle2, font=("Arial", 15), width=8)
trebleEntry.insert(0, AudioManupulator.treble_boost_factor)
trebleEntry.place(x=265,y=105)

# Gain
gainEntry = Entry(rectangle2, font=("Arial", 15), width=8)
gainEntry.insert(0, AudioManupulator.gain_boost_factor)
gainEntry.place(x=385,y=105)

# Music Name
musicEntry = Entry(rectangle3, font=("Arial", 25))
musicEntry.place(relx=17/upperSectionSize[0],rely=17/upperSectionSize[1], relwidth=165/upperSectionSize[0], relheight=17/upperSectionSize[1])


#-- Main Loop --#
root.mainloop()
