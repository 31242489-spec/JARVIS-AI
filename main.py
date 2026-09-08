

import win32com.client

speaker = win32com.client.Dispatch("SAPI.SPVOICE")


while 1 :
        print ("ENTER THE WORD YOU WANT TO SPEAK IT OUT BY COMPUTER ")
        S = input()
        speaker.speak('s')
