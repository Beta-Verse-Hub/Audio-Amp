#-- Imports --#
from tkinter import *
from PIL import Image as pilImage, ImageTk as pilImageTk
from time import sleep, time
from threading import Thread
import os
import AudioManupulator


#-- Global Variables --#
overload_last_checked = None
overload_start_time = None
overload_duration_threshold = 3.0
overloaded = False
playMusic = False
ampSwitch = False


#-- Functions --#

def update_volume_indicator(rms_level):
    """
    Updates the volume indicator lights based on RMS audio level.
    """
    normalized = rms_level / 32768.0  # Convert to 0.0 - 1.0

    # There are 5 ovals; we'll turn on more as the volume increases
    thresholds = [0.1, 0.3, 0.5, 0.7, 0.9]  # For each light

    colors = []
    for t in thresholds:
        if normalized >= t:
            if t >= 0.9:
                colors.append("#FF0000")  # Red for high
                overloadIndicator.itemconfig(1, fill="#FF0000")
            elif t >= 0.7:
                colors.append("#FFFF00")  # Yellow for medium-high
                overloadIndicator.itemconfig(1, fill="#770000")
            else:
                colors.append("#00FF00")  # Green for low
                overloadIndicator.itemconfig(1, fill="#770000")
        else:
            colors.append("#333333")  # Off/dim

    # Check for overload
    global overload_start_time
    overload = normalized >= 0.9

    current_time = time()
    if overload:
        if overload_start_time is None:
            overload_start_time = current_time  # Start timing
        elif current_time - overload_start_time >= overload_duration_threshold:
            stop()  # Stop audio after prolonged overload
            overload_start_time = None  # Reset
            overloaded = True # Set overloaded flag
    else:
        overload_start_time = None

    # Update the ovals' colors in the canvas (thread-safe)
    def update_canvas():
        volumeIndicator.itemconfig(1, fill=colors[4])  # Top
        volumeIndicator.itemconfig(2, fill=colors[3])
        volumeIndicator.itemconfig(3, fill=colors[2])
        volumeIndicator.itemconfig(4, fill=colors[1])
        volumeIndicator.itemconfig(5, fill=colors[0])  # Bottom

    root.after(0, update_canvas)  # Run in UI thread

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

    if ampSwitch: # Switch off
        switchImage = pilImage.open("Assets/offSwitch.png")
        switchImage = switchImage.resize((96, 192))
        switchImage = pilImageTk.PhotoImage(switchImage)

        switchButton.config(image=switchImage)
        switchButton.image = switchImage

        switchIndicator.create_oval(40, 40, 80, 80, fill="#007700")

        stop()

        ampSwitch = False
    else: # Switch on
        switchImage = pilImage.open("Assets/onSwitch.png")
        switchImage = switchImage.resize((96, 192))
        switchImage = pilImageTk.PhotoImage(switchImage)

        switchButton.config(image=switchImage)
        switchButton.image = switchImage

        switchIndicator.create_oval(40, 40, 80, 80, fill="#00FF00")

        ampSwitch = True

def unoverload():
    global overloaded
    overloaded = False

def increaseBoostFactor(amount=1, factor="gain"):
    """
    Increases the boost factor for a given frequency range by the specified amount.

    Parameters
    ----------
    amount : int, optional
        The amount to increase the boost factor by. Defaults to 1.
    factor : str, optional
        The frequency range to increase the boost factor for. Can be one of
        "bass", "mid", "treble", or "gain". Defaults to "gain".

    Notes
    -----
    This function increases the boost factor for the specified frequency range
    by the specified amount and updates the corresponding text entry box with
    the new value. The boost factor is capped at 0 and 100.
    """
    global midLabel, bassLabel, trebleLabel, gainLabel

    if factor == "bass":
        AudioManupulator.bass_boost_factor = max(0, min(100, AudioManupulator.bass_boost_factor + amount))
        bassLabel.config(text=str(AudioManupulator.bass_boost_factor))

    elif factor == "mid":
        AudioManupulator.mid_boost_factor = max(0, min(100, AudioManupulator.mid_boost_factor + amount))
        midLabel.config(text=str(AudioManupulator.mid_boost_factor))

    elif factor == "treble":
        AudioManupulator.treble_boost_factor = max(0, min(100, AudioManupulator.treble_boost_factor + amount))
        trebleLabel.config(text=str(AudioManupulator.treble_boost_factor))

    elif factor == "gain":
        AudioManupulator.gain_boost_factor = max(0, min(100, AudioManupulator.gain_boost_factor + amount))
        gainLabel.config(text=str(AudioManupulator.gain_boost_factor))

def play():
    """
    Sets the global variable `playMusic` to `True`.

    Notes
    -----
    This function is used to indicate that music playback should begin.
    """

    if ampSwitch:
        global playMusic
        playMusic = True

def stop():
    """
    Stops the music playback and enables the text entry boxes.

    Notes
    -----
    This function is used to stop music playback and re-enable the text entry
    boxes for the boost factors. It calls the `stop` function from the
    `AudioManupulator` module to stop music playback and the `set_entries_state`
    function to enable the text entry boxes.
    """
    global volumeIndicator, overloadIndicator

    for i in range(5):
        volumeIndicator.itemconfig(i+1, fill="#333333")
    
    overloadIndicator.itemconfig(1, fill="#770000")

    AudioManupulator.stop()

def mainThread():
    """
    Main thread that runs in the background to control the music playback.

    This thread is responsible for checking if the music file exists and if
    playback should begin. If the file exists and playback should begin, it
    calls the `play` function from the `AudioManupulator` module to start music
    playback.

    It also updates the master volume, bass, mid, treble, and gain boost factors
    based on the values in the corresponding text entry boxes.

    Notes
    -----
    This function runs until the main window is closed.
    """
    global playMusic
    global musicEntry
    global masterVolumeSlider
    global midLabel, bassLabel, trebleLabel, gainLabel
    global overloadIndicator, overloaded

    while root.winfo_exists():
        if not os.path.exists(musicEntry.get()):
            playMusic = False
        
        if overloaded:
            overloadIndicator.itemconfig(1, fill="#770000")

        if playMusic and os.path.exists(musicEntry.get()) and ampSwitch and not overloaded:
            AudioManupulator.play(musicEntry.get(), volume_callback=update_volume_indicator)
            playMusic = False

        AudioManupulator.master_volume_factor = masterVolumeSlider.get()

        AudioManupulator.bass_boost_factor = int(bassLabel.cget("text"))
        AudioManupulator.mid_boost_factor = int(midLabel.cget("text"))
        AudioManupulator.treble_boost_factor = int(trebleLabel.cget("text"))
        AudioManupulator.gain_boost_factor = int(gainLabel.cget("text"))

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
stopButton = Button(rectangle3, text="Stop", font=("Arial", 15), command=stop)
stopButton.place(relx=200/upperSectionSize[0], rely=17/upperSectionSize[1], relwidth=200/window_width, relheight=250/window_height)

# Overload
overloadButtonImage = pilImage.open("Assets/pushButton.png")
overloadButtonImage = overloadButtonImage.resize((128, 128))
overloadButtonImage = pilImageTk.PhotoImage(overloadButtonImage)

overloadButton = Button(rectangle2, image=overloadButtonImage, highlightthickness=0)
overloadButton.place(x=500, y=56, width=128, height=128)


#-- Boost Buttons --#

# Mid
increaseMidButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(1, "mid"))
increaseMidButton.place(x=25,y=60)

decreaseMidButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-1, "mid"))
decreaseMidButton.place(x=25,y=140)

# Bass
increaseBassButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(1, "bass"))
increaseBassButton.place(x=145,y=60)

decreaseBassButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-1, "bass"))
decreaseBassButton.place(x=145,y=140)

# Treble
increaseTrebleButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(1, "treble"))
increaseTrebleButton.place(x=265,y=60)

decreaseTrebleButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-1, "treble"))
decreaseTrebleButton.place(x=265,y=140)

# Gain
increaseGainButton = Button(rectangle2, text="^", width=12, height=2, command=lambda: increaseBoostFactor(1, "gain"))
increaseGainButton.place(x=385,y=60)

decreaseGainButton = Button(rectangle2, text="v", width=12, height=2, command=lambda: increaseBoostFactor(-1, "gain"))
decreaseGainButton.place(x=385,y=140)


#-- Sliders --#
masterVolumeSlider = Scale(rectangle4, from_=2.0, to=0.0, resolution=0.1, orient=VERTICAL, length=300, bg="#383838", fg="#FFFFFF", highlightthickness=0)
masterVolumeSlider.configure(activebackground="#FF0000")
masterVolumeSlider.set(AudioManupulator.master_volume_factor)
masterVolumeSlider.place(x=45, y=285)


#-- Labels --#

# App Name
appName = Label(rectangle, text="Audio Amp", font=("Arial", 30))
appName.place(relx=530/window_width, rely=300/window_height)

# Mid
midLabel = Label(rectangle2, font=("Arial", 15), width=8, text=str(AudioManupulator.mid_boost_factor), bg="#383838", fg="white")
midLabel.place(x=25, y=105)

# Bass
bassLabel = Label(rectangle2, font=("Arial", 15), width=8, text=str(AudioManupulator.bass_boost_factor), bg="#383838", fg="white")
bassLabel.place(x=145, y=105)

# Treble
trebleLabel = Label(rectangle2, font=("Arial", 15), width=8, text=str(AudioManupulator.treble_boost_factor), bg="#383838", fg="white")
trebleLabel.place(x=265, y=105)

# Gain
gainLabel = Label(rectangle2, font=("Arial", 15), width=8, text=str(AudioManupulator.gain_boost_factor), bg="#383838", fg="white")
gainLabel.place(x=385, y=105)

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


#-- Indicators --#
overloadIndicator = Canvas(rectangle5, width=120, height=120, bg="#383838", highlightthickness=0)
overloadIndicator.create_oval(40, 40, 80, 80, fill="#770000")
overloadIndicator.place(x=15,y=155)

switchIndicator = Canvas(rectangle5, width=120, height=120, bg="#383838", highlightthickness=0)
switchIndicator.create_oval(40, 40, 80, 80, fill="#007700")
switchIndicator.place(x=15,y=15)

volumeIndicator = Canvas(rectangle4, width=30, height=250, bg="#383838", highlightthickness=0)
for i in range(5):
    volumeIndicator.create_oval(0, i * 50, 30, i*50+30, fill="#333333")
volumeIndicator.place(x=60,y=30)

#-- Entry Boxes --#

# Music Name
musicEntry = Entry(rectangle3, font=("Arial", 25))
musicEntry.place(relx=17/upperSectionSize[0],rely=17/upperSectionSize[1], relwidth=165/upperSectionSize[0], relheight=17/upperSectionSize[1])


#-- Main Loop --#
root.mainloop()
