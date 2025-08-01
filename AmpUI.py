from tkinter import *
import AudioManupulator

def play():
    AudioManupulator.play("World of Terminal.wav")

root = Tk()
root.title("Audio Amplifier")
root.geometry("600x250")

rectangle = Frame(root, width=100, height=50, bg="blue")
rectangle.place(x=50, y=50)

b = Button(root, text="Play", font=("Arial", 15), command=play).pack(pady=20)



root.mainloop()