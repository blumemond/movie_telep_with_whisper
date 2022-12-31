import os, sys
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
# import movie
import tkinter as tk
import whisper
import srt
from srt import Subtitle
from datetime import timedelta
from moviepy import editor
from moviepy.video.io.VideoFileClip import VideoFileClip
import os.path as op

subtitles = []
subtitleNumber = int(1)

# class View():
#     def __init__(self, app, model):
#         self.master = app
#         self.model = model

#         # アプリ内のウィジェットを作成
#         self.create_widgets()

#     def create_widgets(self):
#         canvas_width  = 400
#         canvas_height = 600

#         # キャンバスとボタンを配置するフレームの作成と配置
#         self.main_frame = tkinter.Frame(self.master)
#         self.main_frame.pack()

#         # キャンバスを配置するフレームの作成と配置
#         self.canvas_frame = tkinter.Frame(self.main_frame)
#         self.canvas_frame.grid(column=1, row=1)

#         # テロップ用テキストボックスを配置するフレームの作成と配置
#         self.canvas_frame = tkinter.Frame(self.main_frame)
#         self.canvas_frame.grid(column=1, row=2)

#         # ユーザ操作用フレームの作成と配置
#         self.operation_frame = tkinter.Frame(self.main_frame)
#         self.operation_frame.grid(column=2, row=1)

#         # キャンバスの作成と配置
#         self.canvas = tkinter.Canvas(
#             self.canvas_frame,
#             width=canvas_width,
#             height=canvas_height,
#             bg="#EEEEEE",
#         )
#         self.canvas.pack()

#         # ファイル読み込みボタンの作成と配置
#         self.load_button = tkinter.Button(self.operation_frame, text="動画選択")
#         self.load_button.pack()


#選択された動画の拡張子を判別し、動画ならTrue、動画でないならFlaseを返す
def extensionCheck(filePath):
    filePath = str(filePath)
    if filePath.endswith((".avi", ".mp4", ".mov", ".mov", ".mwv", ".avchd")):
        return True
    else:
        return False


def backButton_clicked():
    global subtitleNumber
    saveSubtitle()
    if subtitleNumber >= 1:
        subtitleNumber = subtitleNumber - 1
        subtitleBox.delete('1.0', 'end')
        subtitleBox.insert('1.0', subtitles[subtitleNumber][1])
    else:
        return


def nextButton_clicked():
    global subtitleNumber
    saveSubtitle()
    if subtitleNumber < len(subtitles) - 1:
        subtitleNumber = subtitleNumber + 1
        subtitleBox.delete('1.0', 'end')
        subtitleBox.insert('1.0', subtitles[subtitleNumber][1])
    else:
        return


def saveSubtitle():
    subtitles[subtitleNumber][1] = subtitleBox.get("1.0", "end")


# 参照ボタンのイベント
# button1クリック時の処理
def button1_clicked():
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    # file1.set(filepath)
    extensionFlag = extensionCheck(filepath)
    if extensionFlag:
        pathText["text"] = filepath
    else:
        messagebox.showinfo('拡張子エラー',
                            '選択されたファイルは動画ではありません。\n動画ファイルを選択しなおしてください。')


# button2クリック時の処理
def getSbutitleButton_clicked():
    getSubTitles(pathText["text"])
    print(subtitles)


def button3_clicked():
    result = subtitleBox.get("1.0", "end")
    print(result)


#whisperで取得した文字起こしデータをSRT形式のリストに追加する
def add_line(s):
    new_s = s
    s_count = len(s)
    s_max_count = 15
    if s_count >= s_max_count:
        if (s_count - s_max_count) >= 3:
            # 15文字以上、かつ、2行目が3文字以上あれば、改行する
            # つまり、18文字以上であれば、15文字で改行する
            new_s = s[:s_max_count] + "\n" + s[s_max_count:]

    return new_s


def getSubTitles(path):
    global subtitleNumber
    model = whisper.load_model("medium")
    result = model.transcribe(path)
    segments = result["segments"]
    print(segments)
    print("*" * 100)
    for data in segments:
        index = data["id"] + 1
        start = data["start"]
        end = data["end"]
        text = add_line(data["text"])
        sub = [(start, end), text]
        subtitles.append(sub)
    print(subtitles)
    subtitleBox.delete('1.0', 'end')
    subtitleBox.insert('1.0', subtitles[0][1])
    subtitleNumber = int(0)

    # video = VideoFileClip(pathText["text"])
    # annotated_clips = [
    #     annotate(video.subclip(from_t, to_t), txt)
    #     for (from_t, to_t), txt in subs
    # ]  #動画と字幕を繋げる処理
    # final_clip = editor.concatenate_videoclips(annotated_clips)
    # final_clip.write_videofile("movie_withSubtitle.mp4")


#字幕の設定関数
def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    #Writes a text at the bottom of the clip.
    txtclip = editor.TextClip(txt,
                              fontsize=fontsize,
                              font=font,
                              color=txt_color)
    cvc = editor.CompositeVideoClip(
        [clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)


def main():
    # rootの作成
    root = Tk()
    root.title('WhisperAutoSubtitleMaker')
    root.resizable(False, False)

    #手順1の作成
    #動画パスを取得する
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(sticky=tk.W)
    Title1 = ttk.Label(
        frame1,
        text="手順１：動画ファイルを選択する",
        font=("Helvetica", "20", "bold"),
    )
    Title1.grid(column=1, row=0)

    global pathText
    pathText = ttk.Label(
        frame1,
        text="",
        font=("Helvetica", "10"),
    )
    pathText.grid(column=1, row=1)

    button1 = ttk.Button(frame1, text=u'選択', command=button1_clicked)
    button1.grid(column=2, row=1)

    #手順2の作成
    #Whisperを実行する
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(sticky=tk.W)
    Title2 = ttk.Label(
        frame2,
        text="手順２：自動文字起こしをする(10-20分ほどかかります)",
        font=("Helvetica", "20", "bold"),
    )
    Title2.grid(sticky=tk.W)

    button2 = ttk.Button(frame2,
                         text=u'自動文字起こしを実行する',
                         command=getSbutitleButton_clicked)
    button2.grid()

    #手順3の作成
    #動画の表示領域を作成する
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid()

    #手順4の作成
    #自動文字起こしの編集画面を表示する
    frame4 = ttk.Frame(root, padding=10)
    frame4.grid(sticky=tk.W)
    Title3 = ttk.Label(
        frame4,
        text="手順3：作成されたテロップのチェック＆修正をする",
        font=("Helvetica", "20", "bold"),
    )
    Title3.grid(column=1, row=0)

    # キャンバスの作成と配置
    canvas = tk.Canvas(
        frame4,
        width=500,
        height=300,
        background="#afafb0",
    )
    canvas.grid(column=1, row=1)

    Title4 = ttk.Label(
        frame4,
        text="字幕",
        font=("Helvetica", "20"),
    )
    Title4.grid(column=1, row=2)

    global subtitleBox
    subtitleBox = tk.Text(frame4, width=50, height=10)
    subtitleBox.grid(column=1, row=3)

    button3 = ttk.Button(frame4, text=u'テスト', command=button3_clicked)
    button3.grid(column=1, row=4)

    #手順5の作成
    #テロップ間を移動する
    frame5 = ttk.Frame(root, padding=10)
    frame5.grid(sticky=tk.W)
    button4 = ttk.Button(frame5, text=u'戻る', command=backButton_clicked)
    button4.pack(side=tk.LEFT, anchor=tk.CENTER)
    button5 = ttk.Button(frame5, text=u'次へ', command=nextButton_clicked)
    button5.pack(side=tk.LEFT, anchor=tk.CENTER)

    #手順6の作成
    #動画のエンコードを実行する
    frame6 = ttk.Frame(root, padding=10)
    frame6.grid(sticky=tk.W)
    Title5 = ttk.Label(
        frame6,
        text="手順4：完成したテロップで動画を作成する",
        font=("Helvetica", "20", "bold"),
    )
    Title5.grid()

    root.mainloop()


if __name__ == '__main__':
    main()