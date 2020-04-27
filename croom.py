'''
@ All copy right is reserved for CRoom team

Developer team:

Nourah Janbi
Sara Alahmadi 
Sahar Omer
Ebtesam Alomari
Nada Saad

April 2020
'''

import tkinter
from tkinter import *
import multiprocessing
from playsound import playsound
import cv2
from PIL import Image, ImageTk 
import time
import numpy as np
import pyglet

class App:
    def __init__(self, window, window_title):
        #class =1  classesview=0  classfinish=2
        pyglet.font.add_file('GE Dinar One Medium.ttf')
        
        self.windowID=0
        #main window setting
        self.window = window
        self.window.title(window_title)
        self.window.geometry('860x600')
        self.window.configure(bg='white')
        
        
        #control variavle
        self.cam_is_on=True
        self.mic_is_on=False
        self.audio_is_on=True
        self.hand_is_up=False
        
        self.startWatching=False
        self.startLeft=False
        self.endLeft=False
        self.countLeft=0
        
        self.startLose=False
        self.endLose=False
        
        self.id=0
        
        self.startExit=False
        self.soundProcess= None # no sound process running
        self.classSoundProcess= None # no sound process running
        
        #logo
        window.iconbitmap('imges\\croom.ico')
        #self.logo_image = (Image.open("imges\\croom.png")).resize((50, 50), Image.ANTIALIAS) 
        #self.logo_image=ImageTk.PhotoImage(image=self.logo_image)
        
        
        #camera source
        self.video_source = 0
        
        self.classesFrame=Frame(self.window, bg="white")
        self.classesFrame.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        
        #self.logolabel = Label(self.classesFrame, image=self.logo_image,bg='white')
        #self.logolabel.grid(row=0, column=2,sticky=E)
        
        self.label2 = Label(self.classesFrame,text=" الجــــــدول الدراســـــي ", bg="white",fg="#FAA929",highlightthickness=0,font=("GE Dinar One", 20))
        self.label2.grid(row=0, column=0, columnspan=3)
        
        
        self.live_class =Image.open("imges\\math.png").resize((450, 60), Image.ANTIALIAS) 
        self.live_class= ImageTk.PhotoImage(image=self.live_class)
        self.livelabel = Label(self.classesFrame, image=self.live_class,bg='white')
        self.livelabel.grid(ipadx=180,ipady=40, row=1, column=0,columnspan=3)
        
        self.livelabel.bind("<Button-1>",lambda x:self.startClasslabel_click())
        
        #english
        self.e_class1 =Image.open("imges\\all classes.png").resize((370,340), Image.ANTIALIAS) 
        self.e_class1= ImageTk.PhotoImage(image=self.e_class1)
        self.e_class1label = Label(self.classesFrame, image=self.e_class1,bg='white')
        self.e_class1label.grid(row=2, column=1, sticky=E)
        
          #add1
        self.chr_image = (Image.open("imges\\char.png")).resize((130, 200), Image.ANTIALIAS) 
        self.chr_image=ImageTk.PhotoImage(image=self.chr_image)
        self.chr_label = Label(self.classesFrame, image=self.chr_image,bg='white')
        self.chr_label.grid(row=2, column=2 ) 
        
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        
   
    #show main window
    def classes_frame(self):
        self.classesFrame=Frame(self.window, bg="white")
        self.classesFrame.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.label2 = Label(self.classesFrame,text=" C L A S S E S ", bg="white",fg="#FAA929",highlightthickness=0,font=("Helvetica", 20))
        self.label2.grid(row=0,column=1, columnspan=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        

     
    def startClasslabel_click(self):
        self.classesFrame.destroy()
        self.windowID=1
        self.class_frame()  
        
    #show class window                                  
    def class_frame(self):
        self.classWindowFrame=Frame(self.window, bg="white")
        self.classWindowFrame.pack()
        
        #point
        self.label3 = Label(self.classWindowFrame,text=" النقاط: 40 ", bg="white",highlightthickness=0,font=("GE Dinar One", 10))
        self.label3.grid(ipady=0, row=0, column=0, columnspan=2, sticky=W)       
        
        #class title
        self.label2 = Label(self.classWindowFrame,text=" عنوان الدرس : الرقم اثنــــان", bg="white",fg="#FAA929",highlightthickness=0,font=("GE Dinar One", 20))
        self.label2.grid( row=1, column=0)
        
        # top buttons
        self.buttonsframe=Frame(self.classWindowFrame, width=200, height=50, bg="white")
        self.buttonsframe.grid(row=1, column=1)
            
        #cam
        self.cam_on_image = (Image.open("imges\\camon.png")).resize((30, 30), Image.ANTIALIAS) 
        self.cam_on_image=ImageTk.PhotoImage(image=self.cam_on_image)
        self.cam_off_image = (Image.open("imges\\camoff.png")).resize((30, 30), Image.ANTIALIAS) 
        self.cam_off_image=ImageTk.PhotoImage(image=self.cam_off_image)
        
        self.camlabel = Label(self.buttonsframe, image=self.cam_on_image,bg='white')
        self.camlabel.grid(row=0, column=1, sticky=S)
        self.camlabel.bind("<Button-1>",lambda x:self.camlabel_click())
        
        #mic
        self.mic_on_image = (Image.open("imges\\mic.png")).resize((30, 30), Image.ANTIALIAS) 
        self.mic_on_image=ImageTk.PhotoImage(image=self.mic_on_image)
        self.mic_off_image = (Image.open("imges\\mic_muted.png")).resize((30, 30), Image.ANTIALIAS) 
        self.mic_off_image=ImageTk.PhotoImage(image=self.mic_off_image)
        
        self.miclabel = Label(self.buttonsframe, image=self.mic_off_image,bg='white')
        self.miclabel.grid(row=0, column=2, sticky=S)
        self.miclabel.bind("<Button-1>",lambda x:self.miclabel_click())
        
        #audio
        self.audio_on_image = (Image.open("imges\\audio.png")).resize((30, 30), Image.ANTIALIAS) 
        self.audio_on_image=ImageTk.PhotoImage(image=self.audio_on_image)
        self.audio_off_image = (Image.open("imges\\audio_muted.png")).resize((30, 30), Image.ANTIALIAS) 
        self.audio_off_image=ImageTk.PhotoImage(image=self.audio_off_image)
        
        self.audiolabel = Label(self.buttonsframe, image=self.audio_on_image,bg='white')
        self.audiolabel.grid(row=0, column=3, sticky=S)
        self.audiolabel.bind("<Button-1>",lambda x:self.audiolabel_click())

         #hand
        self.hand_up_image = (Image.open("imges\\handup.png")).resize((30, 30), Image.ANTIALIAS) 
        self.hand_up_image=ImageTk.PhotoImage(image=self.hand_up_image)
        self.hand_down_image = (Image.open("imges\\handdown.png")).resize((30, 30), Image.ANTIALIAS) 
        self.hand_down_image=ImageTk.PhotoImage(image=self.hand_down_image)
        
        self.handlabel = Label(self.buttonsframe, image=self.hand_down_image,bg='white')
        self.handlabel.grid(row=0, column=4, sticky=S)
        self.handlabel.bind("<Button-1>",lambda x:self.handlabel_click()) 
        
        #exit class
        self.exit_image = (Image.open("imges\\exit.png")).resize((30, 30), Image.ANTIALIAS) 
        self.exit_image=ImageTk.PhotoImage(image=self.exit_image)

        self.exitlabel = Label(self.buttonsframe, image=self.exit_image,bg='white')
        self.exitlabel.grid(row=0, column=5, sticky=S)
        self.exitlabel.bind("<Button-1>",lambda x:self.exitlabel_click()) 
        
        
        #teacher board 
        self.class_start=True
        self.board=MyVideoCapture(self,'sounds\\fast.mp4',650,500)  
        self.board_canvas = tkinter.Canvas(self.classWindowFrame, bg="white", width = self.board.width, height = self.board.height)
        self.board_canvas.grid(row=2, column=0, rowspan=3)
        self.classSoundProcess=multiprocessing.Process(target=playsound, args=("sounds\\class_fast.mp3",))
        self.classSoundProcess.start()

        #boardimg = Image.open("imges\\board.jpg")
        #boardimg = boardimg.resize((650, 500), Image.ANTIALIAS) 
        #self.board = ImageTk.PhotoImage(boardimg)
        #self.label1 = Label(self.classWindowFrame, image=self.board,borderwidth = 1, relief="sunken")
        #self.label1.image = self.board
        #self.label1.grid(row=2, column=0, rowspan=3, sticky=W)
        

         # chat and response frame
        self.chatframe=Frame(self.classWindowFrame, width=200, height=150, bg="white")
        self.chatframe.grid(row=3, column=1, sticky=E)
    
        # correct or wrong button
        correct_wrong_frame = tkinter.Frame(self.chatframe)
        self.correct_image = (Image.open("imges\\correct.png")).resize((70, 70), Image.ANTIALIAS) 
        self.correct_image=ImageTk.PhotoImage(image=self.correct_image)
        self.correctlabel = Label(correct_wrong_frame, image=self.correct_image,bg='white')
        self.correctlabel.grid(row=0, column=0)
        #self.correctlabel.bind("<Button-1>",lambda x:self.correctlabel_click()) 

        self.wrong_image = (Image.open("imges\\wrong.png")).resize((70, 70), Image.ANTIALIAS) 
        self.wrong_image=ImageTk.PhotoImage(image=self.wrong_image)
        self.correctlabel = Label(correct_wrong_frame, image=self.wrong_image,bg='white')
        self.correctlabel.grid(row=0, column=1)
        #self.correctlabel.bind("<Button-1>",lambda x:self.correctlabel_click()) 
        
        #correct_wrong_frame.grid(row=2, column=0,columnspan=3, sticky=S)
        
        #messages
        messages_frame = tkinter.Frame(self.chatframe)
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        self.msg_list = tkinter.Text(messages_frame, height=5, width=23, yscrollcommand=scrollbar.set)
        self.msg_list.tag_configure('right', justify='right')
        self.msg_list.insert(tkinter.END, "المعلمة:درس الرقم 2"+'\n','right')
        scrollbar.pack(side=tkinter.LEFT )
        self.msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
        messages_frame.grid(row=0, column=0, columnspan=3)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("اكتب الاجابة هنا")
        entry_field = tkinter.Entry(self.chatframe, textvariable=self.my_msg, justify=tkinter.RIGHT)
        entry_field.bind("<Return>", lambda x:self.send())
        entry_field.grid(row=1, column=2)
        send_button = tkinter.Button(self.chatframe, text="ارسل", command=lambda:self.send())
        send_button.grid(row=1, column=1)
        self.draw_image = (Image.open("imges\\draw.png")).resize((30, 30), Image.ANTIALIAS) 
        self.draw_image=ImageTk.PhotoImage(image=self.draw_image)
        self.drawlabel = Label(self.chatframe, image=self.draw_image,bg='white')
        self.drawlabel.grid(row=1, column=0, sticky=N+S+W+E)
        self.drawlabel.bind("<Button-1>",lambda x:self.draw(DrawWindow)) 


        #character
        # Create a canvas that can fit the above video source size
        self.charCanvas = tkinter.Canvas(self.classWindowFrame, width = 200, height = 200,bg='white',highlightthickness=0)
        self.charCanvas.grid(row=2, column=1)    
        self.girl_img = Image.open("imges\\girl.png")
        self.girl_img = self.girl_img.resize((200, 200), Image.ANTIALIAS) 
        self.girl_img=ImageTk.PhotoImage(image=self.girl_img)
        self.charImage = self.charCanvas.create_image(100, 100, anchor=tkinter.CENTER, image=self.girl_img)
        

        
        #kid live video
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self,self.video_source,200,220)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.classWindowFrame, bg="yellow", width = self.vid.width, height = self.vid.height,highlightthickness=0)
        self.canvas.grid(row=4, column=1)
        
    
        # @ text
        status= Label(self.classWindowFrame, text=" جميع الحقوق محفوظه لفريق كرووم",bg='white', highlightthickness=0,font=("GE Dinar One", 9))
        status.grid(row=5,column=0, columnspan=2)
        

    #show exit window
    def class_end_frame(self):
        self.classEndFrame=Frame(self.window, bg="white")
        self.classEndFrame.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        label2 = Label(self.classEndFrame,text=" أنتهــــــــى الفصل الدراســــي ", bg="white",fg="#FAA929",highlightthickness=0,font=("GE Dinar One", 20))
        label2.pack()
        #character
        # Create a canvas that can fit the above video source size
        self.charExitCanvas = tkinter.Canvas(self.classEndFrame,width=600, height= 300, bg='white',highlightthickness=0)
        self.charExitCanvas.pack()
        self.exit_girl_img = Image.open("imges\\lesson is end\\lesoonisend000.png")
        self.exit_girl_img = self.exit_girl_img.resize((200, 200), Image.ANTIALIAS) 
        self.exit_girl_img=ImageTk.PhotoImage(image=self.exit_girl_img)
        self.charExitImage = self.charExitCanvas.create_image(300,150, image=self.exit_girl_img)
        self.startExit=True
        self.id=100
         
        if self.soundProcess:
                self.soundProcess.terminate() #close the sound
        if self.classSoundProcess:
                self.classSoundProcess.terminate() #close the sound
        self.soundProcess=multiprocessing.Process(target=playsound, args=("sounds\\classisfinish.mp3",))
        self.soundProcess.start()


        # top buttons
        addframe=Frame(self.classEndFrame, bg="white",bd=1)
        addframe.pack(expand=tkinter.YES, fill=tkinter.X)
       
        label3 = Label(addframe,text="المتجــر ", bg="white",fg="#FAA929",highlightthickness=0,font=("GE Dinar One", 20))
        label3.grid(row=0, column=0,columnspan=5, sticky=SE)   
        
        buy_button = tkinter.Button(addframe, text="شـــراء", command=lambda:self.send())
        buy_button.grid(row=2, column=1,columnspan=4)
            
        #add1
        self.chr_image = (Image.open("imges\\char.png")).resize((130, 200), Image.ANTIALIAS) 
        self.chr_image=ImageTk.PhotoImage(image=self.chr_image)
        self.chr_label = Label(addframe, image=self.chr_image,bg='white')
        self.chr_label.grid(ipadx=70, row=1, column=0,rowspan=2, sticky=W) 
        
        #add1
        self.add1_image = (Image.open("imges\\add1.png")).resize((80, 80), Image.ANTIALIAS) 
        self.add1_image=ImageTk.PhotoImage(image=self.add1_image)
        self.add1_label = Label(addframe, image=self.add1_image,bg='white')
        self.add1_label.grid(ipadx=20,row=1, column=1, sticky=N+S+W+E)
        self.add1_label.bind("<Button-1>",lambda x:self.add1label_click())
                
        #add1
        self.add2_image = (Image.open("imges\\add2.png")).resize((80, 80), Image.ANTIALIAS) 
        self.add2_image=ImageTk.PhotoImage(image=self.add2_image)
        self.add2_label = Label(addframe, image=self.add2_image,bg='white')
        self.add2_label.grid(ipadx=20,row=1, column=2, sticky=N+S+W+E)
        self.add2_label.bind("<Button-1>",lambda x:self.add2label_click())
                #add1
        self.add3_image = (Image.open("imges\\add3.png")).resize((80, 80), Image.ANTIALIAS) 
        self.add3_image=ImageTk.PhotoImage(image=self.add3_image)
        self.add3_label = Label(addframe, image=self.add3_image,bg='white')
        self.add3_label.grid(ipadx=20,row=1, column=3, sticky=N+S+W+E)
                   
                    #add1
        self.add4_image = (Image.open("imges\\add4.png")).resize((80, 80), Image.ANTIALIAS) 
        self.add4_image=ImageTk.PhotoImage(image=self.add4_image)
        self.add4_label = Label(addframe, image=self.add4_image,bg='white')
        self.add4_label.grid(ipadx=20,row=1, column=4, sticky=N+S+W+E)
        
                   
                   
    def add1label_click(self): 
        self.chr_image = (Image.open("imges\\char_add1.png"))
        self.chr_image = self.chr_image.resize((130, 200), Image.ANTIALIAS) 
        self.chr_image=ImageTk.PhotoImage(image=self.chr_image)
        self.chr_label.configure(image=self.chr_image)
    
    def add2label_click(self): 
        self.chr_image = (Image.open("imges\\char_add2.png"))
        self.chr_image = self.chr_image.resize((130, 200), Image.ANTIALIAS) 
        self.chr_image=ImageTk.PhotoImage(image=self.chr_image)
        self.chr_label.configure(image=self.chr_image)
    
    def camlabel_click(self):
        # cam muted if was on
        if self.cam_is_on:
            self.cam_is_on=False
            self.camlabel.configure(image=self.cam_off_image)
        else:
            self.cam_is_on=True
            self.camlabel.configure(image=self.cam_on_image)
  
    def miclabel_click(self):
        # mic muted if was on
        if self.mic_is_on:
            self.mic_is_on=False
            self.miclabel.configure(image=self.mic_off_image)
        else:
            self.mic_is_on=True
            self.miclabel.configure(image=self.mic_on_image)
  
    def audiolabel_click(self):
        # audio muted if was on
        if self.audio_is_on:
            self.audio_is_on=False
            self.audiolabel.configure(image=self.audio_off_image)
            #if sound was playing also close it
            if self.soundProcess:
                self.soundProcess.terminate() #close the sound
        else:
            self.audio_is_on=True
            self.audiolabel.configure(image=self.audio_on_image)
        
    def exitlabel_click(self):
        self.classWindowFrame.destroy()
        self.windowID=2
        self.vid.__del__()
        self.board.__del__()
        self.class_end_frame()
        
    def handlabel_click(self):
        # hand if was up
        if self.hand_is_up:
            self.hand_is_up=False
            self.handlabel.configure(image=self.hand_down_image)
            #if sound was playing also close it
            if self.soundProcess:
                self.soundProcess.terminate() #close the sound
        else:
            self.hand_is_up=True
            self.handlabel.configure(image=self.hand_up_image)

    def send(self):
        self.msg_list.insert(tkinter.END, "أنا:"+self.my_msg.get()+'\n' ,'right')
       
        
        
    def draw(self,Win_class):
        global draw_window
        draw_window = tkinter.Toplevel(self.window)
        Win_class(draw_window,self)

    def getPhotoNumber(self,i,digit=3):
        #cearte str for the name of the photo
        if digit==2:
            if self.id<10:
                return("0"+str(i))
            else:
                return(str(i))
        else:
            if self.id<10:
                return("00"+str(i))
            elif self.id<100:
                return("0"+str(i))
            else:
                return(str(i))
        
    def update(self):
        
        if  self.windowID==1:
            if self.class_start:
                boardRet, boardFrame = self.board.get_frame()
                if boardRet:
                    self.boardPhoto = ImageTk.PhotoImage(image = Image.fromarray(boardFrame))
                    self.board_canvas.create_image(0, 0, image = self.boardPhoto, anchor = tkinter.NW)
                    
            #cheack the face
            # Get a frame from the video source
            facefound,ret, frame = self.vid.get_frame_face()
            if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            
                # change the character depend on face found or not
                if facefound:
                    #started wataching (stop left)
                    if self.startWatching:
                        if self.startLeft and  self.soundProcess:
                            self.soundProcess.terminate() #close the sound
                        self.startLeft=False #end the left as he back
                        self.endLeft=False
                        self.startLose=False
                        self.endLose=False
                        self.countLeft=0
                        #action we want when kids watching

                                                   
                        #get the photo and show
                        self.img = Image.open("imges\\blink\\blink"+self.getPhotoNumber(self.id,2)+".png")
                        self.img = self.img.resize((200, 200), Image.ANTIALIAS) 
                        self.img=ImageTk.PhotoImage(image=self.img)
                        self.charCanvas.itemconfigure(self.charImage, image=self.img)
                        self.charCanvas.coords(self.charImage,100,100)
                        #set the next photo
                        self.id=self.id+1
                        if self.id>65: #limit of photos
                            self.id=0      

                    else:   
                        #first time face found start watching on
                        self.startWatching=True
                        self.id=0

                else: 
                    #If kids not watching
                    self.countLeft=self.countLeft+1
                    if self.countLeft > 150:#lose point for bing away for this time
                        if self.startLose and not self.endLose:
                            self.startWatching=False # end watching
                            #get the photo and show
                            self.img = Image.open("imges\\youlose10\\vedios2"+self.getPhotoNumber(self.id)+".png")
                            self.img = self.img.resize((200, 200), Image.ANTIALIAS) 
                            self.img=ImageTk.PhotoImage(image=self.img)
                            self.charCanvas.itemconfigure(self.charImage, image=self.img)
                            self.charCanvas.coords(self.charImage,100,100)
                            #set the next photo
                            self.id=self.id+1
                            if self.id>210: #limit of photos
                                self.id=0      
                                self.endLose=True
                        elif not self.endLose:   
                            #first time 
                            self.startLose=True
                            self.startWatching=False # end watching
                            #start sound if not muted audio
                            if self.audio_is_on:
                                self.soundProcess=multiprocessing.Process(target=playsound, args=("sounds\\sorryforthat.mp3",))
                                self.soundProcess.start()
                            self.id=40 #set the id to 1
                    else:
                        if self.startLeft and not self.endLeft:
                            self.startWatching=False # end watching
                            #get the photo and show
                            self.img = Image.open("imges\\whereareyou\\whereareyou"+self.getPhotoNumber(self.id)+".png")
                            self.img = self.img.resize((200, 200), Image.ANTIALIAS) 
                            self.img=ImageTk.PhotoImage(image=self.img)
                            self.charCanvas.itemconfigure(self.charImage, image=self.img)
                            self.charCanvas.coords(self.charImage,100,100)
                            #set the next photo
                            self.id=self.id+1
                            if self.id>159: #limit of photos
                                self.id=0      
                                self.endLeft=True
                        elif not self.endLeft:
                            #first time
                            self.startLeft=True
                            self.startWatching=False # end watching
                            #start sound if not muted audio
                            if self.audio_is_on:
                                self.soundProcess=multiprocessing.Process(target=playsound, args=("sounds\\whereareyou.mp3",))
                                self.soundProcess.start()
                            self.id=80 #set the id to 1

        elif  self.windowID==2:
            if self.startExit:
                #get the photo and show
                self.exit_girl_img = Image.open("imges\\lesson is end\\lesoonisend"+self.getPhotoNumber(self.id)+".png")
                self.exit_girl_img = self.exit_girl_img.resize((200, 200), Image.ANTIALIAS) 
                self.exit_girl_img=ImageTk.PhotoImage(image=self.exit_girl_img)
                self.charExitCanvas.itemconfigure(self.charExitImage, image=self.exit_girl_img)
                self.charExitCanvas.coords(self.charExitImage,300,150)
                #set the next photo
                self.id=self.id+1
                if self.id>310: #limit of photos
                    self.id=0    
                    self.startExit=False
                    
        self.window.after(self.delay, self.update)
        
 
        
class MyVideoCapture:
    def __init__(self,main_window, video_source=0,width=100,height=100):
        self.main_window=main_window
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
            
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame_face(self):
        facefound=False
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=5,minSize=(20, 20))
                if len(faces)>0:
                    facefound=True
                # Return a boolean success flag and the current frame converted to BGR
                return (facefound,ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (facefound,ret, None)
        else:
            return (facefound,ret, None)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                self.main_window.class_start=False
                self.main_window.exitlabel_click()
                print("class ended")
                
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
         if self.vid.isOpened():
            self.vid.release()

            
class DrawWindow:

    def __init__(self, root,main_window):
        
        self.px,self.py=-1,-1
        self.startD=False
        self.main_window=main_window
        self.root = root
        self.root.geometry("300x300+500+200")
        self.root["bg"] = "white"
        self.canvas = tkinter.Canvas(self.root, width = 200, height = 200,bg='white',highlightthickness=0)
        self.canvas.pack(expand=tkinter.YES) 
        self.canvas.bind("<B1-Motion>",lambda event:self.draw(event))
        self.canvas.bind("<Button-1>",lambda e:self.startDraw())
        self.canvas.bind("<ButtonRelease-1>",lambda e: self.endDraw())
        
        send_button = tkinter.Button(self.root, text="أرســـل", command=lambda:self.send())
        
        send_button.pack(expand=tkinter.YES, fill=tkinter.X) 

    def startDraw(self):
        self.startD =True
        
    def endDraw(self):
        self.startD =False
        self.px,self.py = -1,-1
        
    def draw(self,e):
        if self.px != -1:
            self.canvas.create_line(self.px, self.py,e.x , e.y)
            self.px,self.py = e.x,e.y
        else:
            self.px,self.py = e.x,e.y
            
    def send(self):
        self.main_window.msg_list.insert(tkinter.END, "أنا: تم أرسال الصوره"+'\n','right')
        self.root.destroy()
        
# Create a window and pass it to the Application object
if __name__ == '__main__':
    a=App(tkinter.Tk(), "CRoom كرووم")
    a.window.mainloop()
