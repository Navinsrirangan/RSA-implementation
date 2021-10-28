# -*- coding: utf-8 -*-

"""

    Main GUI
    
"""
import math
import eea
import random
import rsa_keygen
import rsa
from os import path
import getBlockAndText
import base64

import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import filedialog as fd

win = tk.Tk() # Create instance
win.title("RSA Algorithm") # add title
tabControl=ttk.Notebook(win) # Create Tab Control
# Key Generation tab
tab1=ttk.Frame(tabControl) # Create a Tab
tabControl.add(tab1,text="Key Generation") # add the tab
# Encryption Tab
tab2=ttk.Frame(tabControl) # Create a Tab
tabControl.add(tab2,text="Encryption") # add the tab

# Decryption Tab
tab3=ttk.Frame(tabControl) # Create a Tab
tabControl.add(tab3,text="Decryption") # add the tab


tabControl.pack(expand=1,fill="both") # Pack to make visible
#=================
# Key Generation
empty_label=ttk.Label(tab1,text=" ")
empty_label.grid(column=0,row=0,sticky='W')
key_label=ttk.Label(tab1,text="To Generate new Key (large prime mumbers), press \"New\" Button.")
key_label.grid(column=1,row=1,sticky='W')

empty_label1=ttk.Label(tab1,text=" ")
empty_label1.grid(column=0,row=2,sticky='W')
# Modified Button Click Function
def click_me():
    global p,q,e,n,d
    p,q,e, n, d=rsa_keygen.RSA_keygen()
    p_text.delete(0.0, END)
    p_text.insert(0.0, str(p))
    q_text.delete(0.0, END)
    q_text.insert(0.0, str(q))
    pub_text.delete(0.0, END)
    pub_text.insert(0.0, "("+str(e)+", "+str(n)+")")
    pri_text.delete(0.0, END)
    pri_text.insert(0.0, str(d))
# Adding a Button
action = ttk.Button(tab1, text="New", command=click_me)   
action.grid(column=1, row=3,sticky='W')    

# prime number p
p_label=ttk.Label(tab1,text="         p:    ")
p_label.grid(column=0,row=4,sticky='W')
p_text = Text(tab1, width = 50, height = 5, wrap = WORD)
p_text.grid(column=1,row=4, columnspan = 2, sticky = W)

empty_label2=ttk.Label(tab1,text=" ")
empty_label2.grid(column=0,row=5,sticky='W')

# prime number q
q_label=ttk.Label(tab1,text="          q:    ")
q_label.grid(column=0,row=6,sticky='W')
q_text = Text(tab1, width = 50, height = 5, wrap = WORD)
q_text.grid(column=1,row=6, columnspan = 2, sticky = W)
#==================================
# Encryption Tab
empty_label3=ttk.Label(tab2,text=" ")
empty_label3.grid(column=1,row=0,sticky='W')
    
    
def loadText():
    global msg
    try:
        fDir = path.dirname(__file__)
        fName = fd.askopenfilename(parent=win, initialdir=fDir)
        f=open(fName,'r')
        msg=f.read()
        f.close()
    except:
        msg=""
        from tkinter import messagebox
        messagebox.showwarning(title=None, message="Oops! This is not valid file!!!\nPlease choose again or type text in here directly.")
    plain_text.delete(0.0, END)
    plain_text.insert(0.0, msg)
    

# Public Key
# e
pub_label=ttk.Label(tab2,text="  Public Key: \n  (e, n)=")
pub_label.grid(column=0,row=1,sticky='W')

pub_text = Text(tab2, width = 60, height = 5, wrap = WORD)
pub_text.grid(column=1,row=1, columnspan = 2, sticky = W)

load_text = ttk.Button(tab2, text="Load Text", command=loadText)   
load_text.grid(column=1, row=2,sticky='W')

plain_label=ttk.Label(tab2,text=" Message")
plain_label.grid(column=0,row=3,sticky='W')
 
plain_text = Text(tab2, width = 60, height = 6, wrap = WORD)
plain_text.grid(column=1,row=3, columnspan = 2, sticky = W)

def encryptionText():
    msg=plain_text.get("1.0", END)
    key=pub_text.get("1.0", END)
    if len(key)==1:
        from tkinter import messagebox
        messagebox.showwarning(title="Warning", message="Empty Key!!!\nPlease generate new Key or type directly.")
    else:
        if len(msg)==1:
            from tkinter import messagebox
            messagebox.showwarning(title="Warning", message="Empty message!!!\nPlease choose text file or type text.")
        else:
            # convert text to block integers
            global blockSize
            blockSize = int(math.log(n, 128))
            x=getBlockAndText.getBlocksFromText(msg, blockSize)
            global base64_cliper, y
            y=rsa.RSA_encrypt(x, (e,n))
            # convert block integer to text
            cliper=getBlockAndText.getTextFromBlocks(y, blockSize)
            
            cliper_bytes = cliper.encode('utf-8')
            base64_bytes = base64.b64encode(cliper_bytes)
            base64_cliper = base64_bytes.decode('ascii')
        
  
            encrypt_text.delete(0.0, END)
            encrypt_text.insert(0.0, base64_cliper)
    


encryption = ttk.Button(tab2, text="Encryption", command=encryptionText)   
encryption.grid(column=1, row=4,sticky='W')

encrypt_label=ttk.Label(tab2,text=" Encrypted\n    Text")
encrypt_label.grid(column=0,row=5,sticky='W')
 
encrypt_text = Text(tab2, width = 60, height = 6, wrap = WORD)
encrypt_text.grid(column=1,row=5, columnspan = 2, sticky = W)

#==================================
#==================================
# Decryption Tab
empty_label4=ttk.Label(tab3,text=" ")
empty_label4.grid(column=1,row=0,sticky='W')

def readCliper():
    cliper_text.delete(0.0, END)
    cliper_text.insert(0.0, base64_cliper)


# Public Key
# e
private_label=ttk.Label(tab3,text="Private Key: \n    d =")
private_label.grid(column=0,row=1,sticky='W')

pri_text = Text(tab3, width = 60, height = 5, wrap = WORD)
pri_text.grid(column=1,row=1, columnspan = 2, sticky = W)

show_clip = ttk.Button(tab3, text="Show Text", command=readCliper)   
show_clip.grid(column=1, row=2,sticky='W')

cliper_label=ttk.Label(tab3,text=" Cliper \n  Message")
cliper_label.grid(column=0,row=3,sticky='W')
 
cliper_text = Text(tab3, width = 60, height = 6, wrap = WORD)
cliper_text.grid(column=1,row=3, columnspan = 2, sticky = W)

def decryptionText(): # Decryption
   
    base64_bytes = base64_cliper.encode('utf-8')
    cliper_bytes = base64.b64decode(base64_bytes)
    cliper = cliper_bytes.decode('utf-8')
    blockIntegers=getBlockAndText.getBlocksFromText(cliper, blockSize)
    x=rsa.RSA_decrypt(blockIntegers,(d,n))
    txt=getBlockAndText.getTextFromBlocks(x, blockSize)
    decrypt_text.delete(0.0, END)
    decrypt_text.insert(0.0, str(txt))
    

decryption = ttk.Button(tab3, text="Decryption", command=decryptionText)   
decryption.grid(column=1, row=4,sticky='W')

decrypt_label=ttk.Label(tab3,text=" Decrypted\n    Text")
decrypt_label.grid(column=0,row=5,sticky='W')
 
decrypt_text = Text(tab3, width = 60, height = 6, wrap = WORD)
decrypt_text.grid(column=1,row=5, columnspan = 2, sticky = W)

#==================================
# Decryption Tab
#==================================
win.geometry("600x400")
win.mainloop()

