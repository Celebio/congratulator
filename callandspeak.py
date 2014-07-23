#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import pjsua as pj
import threading
import urllib
import subprocess
import random
import urllib
import urllib2

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT = BASE_DIR






SIP_HOST = ""     # SIP PROVIDER HERE, For example SIP_HOST = "sip.ovh.fr"
SIP_LOGIN = ""
SIP_PWD = ""

CALL_SIP_URI = ""   # The phone number you want to call in sip uri format, for example : CALL_SIP_URI = "sip:0033827384719@sip.ovh.fr"


lib = None


import unicodedata
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')



# Logging callback
def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()


# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global lib
        print "Call is ", self.call.info().state_text,
        print self.call.info()
        print "self.call.info().state", self.call.info().state
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
        if self.call.info().state == 6:     #pj.Call.DISCONNECTED:
            print "hangup ?? :'("
            # self.call.hangup()
            try:
                lib.destroy()
            except:
                pass

            sys.exit(0)

    # Notification when call's media state has changed.
    def on_media_state(self):
        global lib
        print "on media state", self.call.info().media_state
        
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            print "Creating wav"

            player_id = lib.create_player("temp.wav")
            #player_id = lib.create_player("/vagrant/africa-toto.wav")

            player_slot = lib.player_get_slot(player_id)

            call_slot = self.call.info().conf_slot
            lib.conf_connect(call_slot, player_slot)
            lib.conf_connect(player_slot, call_slot)

            print "Hello world, I can talk!"



 
#----------------------------------------------------------------------
def get_google_voice(phrase, fId):
    """
    Function that will send http request to google translate
    and save audio file from responce with voiced input phrase.
    Parameters:
    @phrase: sentence to transform into voice.
    Returns:
    If ok - name of created file, else - returns None.
    """
    
    language='fr' #Setting language.
    url = "http://translate.google.com/translate_tts" #Google translate url for getting sound.
    user_agent="Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." 
    file_name="temp%d.mp3" % (fId) #Temp file for saving our voiced phrase.
 
    params = urllib.urlencode({'q':phrase, 'tl':language}) #query parameters.
    request = urllib2.Request(url, params) #http request.
    request.add_header('User-Agent', user_agent) #adding agent as header.
    response = urllib2.urlopen(request) 
    
    if response.headers['content-type'] == 'audio/mpeg':
        with open(file_name, 'wb') as file:
            file.write(response.read())

        return file_name
    else:
        return None


def congratSalesman(salerName, salerSexe, customerName):
    global lib
    print "getting speak from google"

    text_to_say = ""
    text_ouverture = ""

    a = random.random()
    print a
    if a < 0.1:
        text_ouverture = "HOP HOP HOP. Ouech mon frère."
    elif a < 0.2:
        if salerSexe == "M":
            text_ouverture = "Bonjour monsieur."
        else:
            text_ouverture = "Bonjour madame."
        text_ouverture += "Veuillez m'excuser de vous déranger."
        if random.random() < 0.3:
            text_ouverture += "Ce n'est pas mon genre de déranger les gens pour rien"
    elif a < 0.3:
        text_ouverture = "Hey hey hey. A base de benz benz benz."
    elif a < 0.4:
        text_ouverture = "Je suis le représentant virtuel de Nereo."
    elif a < 0.5:
        text_ouverture = "Hello. Je viens d'apprendre des choses."
    elif a < 0.6:
        text_ouverture = "Allo. Allo?. Non mais allo quoi?."
    elif a < 0.7:
        text_ouverture = "Bonjour. C'est génial. Vraiment génial."
    elif a < 0.8:
        text_ouverture = "Bonjour. J'ai entendu dire que y en a qui faisait chauffer le CRM."
    elif a < 0.9:
        text_ouverture = "Allo. Vous m'entendez? Je crois qu'il y a du niveau."
    elif a < 1.0:
        text_ouverture = "Oh! C'est ouf. C'est vraiment ouf."

    text_to_say += text_ouverture + "."

    text_customer_name = ""
    a = random.random()
    print a
    if a < 0.3:
        text_customer_name = "J'ai appris que %s fait maintenant parti de nos clients." % customerName
    elif a < 0.6:
        text_customer_name = "Alors? %s fait maintenant parti de nos clients?" % customerName
    elif a < 1:
        text_customer_name = "Je sais tout. On me l'a dit. %s fait maintenant parti de nos clients." % customerName

    text_to_say += text_customer_name + "."

    text_happy = ""
    a = random.random()
    print a
    if a < 0.1:
        text_happy = "Tu peux pas savoir comme je suis contente."
    elif a < 0.2:
        text_happy = "J'ai envie de pleurer de bonheur."
    elif a < 0.3:
        text_happy = "Je suis tellement contente que je suis en larmes."
    elif a < 0.4:
        text_happy = "Cette une excellente nouvelle."
    elif a < 0.5:
        text_happy = "Je crois que je suis très émue. Excuse-moi si je parais un peu trop émue."
    elif a < 0.6:
        text_happy = "C'est vraiment une bonne nouvelle. Bonne bonne bonne. Quand la nouvelle est bonne."
    elif a < 0.7:
        text_happy = "Je suis tellement heureuse. La dernière fois que j'ai été aussi heureuse c'est quand Onour m'a programmée."
    elif a < 0.8:
        text_happy = "C'est un vrai moment de bonheur."
    elif a < 0.9:
        text_happy = "A chaque nouveau client, c'est un moment d'émotion."
    elif a < 1:
        if salerSexe == "M":
            text_happy = "Tu dois être aussi heureux que moi."
        else:
            text_happy = "Tu dois être aussi heureuse que moi."

    text_to_say += text_happy + "."

    text_congrats = ""
    a = random.random()
    print a
    if a < 0.1:
        text_congrats = "Tu déchires tellement qu'il faut que tu restes loin des documents importants. Tu risquerais de les déchirer."
    elif a < 0.2:
        text_congrats = "Franchement chapeau. Un grand bravo à toi."
    elif a < 0.3:
        text_congrats = "Je crois que rien ne t'arrete. Tu aimes Johnny ou quoi? Tu allumes le feu."
    elif a < 0.4:
        text_congrats = "Tu déchires vraiment ta race. Je suis fière de toi."
    elif a < 0.5:
        text_congrats = "Tu es une superstar. Vraiment. Non, vraiment. Je le pense vraiment, même si je ne suis qu'un robot, je le pense."
    elif a < 0.6:
        text_congrats = "On devrait mettre ta photo sur les murs de Nereo, voire ta sculpture."
    elif a < 0.7:
        text_congrats = "Ce que tu fais est vraiment ouf. C'est le résultat d'un travail acharné. Ton charisme y est pour quelque chose aussi, forcément."
    elif a < 0.8:
        if salerSexe == "M":
            text_congrats = "Tu es le meilleur."
        else:
            text_congrats = "Tu es la meilleure."
    elif a < 0.9:
        text_congrats = "Si tu continues comme ça, il n'y aura plus de client à signer. Tout le monde sera client de Nereo."
    elif a < 1.0:
        text_congrats = "Je ne sais pas comment te dire, tu as vraiment assuré."
        

    text_to_say += text_congrats + "."

    text_congrats2 = "Bravo, bravo et encore bravo. Félicitations!"
    text_to_say += text_congrats2 + "."

    text_nereoouf = "Grâce à toi, Nereo va continuer à tout déchirer. L'échec n'est pas une option."
    text_to_say += text_nereoouf + "."

    createNewWav = True
    
    if createNewWav:
        ctr = 0
        for sentence in text_to_say.split("."):
            if sentence:
                try:
                    print "sentence", strip_accents(unicode(sentence))
                except:
                    pass
                get_google_voice(sentence, ctr)
                ctr += 1

        print "done, enfin je crois"

        cmd = "mpg123 -w temp.wav %s" % (" ".join(["temp%d.mp3" % (i) for i in range(ctr)]))
        print cmd.encode('utf-8')
        subprocess.call(cmd, shell=True)

        print "created wav"
    try:
        # Create library instance
        lib = pj.Lib()

        # Init library with default config
        lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))
        lib.set_null_snd_dev()

        # Create UDP transport which listens to any available port
        transport = lib.create_transport(pj.TransportType.UDP)
        
        # Start the library
        lib.start()

        acc = lib.create_account(pj.AccountConfig(SIP_HOST, SIP_LOGIN, SIP_PWD))


        acc_cb = MyAccountCallback(acc)
        acc.set_callback(acc_cb)
        acc_cb.wait()

        # Make call
        call = acc.make_call(CALL_SIP_URI, MyCallCallback())

        # Wait for ENTER before quitting
        print "Press <ENTER> to quit"
        input = sys.stdin.readline().rstrip("\r\n")

        # We're done, shutdown the library
        lib.destroy()
        lib = None

    except pj.Error, e:
        print "Exception: " + str(e)
        lib.destroy()
        lib = None
        sys.exit(1)


congratSalesman("Test", "M", sys.argv[1])


