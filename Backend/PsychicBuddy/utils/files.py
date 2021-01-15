import speech_recognition as sr
from datetime import datetime

from pydub.silence import split_on_silence
from pydub import AudioSegment

from moviepy.editor import *
from PIL import Image
import numpy as np
import sys
import cv2
import os 

from . import sModel , iModel

filename = './Media/OSR_us_000_0010_8k.wav'

r = sr.Recognizer()

classes = ['Algebra',
 'Calculus',
 'City',
 'Curves',
 'Education',
 'Flower',
 'Geometry',
 'Light',
 'Science',
 'Trigonometry']

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    sound = AudioSegment.from_wav(path)  
    
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    print('[+] Processing Audio')
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    os.rmdir(folder_name)
    return whole_text

def audioToText(filename) :
    return get_large_audio_transcription(filename)

def videoToAudio(filename) :
    try :
        audioFilename = './Media/Temp.wav'
        video = VideoFileClip(filename)
        audio = video.audio
        audio.write_audiofile(audioFilename)
    except :
        audioFilename = None
    
    return audioFilename

def saveVideo(filename) :
    vc = cv2.VideoCapture(filename)
    frame_ = vc.read()

    frame = cv2.resize(frame_,(128,128,3))

    pred = iModel.predict([frame])

    if np.max(pred) < 0.5 : 
        return -1 
    else :
        im = Image.fromarray(frame_)
        im.save('Saves/'+classes[np.argmax(pred,axis=1)[0]]+'_'+str(datetime.now()))
        return np.argmax(pred,axis=1)[0]

def videoToText(filename) :
    saveVideo(filename)
    audioFilename = videoToAudio(filename)
    text = audioToText(audioFilename)

    return text

def splitPassage(text,length=128) :
    words = text.split()

    parts = []
    for i in range(len(words)//length) :
        parts.append(words[i*length:(i+1)*length])
    
    return parts
# text = videoToText('./Media/2020-12-03 13-08-32.mkv')
# print(text)