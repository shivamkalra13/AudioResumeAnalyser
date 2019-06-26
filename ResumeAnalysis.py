import speech_recognition as sr
import os

print('*'*10+"Welcome to Resume Analyser(Analyses only pronounciation and clearity of voice)"+'*'*10)
path=input("Enter the path of the folder that contains the files : ")
#dictf=input("Enter the path of dictionary file : ")
dictf=r"..\words_alpha.txt"
os.chdir(path)
flist=os.listdir()
reslist=[]
wrds=[]        #list of words in the file
acc=0

#check word in dictionary file
def wordInFile(wrd):
    dic=open(dictf)
    for dw in dic:
        if(dw[:-1]==wrd):
            return True
    return False
    

for file in flist:
    if(file[-4:]=='.wav'):
        print('processing : '+file)
        audio_file=(file)
        fpth=file[:-4]+'.txt'
        reslist.append(fpth)
        fo=open(fpth,'wt')
        r=sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            #reads the audio file.Here we use record instead of listen
            audio = r.record(source)
        try:
            #print('The audio contains : '+r.recognize_google(audio))
            fo.write(r.recognize_google(audio))
            fo.close()

        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')

        except sr.RequestError as e:
            print('Could not request rresult from google speech recognition service; {0}'.format(e))


#now read word by word from each file in reslist and compare these words in dictionary.
for fl in reslist:
    wrds=[]
    fo=open(fl)
    acc=0
    for line in fo:
        wrds.extend(line.split(' '))    #list of words in the file
    for wd in wrds:
        if wordInFile(wd):
            acc+=1
    accuracy=(acc/len(wrds))*100
    print("The english accuracy of "+fl[:-4]+" is : "+str(accuracy)+"%")
            
    
