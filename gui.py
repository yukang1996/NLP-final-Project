from tkinter import *
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfilename
import docx2txt
from os import listdir
from os.path import isfile, join, dirname, abspath
import nlpAbbreviation as abr
import AbbreCorpus as ac
import textblob as tb
import nltk


file_path = dirname(abspath(__file__))+"\documents"
onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
my_text = []



def _on_click(event):
    textbox1.tag_config("n", foreground="red")
    textbox1.insert("insert lineend","\nHello to you too.","n")

def joinTokens2Words(tokens):
    deto_clean_sentence = ' '.join(tokens)
    # deto_clean_sentence = list(map(lambda token: ' '.join(token), tokens))
    # deto_sentence = []
    # for token in tokens:
    #   deto_sentence.append(' '.join(token))
    return deto_clean_sentence

def fix():
    textbox1.tag_config("n", foreground="red")
    input = textbox1.get("insert linestart","insert lineend")
    # print(input)
    # tkMessageBox.showinfo("Get Sentence", input)
    fix_sentence = Toplevel()
    fix_sentence.geometry("700x100")

    label1 = Label(fix_sentence,text="Do you want to fix this sentence?:\n"+input)
    label1.pack(side=TOP)
    ok_button = Button(fix_sentence,text="OK", command = lambda : fix2(input,fix_sentence))
    ok_button.pack(side=TOP)
    cancel_button = Button(fix_sentence, text="CANCEL", command= lambda : fix_sentence.destroy())
    cancel_button.pack(side=TOP)

def fix2(input,fix_sentence):
    words = input.split(' ')
    after_abbrev = []
    temp = ''
    excelfile = ac.readCorpus()
    for i in range(len(words)):
        #check dictionary
        temp = ac.findWords(words[i],excelfile)
        if(temp == ''):
            try:
                print(words[i])
                after_abbrev.append(abr.noisy_channel(words[i], abr.big_lang_m, abr.big_err_m))
            except:
                print('%s cannot found' % words[i])
                after_abbrev.append(words[i])
        else:
            after_abbrev.append(temp)
    fix_sentence.destroy()
    sentence = joinTokens2Words(after_abbrev)
    sentence = ' '.join(sentence.split())
    textbox1.insert("insert lineend", "\n" + sentence, "n")


def list_of_file():
    top = Toplevel(window)
    scrollbar1 = Scrollbar(top)
    scrollbar1.pack(side=RIGHT, fill=Y)
    top.title("Please choose file from below.")
    Lb1 = Listbox(top,width=50,height=30)
    number = 1
    for i in onlyfiles:
        Lb1.insert(number, i)
        number = number+1
    Lb1.pack()
    Lb1.bind('<Double-Button-1>',lambda e: CurSelet(Lb1,top))
    scrollbar1.config(command=Lb1.yview)

def CurSelet(Lbl,top):
    global my_text
    value="documents/"+str((Lbl.get(ACTIVE)))
    try:
        my_text = docx2txt.process(value).encode('utf-8').decode('cp437').split('\n')
        global cleaned
        cleaned = False
        textbox1.delete("1.0",END)
        for i in range(len(my_text)):
            textbox1.insert(INSERT, my_text[i] + "\n")
            document_name["text"] = value
    except Exception as e:
        tkMessageBox.showinfo("Error!!", e)
    top.withdraw()



def meteprofilling():
    try:
        if cleaned:
            try:
                textbox2.delete("1.0", END)
                textbox2.tag_config("n", background="yellow", foreground="red")
                keyword = []
                for a in my_text:
                    if a == '':
                        pass
                    else:
                        test = a.split(" ")
                        join_word = test[0] + " " + test[1]
                        if join_word not in keyword:
                            keyword.append(join_word)

                for a in keyword:
                    textbox2.insert(INSERT, "Keyword: "+a+"\n","n")
                    for b in my_text:
                        if b == '':
                            pass
                        else:
                            test = b.split(" ")
                            join_word = test[0] + " " + test[1]
                            if join_word == a:
                                textbox2.insert(INSERT, b+"\n")
            except IOError as e:
                tkMessageBox.showinfo("Error!!", e)
        else:
            tkMessageBox.showinfo("Error!!", "The file is not been cleaned yet.")

    except NameError as e:
        pass


def remove_like_reply(sentence):
    clean_sentence = []
    pattern1 = '^Repl'
    for i in range(len(sentence)):
        sentence[i] = sentence[i].split(' ')
        if(len(sentence[i]) <= 3 or (sentence[i][0] == 'Like' and sentence[i][2] == 'Reply')):
            #ignore sentence left than 4 words
            pass
        elif((re.match(pattern1,sentence[i][1]) != None)==True):
            pass
        else:
            clean_sentence.append(sentence[i])
        
    return clean_sentence


def remove_emoji(clean_sentence):
    emoji_pattern = re.compile("["
        u"\U00000021-\U0000002F" #symbols !"#$%^.
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    for i in range(len(clean_sentence)):
        # print()
        # text = str(clean_sentence[i])
        for j in range(len(clean_sentence[i])):
            clean_sentence[i][j]= emoji_pattern.sub(r' ',clean_sentence[i][j])  
            print('xxxxxx '+clean_sentence[i][j])
    return clean_sentence

def remove_wordEmoticon(clean_sentence):
    for sentence in clean_sentence:
        word_index_to_be_delete = []
        for i in range(len(sentence)):
            sentence[i] = " ".join(sentence[i].split())
            if(sentence[i].lower() == "emoticon"):
                sentence[i]=""
                sentence[i-1]=""
    return clean_sentence



def removeNumtoWords(clean_sentence):
    pattern = re.compile(r'([A-z]){1,}\d+')
    for sentence in clean_sentence:
        for i in range(len(sentence)):
            try:
                if(pattern.match(sentence[i])):
                    new_word = ''
                    for j in range(int(sentence[i][-1])):
                        new_word = new_word +' '+sentence[i][:-1]

                    sentence[i] = new_word
            except:
                print(sentence[i]+' gt error.')

    return clean_sentence

# f = lambda x: x*2
# f(2)
#map ~ list.append
#parallel processing, faster than forloop list.append

def joinTokens2Sentence(tokens):
    deto_clean_sentence = list(map(lambda token: ' '.join(token), tokens))
    # deto_sentence = []
    # for token in tokens:
    #   deto_sentence.append(' '.join(token)) 
    return deto_clean_sentence

def splitSentence2Tokens(sentence):
    tokens = []
    for i in range(len(sentence)):
        tokens.append(sentence[i].split(' '))
    return tokens

def clean():
    global my_text
    global cleaned
    cleaned = True
    clean_sentence = remove_like_reply(my_text)
# extract_entities(clean_sentence)
    clean_sentence = remove_emoji(clean_sentence)
    clean_sentence = joinTokens2Sentence(clean_sentence)
    clean_sentence = splitSentence2Tokens(clean_sentence)
    clean_sentence = remove_wordEmoticon(clean_sentence)
    clean_sentence = removeNumtoWords(clean_sentence)
    clean_sentence = joinTokens2Sentence(clean_sentence)
    clear()
    for a in clean_sentence:
        print(a)
        textbox1.insert(INSERT,a+"\n")
    my_text = clean_sentence


def clear():
    textbox1.delete('1.0', END)
    textbox2.delete('1.0', END)
    document_name["text"] = ""

def translate():
    input = textbox1.get("insert linestart","insert lineend")
    print(input)
    text = tb.TextBlob(input)
    print(text.detect_language())
    translated = text.translate(to='en')
    print(translated)
    print(type(translated))
    textbox1.tag_config("n", foreground="green")
    textbox1.insert("insert lineend", "\n" + str(translated), "n")

def tree():
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    NPChunker = nltk.RegexpParser(grammar)
    input = textbox1.get("insert linestart","insert lineend")
    result = NPChunker.parse(nltk.pos_tag(input.split(" ")))
    print(result)
    parsetree = nltk.Tree.fromstring(str(result))
    parsetree.draw()


window = Tk()
window.title("Welcome to GoodDocument app")
window.geometry('1370x720')

left_frame = LabelFrame(window)
left_frame.place(width=100,height=700,x=0,y=0)

middle_frame = LabelFrame(window)
middle_frame.place(width=650,height=700,x=100,y=0)

right_frame = LabelFrame(window)
right_frame.place(width=600,height=700,x=750,y=0)

document_name = Label(middle_frame,text="")
document_name.place(x=0,y=0)

# Scrollbar
scrollbar1 = Scrollbar(middle_frame)
scrollbar1.pack( side = RIGHT, fill = Y )

scrollbar2 = Scrollbar(right_frame)
scrollbar2.pack( side = RIGHT, fill = Y )

# Text (User input for multiple line)
textbox1 = Text( middle_frame,yscrollcommand=scrollbar1.set, width=77,height=43 )
textbox1.place(x=0,y=21)

textbox2 = Text( right_frame,yscrollcommand=scrollbar2.set, width=71,height=43 )
textbox2.place(x=0,y=0)

# Button
btn = Button(left_frame, text="Insert file", command=list_of_file)
btn.place(x=0,y=0)

btn = Button(left_frame, text="Metaprofilling", command=meteprofilling)
btn.place(x=0,y=33)

btn = Button(left_frame, text="Clean", command=clean)
btn.place(x=0,y=73)

btn = Button(left_frame, text="Fix", command=fix)
btn.place(x=0,y=113)

btn = Button(left_frame, text="Translate", command=translate)
btn.place(x=0,y=153)

btn = Button(left_frame, text="Tree", command=tree)
btn.place(x=0,y=193)

btn = Button(left_frame, text="Clear", command=clear)
btn.place(x=0,y=233)

scrollbar1.config( command = textbox1.yview )
scrollbar2.config( command = textbox2.yview )

window.mainloop()