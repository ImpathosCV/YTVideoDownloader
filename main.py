from pytube import YouTube
from PIL import ImageTk
import PIL.Image
from tkinter import *
import ttkbootstrap as ttk
from playsound import playsound
import threading
import requests as req
import time
import os

IllegalChars = ['#', '%', '&', '{', '}', '<', '>', '*', '?', '/', '$', '!', "'", '"', ':', '@', '+', '`', '|', '=', '^', '[', ']', '~', '=', '.']
Queue = []
MainDirectory = './YTVideos'
Running = False
OutputStr = None
InputStr = None
GooseHonk = './Honk.mp3'

def ReplaceString(string, chars, replace):
    for i in chars:
        string = string.replace(i, replace)
    return string

def ValidateUrl(Url):
    ValidationUrl = f'https://www.youtube.com/oembed?url={Url}'
    Request = req.get(ValidationUrl)

    return Request.status_code == 200

def CheckQueue():
    global Running
    ChangeOutputString('Checking Queue')
    if not Queue:
        Running = False
        return ChangeOutputString('All Finished')
    else:
        Running = True
        ChangeOutputString('Downloading Videos')
        LoopThread = threading.Thread(target = RunLoop)
        LoopThread.start()
        LoopThread.join()
        CheckQueue()

def AddToQueue():
    Url = InputStr.get()
    InputStr.set('')
    if ValidateUrl(Url):
        Queue.append(Url)
    else:
        return ChangeOutputString('Invalid Url')
    if not Running:
        CheckQueue()

def GetVideoData(Url):
    # ChangeOutputString('Getting Video Data')
    # print('GettingVideoData')
    VideoData = YouTube(Url)
    # print('VideoData')

    Youtuber = VideoData.author
    Youtuber = ReplaceString(Youtuber, IllegalChars, '')
    Youtuber = ReplaceString(Youtuber, [' '], '-')
    # print('Youtuber')

    VideoName = VideoData.title
    VideoName = ReplaceString(VideoName, IllegalChars, '')
    VideoName = ReplaceString(VideoName, [' '], '-')
    # print('VideoName')
    
    Video = VideoData.streams.get_highest_resolution()
    return {'Youtuber' : Youtuber, 'VideoName' : VideoName, 'Video' : Video}

def CreateDirs(MainPath, MainFolder, SubFolder):
    # ChangeOutputString('Creating Directories')
    # print('CreatingDirectories')
    if not os.path.exists(MainPath):
        os.makedirs(MainPath)
    MainFolderPath = os.path.join(MainPath, MainFolder)
    # print('MainFolderPath')
    if not os.path.exists(MainFolderPath):
        os.makedirs(MainFolderPath)
    SubFolderPath = os.path.join(MainFolderPath, SubFolder)
    # print('SubFolderPath')
    if not os.path.exists(SubFolderPath):
        os.makedirs(SubFolderPath)
    # print('FinishedDirectories')
    return {'ParentFolder' : MainFolderPath, 'ChildFolder' : SubFolderPath}

def ChangeOutputString(Text):
    Output.configure(text = Text)
    Window.update()

def Honk(*args):
    playsound(GooseHonk)

def RunLoop():
    for Url in Queue:
        # ChangeOutputString('Getting Video Data')
        # print('RunningLoop')
        VideoData = GetVideoData(Url)
        Youtuber = VideoData['Youtuber']
        VideoName = VideoData['VideoName']
        Video = VideoData['Video']
        # print('SetVariables')

        # ChangeOutputString('Creating Directories')
        Directories = CreateDirs(MainDirectory, Youtuber, VideoName)
        # print(f'Downloading {VideoName} By {Youtuber}')
        # ChangeOutputString(f'Downloading {VideoName} By {Youtuber}')

        Video.download(Directories['ChildFolder'])
        Queue.remove(Url)
        # print('Downloaded')


Window = ttk.Window(themename = 'cyborg')
Window.title('Video Downloader')
Window.geometry('400x150')

# Title
TitleLabel = ttk.Label(master = Window, text = 'Insert Video Link', font = 'Calibri 12 bold')
TitleLabel.pack(pady = 10)

# Input, Container, Button
Container = ttk.Frame(master = Window)
InputStr = StringVar()
InputField = ttk.Entry(master = Container, font = 'Calibri 6', width = 35, textvariable = InputStr)
Button = ttk.Button(master = Container, text = 'AddToQueue', command = AddToQueue)
InputField.pack(side = 'left', padx = 10, ipady = 5)
Button.pack(side = 'left')
Container.pack(pady = 10)

# Output
Output = ttk.Label(master = Window, font = 'Calibri 8', text = '')
Output.pack(pady = 5)

# Goose
GoosePngOpen = PIL.Image.open('Goose.png')
NewSize = (43, 43)
GoosePngOpen = GoosePngOpen.resize(NewSize)
GoosePng = ImageTk.PhotoImage(GoosePngOpen)
Goose = ttk.Label(master = Window, image = GoosePng)
Goose.place(rely = 1, relx = 0.98, x = 0, y = 0, anchor = SE)
Goose.photo = GoosePng
Goose.bind("<Button-1>", lambda Event: threading.Thread(target=Honk).start())

# Run
Window.resizable(False, False)
Window.mainloop()
