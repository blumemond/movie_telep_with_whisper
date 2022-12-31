import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import threading as th

lock = th.Lock()

class VideoPlayer(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master,width=1000,height=500)
        master.minsize(width=1000,height=500)
        self.config(bg="#000000")
        self.pack(expand=True,fill=tk.BOTH)
        self.video = None
        self.playing = False
        self.video_thread = None
        self.create_video_button()

    def create_video_button(self):
        self.video_button = tk.Button(
            self,
            width = 100,
            height = 25,
            bg="#DDDDDD",
            relief="flat",
            command = self.push_play_button,
        )
        self.video_button.pack(expand=True,fill=tk.BOTH)

    def get_video(self,path):
        self.video = cv2.VideoCapture(path)

    def push_play_button(self):
        if self.video == None:
            messagebox.showerror('エラー','動画データがありません')
            return

        self.playing = not self.playing
        if self.playing:
            self.video_thread = th.Thread(target=self.video_frame_timer)
            self.video_thread.setDaemon(True)
            self.video_thread.start()            
        else:
            self.video_thread = None 

    def next_frame(self):
        global lock
        lock.acquire()
        ret, self.frame = self.video.read()
        if not ret:
            messagebox.showerror("エラー","次のフレームがないので停止します")
            self.playing = False
        else:
            rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb)
            x = self.video_button.winfo_width()/pil.width
            y = self.video_button.winfo_height()/pil.height
            ratio = x if x<y else y #三項演算子 xとyを比較して小さい方を代入
            pil = pil.resize((int(ratio*pil.width),int(ratio*pil.height)))
            image = ImageTk.PhotoImage(pil)
            self.video_button.config(image=image)
            self.video_button.image = image
        lock.release()

    def video_frame_timer(self):
        while self.playing:
            self.next_frame()

if __name__ == "__main__":
    root = tk.Tk()
    path = "/Users/naoki_sakano/Desktop/001_ZIAAAA001_M001_津野さんプロト１.mp4"
    app = VideoPlayer(master=root)
    app.get_video(path)
    root.mainloop()