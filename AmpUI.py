from tkinter import *
from time import sleep
from threading import Thread
import AudioManupulator

playMusic = False

def play():
    global playMusic
    playMusic = True

def mainThread():
    global playMusic
    while root.winfo_exists():
        if playMusic:
            AudioManupulator.play("World of Terminal.wav")
            playMusic = False
        sleep(0.1)

root = Tk()
root.title("Audio Amplifier")
root.geometry("600x320")

mainAudioThread = Thread(target=mainThread, daemon=True)
mainAudioThread.start()

rectangle = Frame(root, width=600, height=180, bg="grey")
rectangle.place(x=0, y=0)

rectangle2 = Frame(root, width=600, height=140, bg="#383838")
rectangle2.place(x=0, y=180)

name = Label(rectangle, text="Audio Amplifier", font=("Arial", 15))
name.place(x=234, y=100)

playButton = Button(rectangle2, text="Play", font=("Arial", 15), command=play,  width=8, height=2)
playButton.place(x=300, y=20)

stopButton = Button(rectangle2, text="Stop", font=("Arial", 15), command=AudioManupulator.stop,  width=8, height=2)
stopButton.place(x=200, y=20)

increaseBassButton = Button(rectangle, text="^", width=8, height=1)
increaseBassButton.place(x=10,y=120)

decreaseBassButton = Button(rectangle, text="v", width=8, height=1)
decreaseBassButton.place(x=10,y=150)

root.mainloop()