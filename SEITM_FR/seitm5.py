# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 19:15:02 2022

@author: hugob
"""

### Bibliothèque ###
import random as r
import tkinter as tk
from tkinter import ttk
import datetime as datetime
import webbrowser
import os
import math as math

import matplotlib.pyplot as plt

"""
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
"""



### Initialisation ###
hauteur_fenêtre = 600
dimension = '900x600'
url = 'https://eseo.fr/'
file_DossierTIPE = "assets\\ressources\\Dossier TIPE.pdf"
file_ProcedureDensite = "assets\\ressources\\ProcedureDensite.pdf"

global dossier
dossier = 'Captures'


global nbr_jour, longueur, inf, pei, tse, pts, tim, pit, dateheure, dens, factdens
nbr_jour = 0
longueur = 0
inf = 0
pei = 0
tse = 0
pts = 0
tim = float(0)
pit = 0
dateheure = 0
dens = 'carte0'
factdens = 0







#///////////////////////////////////#
#///////////////////////////////////#
#/////          IHM            /////#
#///////////////////////////////////#
#///////////////////////////////////#

def open_url(url):
   webbrowser.open_new_tab(url)
   
def open_file(file):
    os.startfile(file)
   
def logo_enterHoover(e):
    global msgboxLogo
    msgboxLogo = tk.Label(wnd,text='Site internet ESEO', font='Helvetica 10 italic')
    msgboxLogo.place(x=50, y=530)

def modele_enterHoover(e):
    global msgboxModele
    msgboxModele = tk.Label(wnd,text='Dossier de première année', font='Helvetica 10 italic')
    msgboxModele.place(x=200, y=165)


#//////////////////////////#


### Lecture du fichier ###
def lire_Carte(fichier):
    carte = []
    with open(f'{fichier}', 'r', encoding='utf-8') as f:
        for ligne in f:
            L1 = []
            for caractere in ligne[:-1]:
                L1 += [int(caractere)]
            carte += [L1]
    #print(carte)
    return carte


### Lecture de la matrice puis représentation graphique pour la densitée###
def creation_grille(M,hauteur_fenêtre,cnv,coox,cooy):
    carreY = len(M[0])
    carreX = len(M[0])
    pasX=hauteur_fenêtre/carreX
    pasY=hauteur_fenêtre/carreY
    for x in range (carreY):
        for y in range(carreX):
            if (M[y][x]==1):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="light coral",outline="grey72")
            if (M[y][x]==2):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="coral",outline="grey72")
            if (M[y][x]==3):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="tomato",outline="grey72")
            if (M[y][x]==4):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="orange red",outline="grey72")
            if (M[y][x]==5):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="red",outline="grey72")
    cnv.place(x=coox,y=cooy)
    cnv.update()
    cnv.after(100)

    
### Lecture de la matrice puis représentation graphique pour la matrice SEITM ###
def creation_grilleSEITM(M,hauteur_fenêtre,cnv,coox,cooy,V):
    carreY = len(M[0])
    carreX = len(M[0])
    pasX=hauteur_fenêtre/carreX
    pasY=hauteur_fenêtre/carreY
    
    for x in range (carreY):
        for y in range(carreX):
            if (M[y][x]==0):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="grey",width=0)
            if (M[y][x]==1):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="white",outline="grey")
            if (M[y][x]==2):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="red",outline="grey")
            if (M[y][x]==3):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="yellow",outline="grey")
            if (M[y][x]==4):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="blue",outline="grey")
            if (M[y][x]==5):
                cnv.create_rectangle(x*pasX, y*pasY, (x+1)*pasX, (y+1)*pasY, fill="black",outline="grey")
            if (V[y][x]==1):
                cnv.create_text((x+0.15)*pasX,(y+0.15)*pasY,text='V')
                
    cnv.place(x=coox,y=cooy)
    cnv.update()
    cnv.after(100)


### Fonction associé au bouton 'Appliquer'
def appliquer_Fonction():
    global dens, carte, tailleAff
    for i in listebox.curselection():
        dens = str(listebox.get(i))
    #print(dens)
    fichier = f'assets\cartes\{dens}.txt'
    carte = lire_Carte(fichier)
    creation_grille(carte, 400, cnv8, 430, 120)
    
    tailleAff.configure(text=f"Taille de la carte : {len(carte)}x{len(carte)}")
    tailleAff.place(x=720,y=550)
    
    change_valeur(valeur2,len(carte))
         
    return(dens)


### Fonction d'auto complétion de la dim de la matrice suivant la carte choisie 
def change_valeur(entry,valeur):
    entry.delete(0,'end')
    entry.insert(0,valeur)    


### Création d'un fichier contenant les paramètres de la simulation ###
def sauvegardeDonées(nom_fichier, nbr_jour, longueur, inf, pei, tse, pts, tim, pit,dateheure,dens):
    f=open(nom_fichier, 'w',encoding='utf-8')
    f.write('Date et Heure de la Simulation : ' + str(dateheure) +'\n')
    f.write('-----------------------------------------------------'+'\n')    
    f.write('Nombre de jours de la simulation : ' + str(nbr_jour) + '\n')
    f.write('Longueur de la matrice carrée : ' + str(longueur) +'\n')
    f.write('Nombre de personne infectées au départ : ' + str(inf) +'\n')
    f.write('Période de passage de Exposé à Infecté : ' + str(pei) +'\n')
    f.write('Taux de passage de Sain à Exposé : ' + str(tse) +'\n')
    f.write('Période de passage de Temporairement Immunisé à Sain : ' + str(pts) +'\n')
    f.write('Taux de passage de Infecté à Mort : ' + str(tim) +'\n')
    f.write('Période de passage de Infecté à Temporairement Immunisé : ' + str(pit) +'\n')
    f.write('Carte de densité appliquée à la simulation : ' + str(dens) +'\n') 
    f.write('-----------------------------------------------------'+'\n')
    f.close()


### Action de la fonction page_Simulation ###
def formulaire(valeur1, valeur2, valeur3, valeur4, valeur5, valeur6, valeur7, valeur8):
    global nom_fichier
    nbr_jour =valeur1.get() #nombre de jour
    longueur =valeur2.get() #longueur (côté) de la matrice
    inf =valeur3.get() #nombre de personne infecté au départ
    tse =valeur4.get() #taux d'infectiosité
    pei =valeur5.get() #période d'infection
    pit =valeur6.get() #période de rétablissement
    pts =valeur7.get() #période de perte d'immunité
    tim =float(valeur8.get()) #taux de mortalilté
    dateheure = str(datetime.datetime.now())
    dateheure2 = list(dateheure)
    dateheure2[13] = 'h'
    dateheure2[16] = 'min'
    dateheure2[19] = 's'
    date = ''.join(dateheure2[0:20])
    nom_fichier = f'{dossier}\{date}.txt'
    sauvegardeDonées(nom_fichier, nbr_jour, longueur, inf, pei, tse, pts, tim, pit,dateheure,dens)
    return (nbr_jour, longueur, inf, pei, tse, pts, tim, pit,dateheure)


# Action de la fonction associée au bouton 'Lancer la simulation'
def lancerSim_Fonction():
    global nbr_jour, longueur, inf, pei, tse, pts, tim, pit, dateheure
    nbr_jour, longueur, inf, pei, tse, pts, tim, pit,dateheure = formulaire(valeur1, valeur2, valeur3, valeur4, valeur5, valeur6, valeur7, valeur8)
    nbr_jour, longueur, inf, pei, tse, pts, tim, pit, dateheure = int(nbr_jour), int(longueur), int(inf), int(pei), float(tse), int(pts), float(tim), int(pit), dateheure
    
    #print(nbr_jour, longueur, inf, pei, tse, pts, tim, pit, dateheure)

    page_Simulation()
    
    
def commencerSim_Fonction():
    global S,E,I,T,M
    
    commencerSim.destroy()
    
    cnv3.after(100)
    
    #testAltern(nbr_jour)
    #testGrille()
    Exécuter_SEITM(nbr_jour,longueur,inf)
    trace(sain, exposé, infecté, temp_immu, mort,dateheure)
    
    page_Graph()


#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#


### Page d'accueil du launcher ###
def page_Accueil():
    global image_modele, image_contagion, image_densité, image_logo
    
    image_modele = tk.PhotoImage(file='assets\images\illustration1.png')
    image_densité = tk.PhotoImage(file='assets\images\illustration2.png')
    image_contagion = tk.PhotoImage(file='assets\images\illustration3.png')
    image_logo = tk.PhotoImage(file='assets\images\logo.png')
    
    illustration3 = tk.Label(wnd, image = image_contagion, borderwidth=0)
    illustration3.place(x=33 ,y=0)
    
    illustration1 = tk.Label(wnd, image = image_modele, borderwidth=0)
    illustration1.place(x=10,y=10)
    illustration1.bind("<Button-1>", lambda e:open_file(file_DossierTIPE))
    illustration1.bind('<Enter>', modele_enterHoover)
    illustration1.bind('<Leave>', lambda e:msgboxModele.destroy())


    illustration2 = tk.Label(wnd, image = image_densité, borderwidth=0)
    illustration2.place(x=690 ,y=390)    
    
    logo = tk.Label(wnd, image = image_logo, cursor="hand2", borderwidth=0)
    logo.place(x=0 ,y=570) 
    logo.bind("<Button-1>", lambda e:open_url(url))
    logo.bind('<Enter>', logo_enterHoover)
    logo.bind('<Leave>', lambda e:msgboxLogo.destroy())
    
    titre = tk.Label(wnd, text="La fouloscopie au service de l'épidémiologie", font='Helvetica 19 bold italic', background='white')
    titre.place(x=350,y=50)
    
    Button1 = tk.Button(wnd, text="Simuler une épidémie", font='Helvetica 13 bold', command=page_Tuto1, relief='groove')
    Button1.pack(side='bottom',pady='50')
    Button1.bind('<Enter>', lambda e:Button1.config(background='OrangeRed3', foreground= "white"))
    Button1.bind('<Leave>', lambda e:Button1.config(background= 'SystemButtonFace', foreground= 'black'))

    return()



#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#


### Page du tuto du launcher ###
def page_Tuto1():
    global tutoPage1, image_tutoPage1
    
    #On efface les éléments de la fenêtre précédente :
    for w in wnd.winfo_children():
        w.destroy()
    
    image_tutoPage1 = tk.PhotoImage(file='assets\images\Tuto_Page_1.png')
    tutoPage1 = tk.Label(wnd, image = image_tutoPage1, borderwidth=0)
    tutoPage1.place(x=0 ,y=0)
    
    
    Suite = tk.Button(wnd, text="Suite", command=page_Données)
    Suite.pack(side='bottom',pady='50')
    Suite.bind('<Enter>', lambda e:Suite.config(background='OrangeRed3', foreground= "white"))
    Suite.bind('<Leave>', lambda e:Suite.config(background= 'SystemButtonFace', foreground= 'black'))


    return()



### Page du formulaire de données ###
def page_Données():
    global cnv10
    
    global sain, infecté, exposé, temp_immu, mort
    sain = [0] #1
    infecté = [0] #2
    exposé = [0] #3
    temp_immu = [0] #4
    mort = [0] #5
    
    #On efface les éléments de la fenêtre précédente :
    for w in wnd.winfo_children():
        w.destroy()

    global condition
    condition = 0

    formulaire_Données()
    #initialisation du formulaire :
    change_valeur(valeur1, 180)
    change_valeur(valeur2, 10)
    change_valeur(valeur3, 3)
    change_valeur(valeur4, 0.5)
    change_valeur(valeur5, 2)
    change_valeur(valeur6, 5)
    change_valeur(valeur7, 7)
    change_valeur(valeur8, 0.001)
    
    
    global vacc, tensHosp, muta
    vacc = tk.IntVar()
    tensHosp = tk.IntVar()
    muta = tk.IntVar()
    
    c1 = tk.Checkbutton(wnd, text='Vaccination',variable=vacc, onvalue=1, offvalue=0, command=None)
    c1.place(x=20,y=430)
    c2 = tk.Checkbutton(wnd, text='Tension Hospitalière',variable=tensHosp, onvalue=1, offvalue=0, command=None)
    c2.place(x=20,y=460)
    c3 = tk.Checkbutton(wnd, text='Mutation',variable=muta, onvalue=1, offvalue=0, command=None)
    c3.place(x=20,y=490)
    
    
    cnv10 = tk.Canvas(wnd, bd=0, width=5, height=560)
    cnv10.create_rectangle(0,0,5,560, fill='grey', width=0)
    cnv10.place(x=370, y=20)
    
    menu_Déroulant()
    
    prévisualisation_Densité()

    Button2 = tk.Button(wnd, text='Lancer la simulation', command=lancerSim_Fonction)
    Button2.place(x=125,y=530)
    Button2.bind('<Enter>', lambda e:Button2.config(background='OrangeRed3', foreground= "white"))
    Button2.bind('<Leave>', lambda e:Button2.config(background= 'SystemButtonFace', foreground= 'black'))
    
    return()

#//////////////////////////#


### Zone de la fenêtre associé au paramètre densité ###
def prévisualisation_Densité():
    global cnv8, tailleAff, current_value, value_label
    
    fichier = f'assets\cartes\{dens}.txt'
    carte = lire_Carte(fichier)
    
    cnv8 = tk.Canvas(wnd, width=400, height=400)
    creation_grille(carte, 400, cnv8, 430, 120)
    
    tailleAff = tk.Label(wnd, text=f"Taille de la carte : {len(carte)}x{len(carte)}")
    tailleAff.place(x=720,y=550)
    
    procedureDens = tk.Label(wnd, text = u"(\u25B6 Plus d'information)", borderwidth=0)
    procedureDens.place(x=460,y=80)
    procedureDens.bind("<Button-1>", lambda e:open_file(file_ProcedureDensite))
    procedureDens.bind('<Enter>', lambda e:procedureDens.config(fg='OrangeRed3'))
    procedureDens.bind('<Leave>', lambda e:procedureDens.config(fg='black'))
    
    # slider current value
    current_value = tk.DoubleVar()
    
    # label for the slider
    slider_label = ttk.Label(wnd, text='Importance du facteur de densité :')
    slider_label.place(x=420,y=530)

    #  slider
    slider = ttk.Scale(wnd, from_=0, to=100, orient='horizontal', command=slider_changed, variable=current_value)
    slider.place(x=420,y=550)


    # value label
    value_label = ttk.Label(wnd, text=get_current_value())
    value_label.place(x=540,y=552)
    
    appliquer_Fonction()
    
    return()


#//////////////////////////#


def get_current_value():
    global factdens
    factdens = current_value.get()
    return '{: .2f} %'.format(current_value.get())


#//////////////////////////#


def slider_changed(event):
    value_label.configure(text=get_current_value())


#//////////////////////////#


def menu_Déroulant():
    global cnv9, listebox, titre2

    titre2 = tk.Label(wnd,text='Carte de densité appliquée :', font='Helvetica 18 bold')
    titre2.place(x=400, y=40)

    cnv9 = tk.Frame(wnd)
    cnv9.place(x=730, y=35)
    
    listebox = tk.Listbox(cnv9,width=20, height=1, justify='center')
    listebox.pack(side='left')
    
    sb = tk.Scrollbar(cnv9, orient='vertical')
    sb.pack(side='right', fill='y')
    
    listebox.configure(yscrollcommand=sb.set)
    sb.config(command=listebox.yview)
    
    listebox.insert(0, "carte0")
    listebox.insert(1, "carte1")
    listebox.insert(2, "carte2")
    listebox.insert(3, "carte3")
    listebox.insert(4, "carte4")
    listebox.insert(5, "carte5")
    listebox.insert(6, "carte6")
    listebox.insert(7, "carte7")
    listebox.insert(8, "carte8")
    listebox.insert(9, "carte9")
    listebox.insert(10, "carte10")
    
    appliquer_Button = tk.Button(wnd, text='Appliquer', command=appliquer_Fonction)
    appliquer_Button.place(x=760,y=80)
    appliquer_Button.bind('<Enter>', lambda e:appliquer_Button.config(background='OrangeRed3', foreground= "white"))
    appliquer_Button.bind('<Leave>', lambda e:appliquer_Button.config(background= 'SystemButtonFace', foreground= 'black'))
    
    return()


#//////////////////////////#


def formulaire_Données():
    global valeur1, valeur2, valeur3, valeur4, valeur5, valeur6, valeur7, valeur8, titre1
    global msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8

    titre1 = tk.Label(wnd,text='Données de la simulation :', font='Helvetica 18 bold')
    titre1.place(x=20, y=100)

    valeur1 = tk.Entry(wnd, width = 5)
    valeur1.place(x=20, y=150)
    msg1 = tk.Label(wnd, text=" : Nombre de jours de la simulation")
    msg1.place(x=60, y=150)
    valeur1.bind('<Enter>', lambda e:msg1.config(fg='OrangeRed3'))
    valeur1.bind('<Leave>', lambda e:msg1.config(fg='black'))
    


    valeur2 = tk.Entry(wnd, width = 5)
    valeur2.place(x=20, y=180)
    msg2 = tk.Label(wnd, text=" : Longueur de la matrice carrée")
    msg2.place(x=60, y=180)
    valeur2.bind('<Enter>', lambda e:msg2.config(fg='OrangeRed3'))
    valeur2.bind('<Leave>', lambda e:msg2.config(fg='black'))

    

    valeur3 = tk.Entry(wnd, width = 5)
    valeur3.place(x=20, y=210)
    msg3 = tk.Label(wnd, text=" : Nombre de personnes infectées au départ")
    msg3.place(x=60, y=210)
    valeur3.bind('<Enter>', lambda e:msg3.config(fg='OrangeRed3'))
    valeur3.bind('<Leave>', lambda e:msg3.config(fg='black'))

    
    
    valeur4 = tk.Entry(wnd, width = 5)
    valeur4.place(x=20, y=240)
    msg4 = tk.Label(wnd, text=" : Taux d'infectiosité")
    msg4.place(x=60, y=240)
    valeur4.bind('<Enter>', lambda e:msg4.config(fg='OrangeRed3'))
    valeur4.bind('<Leave>', lambda e:msg4.config(fg='black'))

    
    
    valeur5 = tk.Entry(wnd, width = 5)
    valeur5.place(x=20, y=270)
    msg5 = tk.Label(wnd, text=" : Durée de l'infection")
    msg5.place(x=60, y=270)
    valeur5.bind('<Enter>', lambda e:msg5.config(fg='OrangeRed3'))
    valeur5.bind('<Leave>', lambda e:msg5.config(fg='black'))

    
    
    valeur6 = tk.Entry(wnd, width = 5)
    valeur6.place(x=20, y=300)
    msg6 = tk.Label(wnd, text=" : Durée de rétablissement")
    msg6.place(x=60, y=300)
    valeur6.bind('<Enter>', lambda e:msg6.config(fg='OrangeRed3'))
    valeur6.bind('<Leave>', lambda e:msg6.config(fg='black'))

    
    
    valeur7 = tk.Entry(wnd, width = 5)
    valeur7.place(x=20, y=330)
    msg7 = tk.Label(wnd, text=" : Durée de perte d'immunité")
    msg7.place(x=60, y=330)
    valeur7.bind('<Enter>', lambda e:msg7.config(fg='OrangeRed3'))
    valeur7.bind('<Leave>', lambda e:msg7.config(fg='black'))

    
    
    valeur8 = tk.Entry(wnd, width = 5)
    valeur8.place(x=20, y=360)
    msg8 = tk.Label(wnd, text=" : Taux de mortalité")
    msg8.place(x=60, y=360)
    valeur8.bind('<Enter>', lambda e:msg8.config(fg='OrangeRed3'))
    valeur8.bind('<Leave>', lambda e:msg8.config(fg='black'))

    return(nbr_jour, longueur, inf, pei, tse, pts, tim, pit, dateheure)


#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#


def page_Simulation():
    global compteur, commencerSim, cnv3, image_stop
    
    #On efface les éléments de la fenêtre précédente :
    for w in wnd.winfo_children():
        w.destroy()

    
    image_stop = tk.PhotoImage(file='assets\images\stop.png')
    stop = tk.Button(wnd, image = image_stop, command=stopFonction, compound = 'left')
    stop.place(x=600,y=0)
    
    compteur = tk.Label(wnd, text='Jour : 0', font='Helvetica 13 bold')
    compteur.place(x=720, y=5)
    
    données_PageSim()
    densité_PageSim()
    
    cnv3 = tk.Canvas(wnd, width=600, height=600)
    cnv3.place(x=0,y=0)
    
    commencerSim = tk.Button(wnd, text='Commencer la Simulation', command=commencerSim_Fonction)
    commencerSim.place(x=230,y=270)
    commencerSim.bind('<Enter>', lambda e:commencerSim.config(background='OrangeRed3', foreground= "white"))
    commencerSim.bind('<Leave>', lambda e:commencerSim.config(background= 'SystemButtonFace', foreground= 'black'))
    
    return()

#//////////////////////////#
def stopFonction():
    global condition
    condition = 1

#//////////////////////////#

# Affichage de la carte de densité appliquée :
def densité_PageSim():
    global cnv6
    
    fichier = f'assets\cartes\{dens}.txt'
    carte = lire_Carte(fichier)
    
    cnv6 = tk.Canvas(wnd, width=300, height=300)
    creation_grille(carte, 300, cnv6, 600, 300)

    return()

#//////////////////////////#

# Affichage des données saisie précédement :
def données_PageSim():
    global msgtim
    
    msg1 = tk.Label(wnd, text='Nombre de jours de la simulation : ' + str(nbr_jour))
    msg1.place(x=610,y=50)
    
    msg2 = tk.Label(wnd, text='Nombre de personnes : ' + str(longueur**2))
    msg2.place(x=610, y=80)

    msg3 = tk.Label(wnd, text='Nombre de personnes infectées au départ : ' + str(inf))
    msg3.place(x=610, y=110)

    msg4 = tk.Label(wnd, text="Durée de l'infection : " + str(pei))
    msg4.place(x=610, y=140)

    msg5 = tk.Label(wnd, text="Taux d'infectiosité : " + str(tse))
    msg5.place(x=610, y=170)

    msg6 = tk.Label(wnd, text="Durée de l'immunité : " + str(pts))
    msg6.place(x=610, y=200)

    msgtim = tk.Label(wnd, text='Taux de mortalité : ' + str(tim))
    msgtim.place(x=610, y=230)

    msg8 = tk.Label(wnd, text='Durée de rétablissement : ' + str(pit))
    msg8.place(x=610, y=260)
    
    return()

#//////////////////////////#

# Affichage de la carte de densité appliquée :
def grille_PageSim():
    global cnv3
    
    cnv3 = tk.Canvas(wnd, width=600, height=600)
    creation_grilleSEITM(M_test, 300, cnv3, 0, 0, V)

    return()

#//////////////////////////#


#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#
#//////////////////////////#

def page_Graph():
    global image_courbes, COURBES
    
    cnv3.after(1000)
    cnv3.destroy()
    
    image_courbes = tk.PhotoImage(file=nom_fichier_courbes)
    COURBES = tk.Label(wnd, image = image_courbes, borderwidth=0)
    COURBES.place(x=84 ,y=100)
    

    reSim = tk.Button(wnd, text='Simuler une autre épidémie', command=page_Données)
    reSim.place(x=155,y=480)
    reSim.bind('<Enter>', lambda e:reSim.config(background='OrangeRed3', foreground= "white"))
    reSim.bind('<Leave>', lambda e:reSim.config(background= 'SystemButtonFace', foreground= 'black'))
    
    quitterButton = tk.Button(wnd, text='Quitter', command=wnd.destroy)
    quitterButton.place(x=350,y=480)
    quitterButton.bind('<Enter>', lambda e:quitterButton.config(background='OrangeRed3', foreground= "white"))
    quitterButton.bind('<Leave>', lambda e:quitterButton.config(background= 'SystemButtonFace', foreground= 'black'))
    
    ouvrirDossier = tk.Label(wnd, text = f'(Ouvrir le dossier "{dossier}")', borderwidth=0)
    ouvrirDossier.place(x=200,y=510)
    ouvrirDossier.bind("<Button-1>", lambda e:open_file(dossier))
    ouvrirDossier.bind('<Enter>', lambda e:ouvrirDossier.config(fg='OrangeRed3'))
    ouvrirDossier.bind('<Leave>', lambda e:ouvrirDossier.config(fg='black'))
   

    return()

    

#///////////////////////////////////#
#///////////////////////////////////#
#/////          SEITM          /////#
#///////////////////////////////////#
#///////////////////////////////////#

def initMat(A,inf,pit):
    n=2+A
    I=[None]*n
    J=[0]*A            #Création matrice état; compteur; passage
    K=[0]*A
    
    global V
    V = [0]*n
    for i in range(len(V)):
        V[i] = [0]*n
    
    for i in range(A): #init Matrice compteur; passage de taille A*A
        J[i]=[0]*A
        K[i]=[0]*A
    for i in range(n): #init Matrice état de taille(A+2)*(A+2)
        I[i]=[None]*n
        
    for j in range(n): #placement des bordures de la matrice état
        if j==0:
            for i in range(n):
                I[j][i]=0
        if 0<j<n-1:
            I[j][0]=I[j][n-1]=0
        else :
            for i in range(n):
                I[j][i]=0
    for j in range(1,A+1): #placement des personnes saines
        for i in range (1,A+1):
            I[j][i]=1
    for k in range(inf):#placement des inféctées de façon aléatoire
        a=r.randint(1,A)
        b=r.randint(1,A)
        if I[a][b]!=2:
            I[a][b]=2
            K[a-1][b-1]=pit
        else:
            while I[a][b]==2:
                a=r.randint(1,A)
                b=r.randint(1,A)
            I[a][b]=2
            K[a-1][b-1]=pit
    return I,J,K,V

#////////////////////////////////#

def SE(i,j,A,B,C): #passage de l'etat sain a exposé
                I=0  #initialisation d'un compteur
                for k in range(-1,2): #parcours des cellules autour de la personnes saine
                    for l in range(-1,2):
                        if A[i+k][j+l]==2: 
                            I+=1 # si il y a un infectée le compteur augmente
                if I==0:        #si le compteur est à 0 : pas d'infectée donc pas de risque d'infection
                                #le sain reste saine
                    B[i-1][j-1]=1
                else:
                    for m in range(I):
                        z=(r.randint(0,100) - 100*(1 - math.exp(-(factdens*0.01)/(carte[i-1][j-1]))))
                        k=0
                        if z<(tse*100):
                            B[i-1][j-1]=3
                            C[i-1][j-1]=pei
                            k=1
                    if k==0:
                         B[i-1][j-1]=1
                         C[i-1][j-1]=0
                return A,B,C

#////////////////////////////////#

def EI(i,j,A,B,C):
                if C[i-1][j-1]==0:
                    if V[i][j]==1:
                        C[i-1][j-1]=pit//3
                        B[i-1][j-1]=2
                    elif V[i][j]==0:
                        B[i-1][j-1]=2
                        C[i-1][j-1]=pit
                else:
                    x=C[i-1][j-1]
                    C[i-1][j-1]=x-1
                    B[i-1][j-1]=3
                return A,B,C
                    
#////////////////////////////////#

def TS(i,j,A,B,C):
                if C[i-1][j-1]==0:
                    B[i-1][j-1]=1
                    C[i-1][j-1]=0
                else:
                    x=C[i-1][j-1]
                    C[i-1][j-1]=x-1
                    B[i-1][j-1]=4
                return A,B,C

#////////////////////////////////#                    
            
def ITM(i,j,A,B,C):
                if C[i-1][j-1]==0:
                    B[i-1][j-1]=4
                    C[i-1][j-1]=pts
                    return A,B,C
                elif r.randint(0,99)<(tim*100):
                    B[i-1][j-1]=5
                    C[i-1][j-1]=0
                    return A,B,C
                else :
                    C[i-1][j-1]-=1
                    B[i-1][j-1]=2
                return A,B,C
                            
#////////////////////////////////#
                            
def scan(A,B,C,V):
    for i in range(1,len(A)-1):
        for j in range(1,len(A)-1):
            if A[i][j]==1:
                A,B,C=SE(i,j,A,B,C)
            if A[i][j]==2:
                A,B,C=ITM(i,j,A,B,C)
            if A[i][j]==3:
                A,B,C=EI(i,j,A,B,C)
            if A[i][j]==4:
                A,B,C=TS(i,j,A,B,C)
    return A,B,C

#////////////////////////////////#

def AdevientB(A,B):
    for i in range(1,len(A)-1):
        for j in range(1,len(A)-1):
           A[i][j]=B[i-1][j-1]
    return A

#////////////////////////////////#        

def TEST_SEITM(n,Longueur,inf):
    global pei,tse,pts,tim,pit
    A,B,C=initMat(Longueur,inf,pit)
    for k in range(n):
        A,B,C=scan(A,B,C)
        A=AdevientB()
        print(k)
    return A,B,C
        
#////////////////////////////////#

def f_tension_Hospitaliere(tim,i,chgm,capa_hopit):

    prcinf = (infecté[i]*100)/((longueur**2)-mort[i])
    
    if chgm==False and prcinf>capa_hopit:
        chgm=True
        tim=tim*2
        liste_tens.append(i)
    elif chgm==True and prcinf<=capa_hopit:
        chgm=False
        tim=tim/2
        liste_tens.append(i)
    msgtim.config(text = f"Taux de mortalité : {str(tim)}")
    return(tim,chgm)


#////////////////////////////////#            
        
def add_donnees_muta(nom_fichier,jmutation,pei,pts,pit,tse,tim):
    f=open(nom_fichier, 'a',encoding='utf-8')
    f.write('-----------------------------------------------------'+'\n')
    f.write('Jour de la mutation : ' + str(jmutation) + '\n')
    f.write('Nouvelle période de passage de Exposé à Infecté : ' + str(pei) +'\n')
    f.write('Nouveau taux de passage de Sain à Exposé : ' + str("{:.2f}".format(tse)) +'\n')
    f.write('Nouvelle période de passage de Temporairement Immunisé à Sain : ' + str(pts) +'\n')
    f.write('Nouveaux taux de passage de Infecté à Mort : ' + str("{:.4f}".format(tim)) +'\n')
    f.write('Nouvelle période de passage de Infecté à Temporairement Immunisé : ' + str(pit) +'\n')
    f.write('-----------------------------------------------------'+'\n')
    f.close()

#////////////////////////////#

def add_donnees_PageSim(jmutation,pei,pts,pit,tse,tim):

    msg4 = tk.Label(wnd, text=u"\u279E       " + str(pei), fg='blue')
    msg4.place(x=800, y=140)

    msg5 = tk.Label(wnd, text=u"\u279E       " + str("{:.2f}".format(tse)), fg='blue')
    msg5.place(x=800, y=170)

    msg6 = tk.Label(wnd, text=u"\u279E       " + str(pts), fg='blue')
    msg6.place(x=800, y=200)

    msg7 = tk.Label(wnd, text=u"\u279E       " + str("{:.4f}".format(tim)), fg='blue')
    msg7.place(x=800, y=230)

    msg8 = tk.Label(wnd, text=u"\u279E       " + str(pit), fg='blue')
    msg8.place(x=800, y=260)
    
    
#////////////////////////////////#
    
def f_mutation(i,jmutation,pei,pts,pit,tse,tim):
    if i==jmutation:
        pei+=r.randint(-((pei//10)+1),((pei//10)+1))
        pts+=r.randint(-((pts//10)+1),((pts//10)+1))
        pit+=r.randint(-((pit//10)+1),((pit//10)+1))
        tse2=tse+(r.randint(-((tse*100//10)),((tse*100//10)))+(r.randint(-2,2)*10))/100
        if tse2<0:
            tse2=0.01
        if tse2<tse:
            tim+=r.randint(0,((tim*100//10)+(r.randint(0,2)*10)))/100
        else:
            tim+=r.randint(-((tim*100//10)+(r.randint(0,2)*10)),0)/100
            if tim<0:
                tim=0.01
        tse=tse2
        
        add_donnees_muta(nom_fichier,jmutation,pei,pts,pit,tse,tim)
        add_donnees_PageSim(jmutation, pei, pts, pit, tse, tim)
        #print("new pei=",pei)
        #print("new pts=",pts)
        #print("new pit=",pit)
        #print("new tse=",tse)
        #print("new tim=",tim)
    return(pei,pts,pit,tse,tim)

#////////////////////////////////#

def Exécuter_SEITM(nbr_jour,longueur,nbr_infecté):
    global pei, tse, pts, tim, pit, sain, exposé, infecté, temp_immu, mort
    global condition
    
    A,B,C,V=initMat(longueur,nbr_infecté,pit)
    
    creation_grilleSEITM(A,600,cnv3,0,0,V)
    cnv3.update()
    cnv3.after(100)
    
    sain, exposé, infecté, temp_immu, mort = Recup_Valeurs(A)
    
    if (tensHosp.get() == 1):
        global liste_tens
        liste_tens = []
        chgm=False
        capa_hopit=(longueur**2)//10
        
    if (muta.get() == 1):
        global jmutation
        jmutation=nbr_jour//2
        #print(jmutation)

    for i in range (0,nbr_jour):
        
        if condition == 1:
            return()
        
        if (tensHosp.get() == 1):
            f_tension_Hospitaliere(tim, i, chgm, capa_hopit)
            
        if (muta.get() == 1):
            pei,pts,pit,tse,tim = f_mutation(i, jmutation, pei, pts, pit, tse, tim)
            msg1 = tk.Label(wnd, text=f'(Mutation : Jour {str(jmutation)})', fg='blue')
            msg1.place(x=780,y=65)
        
        compteur = tk.Label(wnd, text=f'Jour : {i+1}', font='Helvetica 13 bold')
        compteur.place(x=720, y=5)
        
        A,B,C=scan(A,B,C,V)
        A=AdevientB(A,B)
        
        if i>nbr_jour/2 and (vacc.get() == 1) :
            for k in range(1,len(V)-1):
                for j in range(1,len(V)-1):
                    if V[k][j]==0 and 5>r.randint(0,100):
                        V[k][j]=1
        
        creation_grilleSEITM(A, hauteur_fenêtre,cnv3, 0, 0, V)
        cnv3.update()
        cnv3.after(100)
        
        sain, exposé, infecté, temp_immu, mort = Recup_Valeurs(A)
        #print('Fait')
    #print(liste_tens)

    return()

#////////////////////////////////#

def testAltern(nbr_jour):
    a=0
    for i in range (0,nbr_jour):
        if a==1:
            a=0
        elif a==0 :
            a=1
        
        if a==1:
            cnv3.configure(background='blue')
            cnv3.update()
        else :
            cnv3.configure(background='red')
            cnv3.update()
        cnv3.after(100)
    return()

#////////////////////////////////#

def testGrille():
    creation_grilleSEITM(M_test, 600, cnv3, 0, 0, V)
    return()

#////////////////////////////////#

### Test ###   
#A,B,C = initMat(5, 2, 3)

#///////////////////////////////////#
#///////////////////////////////////#
#/////     Représentation      /////#
#///////////////////////////////////#
#///////////////////////////////////#


### Matrice de Test ###
def Matrice(n):
    M = [[r.randint(1,5) for _ in range (0,n+1)] for _ in range (0,n+1)]
    for i in range(0,n+1):
        M[0][i]=0
        M[n][i]=0
        for j in range (1,n+1):
            M[j][0]=0
            M[j][n]=0
    return(M)

M_test = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 4, 2, 1, 3, 5, 1, 4, 4, 4, 0],
          [0, 3, 5, 3, 1, 4, 4, 2, 4, 2, 0],
          [0, 2, 5, 2, 4, 3, 2, 3, 3, 2, 0],
          [0, 3, 3, 1, 1, 2, 5, 3, 2, 5, 0],
          [0, 4, 2, 1, 2, 3, 1, 5, 1, 4, 0],
          [0, 1, 4, 2, 5, 3, 5, 3, 4, 4, 0],
          [0, 4, 3, 2, 5, 5, 1, 4, 2, 3, 0],
          [0, 3, 4, 1, 1, 4, 2, 2, 1, 4, 0],
          [0, 3, 3, 2, 2, 4, 3, 5, 1, 3, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


"""
### Simulation de SEITM ###
def SEITM_test(j=nbr_jour,n=10):
    for i in range(0,nbr_jour):
        M = Matrice(n)
        #print(M)
        creation_grille(M, hauteur_fenêtre)
        cnv3.update()
        sain, exposé, infecté, temp_immu, mort = Recup_Valeurs(M)
        #print('Fait')
        cnv3.after(1000)
    wnd.destroy()
    return(sain, exposé, infecté, temp_immu, mort)
"""        



### Récupération des listes ###
def Recup_Valeurs(M):
    global sain, infecté, temp_immu, exposé, mort
    sain[0] = (len(M)-2)**2
    s = 0
    i = 0
    t = 0
    e = 0
    m = 0
    n = len(M)-1
    for k in range (0,n):
        for j in range (0,n):
            if M[k][j] == 1 :
                s += 1          
            if M[k][j] == 2 :
                i += 1          
            if M[k][j] == 3 :
                e += 1          
            if M[k][j] == 4 :
                t += 1                
            if M[k][j] == 5 :
                m += 1
    sain.append(s)
    infecté.append(i)
    temp_immu.append(t)
    exposé.append(e)
    mort.append(m)
    return(sain, exposé, infecté, temp_immu, mort)

#////////////////////////////////#

#tracer d'une courbe à partir d'une liste
def trace(S,E,I,T,M,dateheure):
    global nom_fichier_courbes
 
    n = len(S)
    x = [i for i in range (0,n)]
    y = [i for i in range(0,S[0])]
    
    plt.clf()
    
    plt.title(dateheure)
    
    plt.plot(x,S,color='green')
    plt.plot(x,E,color='yellow')
    plt.plot(x,I,color='red')
    plt.plot(x,T,color='blue')
    plt.plot(x,M,color='black')
    
    if (muta.get() == 1):
        JMUTATION = [jmutation]*S[0]
        plt.plot(JMUTATION,y,color='grey', linestyle='dashed', linewidth = 3)
    
    plt.xlabel ('Jours')
    
    dateheure2 = list(dateheure)
    dateheure2[13] = 'h'
    dateheure2[16] = 'min'
    dateheure2[19] = 's'
    date = ''.join(dateheure2[0:20])
    
    plt.savefig(f'{dossier}\{date}.png')
    
    nom_fichier_courbes = f'{dossier}\{date}.png'

    
    """
    # create a figure
    figure = Figure(figsize=(6, 4), dpi=100)
    
    # create FigureCanvasTkAgg object
    figure_canvas = FigureCanvasTkAgg(figure, wnd)
    
    # create the toolbar
    NavigationToolbar2Tk(figure_canvas, wnd)
    
    n = len(S)
    x = [i for i in range (0,n)]
    
    # create axes
    axes = figure.add_subplot()
    
    # create the chart
    axes.plot(x,S,color='green')
    axes.plot(x,E,color='yellow')
    axes.plot(x,I,color='red')
    axes.plot(x,T,color='blue')
    axes.plot(x,M,color='black')
    
    axes.set_title(dateheure)
    axes.set_xlabel('Jours')
    
    figure_canvas.get_tk_widget().place(x=0,y=0)
    """





#///////////////////////////////////#
#///////////////////////////////////#
#/////         FENETRE         /////#
#///////////////////////////////////#
#///////////////////////////////////#


"""
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=hauteur_fenêtre, height=hauteur_fenêtre, bg='white')
S,E,I,T,M = Exécuter_SEITM(nbr_jour,longueur,inf)
trace(S,E,I,T,M,dateheure)

wnd.mainloop()
"""

### Création de la fenêtre ###

wnd = tk.Tk()
wnd.title('SEITM')
wnd.geometry(dimension)
wnd.resizable(height = 0, width = 0)

fond = tk.Canvas(wnd, width = 900, height = 600, bg = 'white')
fond.place(x=0,y=0)

page_Accueil()

wnd.mainloop()