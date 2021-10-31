from gtts import gTTS
# import os
from playsound import playsound

# path = os.getcwd()
# print(path)

storepath = "/Users/niko/Desktop/MyApp/Django/minsta/study/"

inText = "BTS멋지다"
language = 'ko'
output = gTTS(text=inText, lang=language, slow=False)
storefile = storepath + "output.mp3"
output.save(storefile)

playsound(storefile)
