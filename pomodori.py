from sys import argv
from os import get_terminal_size
import pyaudio 
import wave
import keyboard
import time 
import colorama
from colorama import Fore,Style,Cursor


def printProgressBar(totalProgress):
    print(f"\r{Fore.GREEN}[",end="")
    tsize = get_terminal_size() 
    
    filled = int(totalProgress*(tsize.columns-3))*'#'
    unfilled = (tsize.columns -3 - int(totalProgress*tsize.columns))*'.'
    print(f"{Fore.YELLOW}{filled}{Fore.RED}{unfilled}",end="")
    print(f"{Fore.GREEN}]{Style.RESET_ALL}",end="")
class TimerHandler:
    timerStates : dict = {
    }
    def __init__(self, workInterval, breakInterval,total):
        self.timerStates["work"] = workInterval
        self.timerStates["shortbreak"] = breakInterval
        self.timerStates["longbreak"] = breakInterval*3.0
        self.total = total
        self.state = "work"
        self.currentSession = 0
    def runTimer(self):
        startTime = time.time()
        interval = self.timerStates[self.state] 
        while time.time() - startTime < minToSec(interval):
            current = minToSec(interval)-  (time.time() - startTime)
            #print(f"\r{interval/current}{Style.RESET_ALL}",end="") 
            printProgressBar(1.0 - current/minToSec(interval)) 
            #print(f"\r{Fore.GREEN}{timeString(current)}{Style.RESET_ALL}",end="")
            if keyboard.is_pressed("escape"):
                print(interval)
                break
        
        self.currentSession += interval
        if self.state == "work": 
            play_sound('EndOfWork.wav')
            self.state = "shortbreak"
            if(self.currentSession >= self.total):
                print("Congrats your work is done!")
                # play allDone here  
                return 
        else:
            play_sound('BreakIsOver.wav')
            self.state = "work"
        self.runTimer()

def minToSec(value):
    return float(value*60.0)
def timeString(value):
    mins, secs = divmod(value, 60)
    return f"{int(mins):02d}:{int(secs):02d}"

def play_sound(file_path):
    wf = wave.open(file_path,'rb')

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)
        if keyboard.is_pressed('escape'):
            break
    stream.stop_stream()
    stream.close() 
    p.terminate()

def runTimer(interval):
    startTime = time.time()

    while time.time() - startTime < minToSec(interval):
        current = minToSec(interval)-  (time.time() - startTime)
        print(f"\r{Fore.GREEN}{timeString(current)}{Style.RESET_ALL}",end="")

    play_sound('EndOfWork.wav')
timeInterval = 25
if len(argv) <= 1:
   print("No time was supplied, using default time of 25 minutes")
   timeInterval = 25
else: 
    if argv[1].isnumeric():
        timeInterval = float(argv[1])
colorama.init()
timer = TimerHandler(timeInterval,5.0,(timeInterval+5)*4)
timer.runTimer()
