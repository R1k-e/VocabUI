##Welcome to FrVocab1.
##Tool for learning French.

from tkinter import *

##for sounds-
from gtts import gTTS
from io import BytesIO
from pygame import mixer

import random

##Creating the root window:
root = Tk()

##Getting Vocab list

def load_txt(filename):
    l = []
    with open(filename, encoding='utf-8') as vocab:
        for g in vocab:
            s = g.replace("\n", "")
            l.append(s)
    return l

        
l = load_txt("Vocab.txt")

##############################language = "fr"


##Creating a Label Widget
myLabel1 = Label(root, text="Practice or Alter File?")



##Putting our Label Widget on Screen
myLabel1.grid(row = 0, column = 0)

##top closed function
def topClosed(x):
    root.deiconify()
    x.destroy()


##Creating the label widget

class Labels():
    def __init__(self,parent,name,varText):
        self.parent = parent
        self.name = name
        self.varText = varText

        self.label = Label(parent,text=varText)
        
    def grid(self, **kwargs):
        self.label.grid(kwargs)

##Creating the Entry widget

class Entries():
    def __init__(self,parent,width,borderwidth):
        self.parent = parent
        self.width = width
        self.borderwidth = borderwidth

        self.entry = Entry(parent,width=width,borderwidth=borderwidth)

    def grid(self, **kwargs):
        self.entry.grid(kwargs)

        
##Creating sound button widget

class soundButtons():
    def __init__(self,parent,sound,language):
        self.parent = parent
        self.sound= sound
        self.lang = language
        ##creating a play sound function
        
    def replay(self):
        mixer.init()
        mp3_fo = BytesIO()
        myobj = gTTS(text=self.sound, lang=self.lang, slow=False)

        myobj.write_to_fp(mp3_fo)

        mixer.music.load(mp3_fo, "mp3")

        mixer.music.play()

    def __call__(self, **kwargs):
        self.button = Button(self.parent,text="listen",command=self.replay)
        
    def grid(self, **kwargs):
        self.button.grid(kwargs)          

##verbsPractice window
def verbsPractice():
    ##Setting up basic properties of new practice window

    practiceWindow =Toplevel()
    practiceWindow.title("Verbs")
    practiceWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(practiceWindow))
    practiceWindow.bind("<Escape>", lambda e: root.destroy())

    ##setting up incorrect counter
    global incorrectVerb
    incorrectVerb = 0
    
    ##conj tuple:
    conj = ("english","infinitive","present tense first person singular","present tense second person singular","present tense third person singular","present tense first person plural",
            "present tense second person plural","present tense third person plural","perfect tense","future tense first person singular","future tense second person singular",
            "future tense third person singular","future tense first person plural","future tense second person plural","future tense third person plural",
            "subjunctive tense first person singular","subjunctive tense second person singular","subjunctive tense third person singular","subjunctive tense first person plural",
            "subjunctive tense second person plural","subjunctive tense third person plural",
            "imperfect tense first person singular","imperfect tense second person singular","imperfect tense third person singular","imperfect tense first person plural",
            "imperfect tense second person plural","imperfect tense third person plural",
            "conditional tense first person singular","conditional tense second person singular","conditional tense third person singular","conditional tense first person plural",
            "conditional tense second person plural","conditional tense third person plural")
    ##pronouns tuple:
    pronouns = ("je","tu","il/elle","nous","vous","ils/elles")
    
    ##getting verbs list:
    if language =="fr":
        verbs = l[2:]
    elif language =="sr":
        verbs = l[3:]
    ##choosing verb:
    selected = random.choice(verbs)
    selected = selected.split(":")

    ##Title label:
    Title = Labels(practiceWindow,"title",selected[0])
    Title.grid()
    
    ##Labels and entries insantiation and gridding:
    
    verbLabelList = []
    verbEntryList = []

    ##setting up labels by measuring the amount of conjugation that can happen:
    
    for i in range(1,len(selected)):

        verbL = Labels(practiceWindow,name = conj[i],varText= conj[i])
        verbL.grid(column=0)

        ##There HAS to be another way of doing this (labeling pronouns):
        if language == "fr":
            if i > 1 and i < 8:
                pronounL = Labels(practiceWindow,name = pronouns[i-2],varText= pronouns[i-2])
                pronounL.grid(column=1, row =i)
            elif i > 8 and i < 15:
                pronounL = Labels(practiceWindow,name = pronouns[i-9],varText= pronouns[i-9])
                pronounL.grid(column=1, row =i)
            elif i >= 15 and i < 21:
                pronounL = Labels(practiceWindow,name = pronouns[i-15],varText= pronouns[i-15])
                pronounL.grid(column=1, row =i)
            elif i >= 21 and i < 27:
                pronounL = Labels(practiceWindow,name = pronouns[i-21],varText= pronouns[i-21])
                pronounL.grid(column=1, row =i)
            elif i >= 27:
                pronounL = Labels(practiceWindow,name = pronouns[i-27],varText= pronouns[i-27])
                pronounL.grid(column=1, row =i)
 
        
        verbLabelList.append(verbL)
        verbE = Entries(practiceWindow, width = 30, borderwidth = "2")
        verbE.grid(column=2, row = i)
        verbEntryList.append(verbE)

        ##soundbuttons:
        if language == "sr":

            verbSound = soundButtons(practiceWindow,selected[i],language)
            verbSound()
            verbSound.grid(column=3,row=i)

    ##getting feedback:
        
    ##setting up feedback label
    feedback = StringVar()
    check = Label(practiceWindow, textvariable = feedback)
    ##Button command (I dont know how to get this to update the label correctly
    def Submit():
        pass_right = "correct"
        remark = "correct"
        conjCount = 1
        for i in verbEntryList:
            ##Checking to see if incorrect, if so change remark to "incorrect", which blocks
            #continuation, and removes what has been entered into that box...
            if i.entry.get() != selected[conjCount]:
                remark = "incorrect"
                i.entry.delete(0, "end")
            conjCount += 1
        

        ##Checking answers:
        feedback.set(remark)
        check.grid()
        practiceWindow.update()
        if remark == pass_right:
            topClosed(practiceWindow)
        ##adding to counter if incorrect:
        elif remark == "incorrect":
            global incorrectVerb
            incorrectVerb += 1
            if incorrectVerb >= 3:
                for i in range(1, len(selected)):
                    verbL = Labels(practiceWindow,name = selected[i],varText= selected[i])
                    verbL.grid(column=3, row = i)

    ##setting up submit button
    
    submitVerbs = Button(practiceWindow, text="Submit",command=Submit)

    ##gridding submit button
    submitVerbs.grid()
    
    if language == "sr":
    ##characters button
        def characters():
            verbEntryList[0].entry.insert(index=len(verbEntryList[0].entry.get()),string="čćdžđljnjšž")
        specialCharacters = Button(practiceWindow,text="characters",command=characters)
        specialCharacters.grid()


##nounsPractice window

###\this all needs to be redone with objects as it is a mess right now

def nounsPractice():
    ##Setting up basic properties of new practice window

    practiceWindow = Toplevel()
    practiceWindow.title("Nouns")
    practiceWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(practiceWindow))
    practiceWindow.bind("<Escape>", lambda e: root.destroy())

    ##Setting up list of 5 nouns
    nouns = l[1].split(";")
    five = []
    for i in range(5):
        five.append(nouns.pop(random.randrange(0,len(nouns))))
    ##eng-french split
    noun1 = five[0].split(":")
    noun2 = five[1].split(":")
    noun3 = five[2].split(":")
    noun4 = five[3].split(":")
    noun5 = five[4].split(":")
    nounsList = [noun1,noun2,noun3,noun4,noun5]
    
    
    ##Setting up entry methods
    noun1E = Entry(practiceWindow, width=30, borderwidth="2")
    noun2E = Entry(practiceWindow, width=30, borderwidth="2")
    noun3E = Entry(practiceWindow, width=30, borderwidth="2")
    noun4E = Entry(practiceWindow, width=30, borderwidth="2")
    noun5E = Entry(practiceWindow, width=30, borderwidth="2")

    ##Setting up labels

    noun1L = Label(practiceWindow, text = str(noun1[0]))
    noun2L = Label(practiceWindow, text = str(noun2[0]))
    noun3L = Label(practiceWindow, text = str(noun3[0]))
    noun4L = Label(practiceWindow, text = str(noun4[0]))
    noun5L = Label(practiceWindow, text = str(noun5[0]))

    ##setting up feedback label
    feedback = StringVar()
    check = Label(practiceWindow, textvariable = feedback)
    ##Button command (I dont know how to get this to update the label correctly
    def Submit():
        ##setting up for playing sound:
        mixer.init()
        
        right = []
        pass_right = ["Yes","Yes","Yes","Yes","Yes"]
        if noun1E.get() == str(noun1[1]):
            right.append("Yes")
        else:
            right.append(noun1[1])

        if noun2E.get() == str(noun2[1]):
            right.append("Yes")
        else:
            right.append(noun2[1])

        if noun3E.get() == str(noun3[1]):
            right.append("Yes")
        else:
            right.append(noun3[1])

        if noun4E.get() == str(noun4[1]):
            right.append("Yes")
        else:
            right.append(noun4[1])
            
        if noun5E.get() == str(noun5[1]):
            right.append("Yes")
        else:
            right.append(noun5[1])

        ##Checking answers:
        feedback.set(right)
        check.grid(row=6)
        practiceWindow.update()
        if right == pass_right:
            verbsPractice()
            mp3_fo = BytesIO()
            read = noun1[1] +","+ noun2[1] +","+ noun3[1] +","+ noun4[1] +","+ noun5[1]
            myobj = gTTS(text=read, lang=language, slow=False)

            myobj.write_to_fp(mp3_fo)

            mixer.music.load(mp3_fo, "mp3")

            mixer.music.play()
            practiceWindow.destroy()

    ##setting up submit button
    
    submitNouns = Button(practiceWindow, text="Submit",command=Submit)


    ##adding all to grid:
    noun1L.grid(row=0,column=0)
    noun1E.grid(row=0,column=1)

    noun2L.grid(row=1,column=0)
    noun2E.grid(row=1,column=1)

    noun3L.grid(row=2,column=0)
    noun3E.grid(row=2,column=1)

    noun4L.grid(row=3,column=0)
    noun4E.grid(row=3,column=1)

    noun5L.grid(row=4,column=0)
    noun5E.grid(row=4,column=1)

    ##adding some sound buttons:
    rowposition = 0
    for i in nounsList:
        nounSound = soundButtons(practiceWindow,i[1],language)
        nounSound()
        nounSound.grid(column=3,row=rowposition)
        rowposition +=1



    submitNouns.grid(row=5)

    ##characters button
    if language == "sr":
        def characters():
            noun1E.insert(index=len(noun1E.get()),string="ČčĆćDŽdžĐđLJljNJnjŠšŽž")
        specialCharacters = Button(practiceWindow,text="characters",command=characters)
        specialCharacters.grid(column = 3)


def alter():
    root.withdraw()
    alterWindow = Toplevel()
    alterWindow.title("Alter")
    alterWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(alterWindow))
    alterWindow.bind("<Escape>", lambda e: root.destroy())

    ##defining nouns and verbs for a simple list of current words in list (temporary):
    nouns = l[0].split(";")
    verbs = l[1:]
    for i in nouns:
        splitNouns = i.split(":")
        newNoun = Labels(alterWindow,splitNouns[0],splitNouns[0])
        newNoun.grid()
    for i in verbs:
        splitVerbs = i.split(":")
        newVerb = Labels(alterWindow,splitVerbs[0],splitVerbs[0])
        newVerb.grid()

##Alphabet test window
def alphabet():
    alphabetWindow = Toplevel()
    alphabetWindow.title("alphabet")
    alphabetWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(alphabetWindow))
    alphabetWindow.bind("<Escape>", lambda e: root.destroy())
    ##loading croat vocab
    global l
    l = load_txt("croatVocab.txt")

    ##Splitting croat alphabet
    sounds = l[0].split(";")
    testSound = random.choice(sounds)

    ##loading selected sound as mp3
    mixer.init()
    mp3_fo = BytesIO()
    read = testSound
    myobj = gTTS(text=read, lang=language, slow=False)

    myobj.write_to_fp(mp3_fo)

    mixer.music.load(mp3_fo, "mp3")

    mixer.music.play()

    ##creating sounds label
    letters = Label(alphabetWindow,text=l[0])
    letters.grid()
    ##creating entry
    response = Entry(alphabetWindow)
    response.grid()
    ##creating submit button
    def soundSubmit():
        if response.get() == testSound:
            alphabetWindow.destroy()
            croat_nouns()
    submitSound = Button(alphabetWindow,text="submit",command=soundSubmit)
    submitSound.grid()
    ##creating replay button
    replay = Button(alphabetWindow, text="replay",command=mixer.music.play)
    replay.grid()

    ##characters button
    def characters():
        response.insert(index=len(response.get()),string="ČčĆćDŽdžĐđLJljNJnjŠšŽž")
    specialCharacters = Button(alphabetWindow,text="characters",command=characters)
    specialCharacters.grid()


### croat noun forms
def croat_nouns():
    ##Setting up window basic properties
    practiceWindow =Toplevel()
    practiceWindow.title("croat_nouns")
    practiceWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(practiceWindow))
    practiceWindow.bind("<Escape>", lambda e: root.destroy())

    
    ###getting nouns:
    global l
    l = load_txt("croatVocab.txt")
    global language
    language = "sr"
    nouns = l[2].split(";")
    selected = random.choice(nouns)
    selected = selected.split(":")

    conj = ("English","Nominative","Accusative","Genitive","Dative","Vocative","Locative","Instrumental")

    ##Title label:
    English = Labels(practiceWindow,"title",selected[0])
    English.grid()
    
    ##Labels and entries insantiation and gridding:
    
    nounLabelList = []
    nounEntryList = []

    ##setting up labels by measuring the amount of conjugation that can happen:
    
    for i in range(1,len(selected)):
        nounL = Labels(practiceWindow,name = conj[i],varText= conj[i])
        nounL.grid(column=0)
        nounLabelList.append(nounL)
        nounE = Entries(practiceWindow, width = 30, borderwidth = "2")
        nounE.grid(column=1, row = i)
        nounEntryList.append(nounE)

        nounSound = soundButtons(practiceWindow,selected[i],language)
        nounSound()
        nounSound.grid(column=2,row=i)


    feedback = StringVar()
    check = Label(practiceWindow, textvariable = feedback)
    
    ##Button command
    def Submit():
        pass_right = "correct"
        remark = "correct"
        conjCount = 1
        for i in nounEntryList:
            ##Checking to see if incorrect, if so change remark to "incorrect", which blocks
            #continuation, and removes what has been entered into that box...
            if i.entry.get() != selected[conjCount]:
                remark = "incorrect"
                i.entry.delete(0, "end")
            conjCount += 1
        

        ##Checking answers:
        feedback.set(remark)
        check.grid()
        practiceWindow.update()
        if remark == pass_right:
            practiceWindow.destroy()
            #nounsPractice()
            nounsPractice()

    ##setting up submit button
    
    submitNouns = Button(practiceWindow, text="Submit",command=Submit)

    ##gridding submit button
    submitNouns.grid()

    def characters():
            nounEntryList[0].entry.insert(index=len(nounEntryList[0].entry.get()),string="ČčĆćDŽdžĐđLJljNJnjŠšŽž")
    specialCharacters = Button(practiceWindow,text="characters",command=characters)
    specialCharacters.grid(column = 3)


##language selection window

def language():
    ##withdrawing root
    root.withdraw()
    ##setting up basic window properties:
    langWindow = Toplevel()
    langWindow.title("language")
    langWindow.protocol("WM_DELETE_WINDOW",lambda: topClosed(langWindow))
    langWindow.bind("<Escape>", lambda e: root.destroy())
    ##Defining button commands:
    def frSubmit():
        global l
        l = load_txt("Vocab.txt")
        global language
        language = "fr"
        langWindow.destroy()
        nounsPractice()
    def crSubmit():
        global language
        language = "sr"
        langWindow.destroy()
        #alphabet()
        croat_nouns()
        

    ##adding buttons:
    submitfr = Button(langWindow, text="French",command=frSubmit)
    submitcr = Button(langWindow,text="Croatian",command=crSubmit)
    submitfr.grid()
    submitcr.grid()
    



##creating two options buttons
myButton1 = Button(root, text = "Practice", command = language)

myButton2 = Button(root, text = "Alter", command = alter)



##adding buttons to root:
myButton1.grid(row=1,column=0)
myButton2.grid(row=2,column=0)


##Kicking off Window's event loop

root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()


