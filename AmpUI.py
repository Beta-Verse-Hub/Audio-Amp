#-- Imports --#
from tkinter import *
from time import sleep
from threading import Thread
import AudioManupulator


#-- Global Variables --#
playMusic = False


#-- Functions --#
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
root.geometry("1300x700+0+0")


#-- Thread --#
mainAudioThread = Thread(target=mainThread, daemon=True)
mainAudioThread.start()


#-- Frames --#
rectangle = Frame(root, width=1300, height=700, bg="grey")
rectangle.place(x=0, y=0)

rectangle2 = Frame(root, width=650, height=250, bg="#383838")
rectangle2.place(x=325, y=400)

rectangle3 = Frame(root, width=650, height=150, bg="#383838")
rectangle3.place(x=325, y=50)

rectangle4 = Frame(root, width=150, height=600, bg="#383838")
rectangle4.place(x=50, y=50)

rectangle5 = Frame(root, width=150, height=600, bg="#383838")
rectangle5.place(x=1100, y=50)

#-- Labels --#
name = Label(rectangle, text="Audio Amplifier", font=("Arial", 30))
name.place(x=520, y=300)


#-- Buttons --#

# Play
playButton = Button(rectangle3, text="Play", font=("Arial", 15), command=play,  width=10, height=3)
playButton.place(x=330, y=35)

# Stop
stopButton = Button(rectangle3, text="Stop", font=("Arial", 15), command=AudioManupulator.stop,  width=10, height=3)
stopButton.place(x=460, y=35)


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


#-- Overload --#
overloadLabel = Frame(rectangle2, width=120, height=120)
overloadLabel.place(x=500,y=60)


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


#-- Main Loop --#
root.mainloop()
