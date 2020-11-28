#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import subprocess

import json
import string

import os
import sys

SetLogLevel(0)

video_name = str(sys.argv[1][:-4] + '.mp4')

print('Video name is ' + video_name)

stream = os.popen('ffmpeg -i ' + video_name + ' ' + sys.argv[1])
output = stream.read()
output

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

sample_rate=16000
model = Model("model")
rec = KaldiRecognizer(model, sample_rate)

process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                            sys.argv[1],
                            '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                            stdout=subprocess.PIPE)
while True:
    data = process.stdout.read(4000)
    if len(data) == 0:
       	break
    if rec.AcceptWaveform(data):
        pass
#        print(rec.Result())
    else:
        pass
#        print(rec.PartialResult())

finish = str(rec.FinalResult())
print(json.loads(finish))
with open('res.json', 'w') as f:
    json.dump(json.loads(finish), f)

