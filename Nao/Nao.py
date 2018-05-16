# -*- coding:utf-8 -*-

import sys
import time
#import builtins
from tkinter import *
from tkinter import messagebox
from tkinter import TclError

import NAO_toiminnot as NAO #Tuodaan NAO_toiminnot moduuli
import SQL_toiminnot as SQL #Tuodaan SQL_toiminnot moduuli

class Gui():
    def __init__(s):
        s.__muokkaustila = 0    #Muuttuja joka tallentaa onko muokkaustila päällä vai pois
        s.__yhdistetty = 0
        s.__root = Tk()
        s.__root.resizable(0,0)
        s.__root.title("NAO tietokanta\t by:Roope Romu")
        """
        Ohjleman valikkopalkki
        """
        s.__valikkoPalkki=Menu(s.__root, relief=RAISED)
        s.__valikkoFile=Menu(s.__valikkoPalkki, tearoff=0,)
        s.__valikkoPalkki.add_cascade(label="File", menu=s.__valikkoFile)
        s.__valikkoRobotti=Menu(s.__valikkoPalkki, tearoff=0)
        s.__valikkoPalkki.add_cascade(label="NAO", menu=s.__valikkoRobotti)
        #valikkoFile objektit
        s.__valikkoFile.add_command(label="Päivitä", command=lambda: s.PaivitaOrja())
        s.__valikkoFile.add_command(label="Yhdistä", command=lambda: s.Yhdista())
        s.__valikkoFile.add_separator()
        s.__valikkoFile.add_command(label="Lopeta", command=lambda: s.__root.destroy())
        #valikkoRobotti objektit
        s.__valikkoRobotti.add_command(label="Lisää NAO", command=lambda: s.lisaaNao())
        s.__valikkoRobotti.add_command(label="Valitse NAO", command=lambda: s.valitseNao())

        """
        Ohjelman pääikkuna, joka on jaettu oikeaan ja vasempaan ruutuun.
        """
        s.__paaIkkuna=Frame(s.__root).grid(row=0, column=0, sticky='nsew')
        s.__paaIkkunaVasenSelite=Label(s.__paaIkkuna, text="", relief=GROOVE).grid(row=0, column=0, sticky='nsew')
        s.__paaIkkunaOikeaSelite=Label(s.__paaIkkuna, text="Käsiteltävä koodi", relief=GROOVE).grid(row=0, column=1, sticky='nsew')

        #paaIkkunaVasen ruudun vasemmanpuoliset objektit
        s.__paaIkkunaVasen=Frame(s.__paaIkkuna)
        s.__paaIkkunaVasen.grid(row=1, column=0, sticky=N+S)
        s.__paaIkkunaOrja=Frame(s.__paaIkkunaVasen)
        s.__paaIkkunaOrja.grid(row=1, column=0, sticky='nsew', padx=1)
        s.__paaIkkunaOrjaKuvaus=Text(s.__paaIkkunaOrja, width=30, height=10, wrap=WORD, state=DISABLED, bg="grey95")
        s.__paaIkkunaOrjaKuvaus.grid(row=2, column=0, columnspan=3, pady=1, padx=1)
        s.__paaIkkunaOrjaUusi=Button(s.__paaIkkunaOrja, text="Uusi", command=lambda: s.UusiToiminto()).grid(row=1, column=0, sticky=E+W)
        s.__paaIkkunaOrjaPaivita=Button(s.__paaIkkunaOrja, text="Päivitä", command=lambda: s.PaivitaOrja()).grid(row=1, column=1, sticky=E+W)
        s.__paaIkkunaOrjaPoista=Button(s.__paaIkkunaOrja, text="Poista", command=lambda: s.PoistaToiminto(), state=DISABLED)
        s.__paaIkkunaOrjaPoista.grid(row=1, column=2, sticky=E+W)
        s.__paaIkkunaLista=Listbox(s.__paaIkkunaVasen, width=30, height=25)
        s.__paaIkkunaLista.config(exportselection=False)
        s.__paaIkkunaLista.bind("<<ListboxSelect>>", s.ListboxValinta)
        s.__paaIkkunaLista.grid(row=2, column=0, sticky=E+W, pady=1, padx=1)
        for toiminto in sorted(SQL.tietokantaToimintoTiedot,key=str.lower):
            s.__paaIkkunaLista.insert('end', toiminto)

        #paaIkkunaText ruudun oikeanpuolinen ruutu.
        s.__paaIkkunaOikea=Frame(s.__paaIkkuna)
        s.__paaIkkunaOikea.grid(row=1, column=1)
        s.__paaikkunaOikeaTallenna=Button(s.__paaIkkunaOikea, text="Tallenna kuvaus/koodi", state=DISABLED, command=lambda: s.TallennaMuokattuKoodi()) #Tallentaa koodin tietokantaan
        s.__paaikkunaOikeaTallenna.grid(row=0, column=1, sticky=E+W)
        s.__paaikkunaOikeaMuokkaustila=Label(s.__paaIkkunaOikea, text="Muokkaustila:").grid(row=0, column=2, sticky=E)
        s.__paaIkkunaOikeaMuokkaa=Button(s.__paaIkkunaOikea, text="Päällä", command=lambda: s.Muokkaa(), width=8) #Mahdollista muokkaus texti kenttiin
        s.__paaIkkunaOikeaMuokkaa.grid(row=0, column=3, sticky=W)
        s.__paaIkkunaKoodi=Text(s.__paaIkkunaOikea, width=80, height=40, wrap=WORD, state=DISABLED, bg="grey95")
        s.__paaIkkunaKoodi.grid(row=1, column=0, rowspan=2, columnspan=4, pady=1, padx=1)
        s.__scrollbar=Scrollbar(s.__paaIkkunaOikea, command=s.__paaIkkunaKoodi.yview)
        s.__scrollbar.grid(row=1, column=5, rowspan=2, sticky='ns')
        s.__paaIkkunaKoodi['yscrollcommand'] = s.__scrollbar.set
        s.__paaIkkunaOikeaYhdista=Button(s.__paaIkkunaOikea, text="Yhdista", command=lambda: s.Connect(), width=9)
        s.__paaIkkunaOikeaYhdista.grid(row=4, column=0)
        s.__paaIkkunaOikeaSuorita=Button(s.__paaIkkunaOikea, text="Suorita", command=lambda: NAO.suoritaToiminto(koodi=s.__paaIkkunaKoodi.get("0.0", END)))      #Suorittaa koodin robotilla
        s.__paaIkkunaOikeaSuorita.grid(row=4, column=2, sticky=E)     
        s.__paaIkkunaOikeaLaheta=Button(s.__paaIkkunaOikea, text="Laheta")        #Lähettää koodin robotin muistiin
        s.__paaIkkunaOikeaLaheta.grid(row=4, column=3, sticky=W)

        """
        Ohjelman alapalkki, Palkissa on kello/päivämäärä ja Naon yhteyden tilan osoitin
        """
        s.__alapalkki=Frame(s.__root, bd=1, relief=RAISED, background="lightgrey")
        s.__alapalkki.grid(row=10, columnspan=10, sticky=E+W, padx=1)
        s.__alapalkkiYhdistetty=Label(s.__alapalkki, text="(D)", fg="black", width=2, background="lightgrey", anchor=W)
        s.__alapalkkiYhdistetty.grid(row=0, column=0)
        s.__alapalkkiRobotti=Label(s.__alapalkki, text=NAO.RobottiNimi, background="lightgrey", width=15, anchor=E)
        s.__alapalkkiRobotti.grid(row=0, column=1, sticky=E)
        s.__alapalkkiRobottiIP=Label(s.__alapalkki, text=NAO.RobottiIP, background="lightgrey", width=10, anchor=CENTER)
        s.__alapalkkiRobottiIP.grid(row=0, column=2, sticky=W)
        s.__alapalkkiRobottiPort=Label(s.__alapalkki, text=NAO.RobottiPort, background="lightgrey", width=5, anchor=W)
        s.__alapalkkiRobottiPort.grid(row=0, column=3, sticky=W)
        s.__alapalkkiKello=Label(s.__alapalkki, text="", background="Lightgrey", width=85, anchor=E)
        s.__alapalkkiKello.grid(row=0, column=5, columnspan=10)

        s.__root.config(menu=s.__valikkoPalkki)
        s.Kello()
        s.__root.mainloop()
        #Varmistetaan että ohjelma ja sen aliohjelmat sammuu.
        try:
            s.__root.destroy()
        except:
            sys.exit()
            pass

    def Kello(s):
        """
        Lyhyt funktio näyttämään aikaa, päivää ja päivämäärää 
        """
        now = time.strftime("%H:%M:%S\t%A %d/%m/%Y ")   #muuttuja now saa ajan
        s.__alapalkkiKello.configure(text=now)          #muuttaa alapalkin kellon tekstin now muuttujan mukaan
        s.__root.after(1000, s.Kello)                   #suorittaa funktion uudelleen 1s/1000ms jälkeen

    def Yhdistetty(s):  #Ohjelman yhdistetty, muokkaa alapalkin yhteyden tilaa osoittavia osia
        global YhdistaTehtava
        s.__paaIkkunaOikeaYhdista.config(text="Disconnect")
        X=NAO.testNaoYhteys()                                            #kutsuu NAO moduulista testNaoYhteys ja palautuksen mukaan muuttaa ulkoasun objekteja
        YhdistaTehtava=s.__root.after(10000, s.Yhdistetty)             #suorittaa funktion uudelleen 10s/10000ms jälkeen
        if X == "Y":
            s.__alapalkkiYhdistetty.configure(text="(Y)", fg="green")
            s.__paaIkkunaOikeaSuorita.configure(state=NORMAL)
            s.__paaIkkunaOikeaLaheta.configure(state=NORMAL)           
        elif X == "N":
            s.__alapalkkiYhdistetty.configure(text="(N)", fg="red")
            s.__paaIkkunaOikeaSuorita.configure(state=DISABLED)
            s.__paaIkkunaOikeaLaheta.configure(state=DISABLED)
        else:
            s.__alapalkkiYhdistetty.configure(text="(C)", fg="yellow")
            s.__paaIkkunaOikeaSuorita.configure(state=DISABLED)
            s.__paaIkkunaOikeaLaheta.configure(state=DISABLED)

    def Connect(s):
        if s.__yhdistetty == 0:
            s.__yhdistetty = 1
            s.__alapalkkiYhdistetty.configure(text="(C)", fg="yellow")
            s.Yhdistetty()
        else:
            s.__yhdistetty = 0
            s.__paaIkkunaOikeaYhdista.config(text="Connect")
            s.__alapalkkiYhdistetty.configure(text="(D)", fg="black")
            s.__root.after_cancel(YhdistaTehtava)

    def Muokkaa(s):
        """
        Muokkaa funktio joka muokkaa pääikkunan objekteja sen mukaan onko muokkaustila päällä vai poissa.
        """
        if s.__muokkaustila == 0:
            s.__paaIkkunaOrjaKuvaus.config(state=NORMAL, bg="white")
            s.__paaIkkunaKoodi.config(state=NORMAL, bg="white")
            s.__paaikkunaOikeaTallenna.config(state=NORMAL)
            s.__paaIkkunaOikeaMuokkaa.configure(text="Pois")
            s.__muokkaustila = 1
        else:
            s.__paaIkkunaOrjaKuvaus.config(state=DISABLED, bg="grey95")
            s.__paaIkkunaKoodi.config(state=DISABLED, bg="grey95")
            s.__paaikkunaOikeaTallenna.config(state=DISABLED)
            s.__paaIkkunaOikeaMuokkaa.configure(text="Päälle")
            s.__muokkaustila = 0 #MUOKKAUSTILAN koodi

    def PaivitaOrja(s): 
        """
        PäivitäOrja funktio joka tyhjentää listboxin sisällön ja tuo sen uudelleen
        """
        s.__paaIkkunaLista.delete(0, END)
        SQL.tietokantaToimintoTiedot.clear()
        SQL.tietokantaLaajuus.clear()
        SQL.tuoTietokanta()
        for toiminto in sorted(SQL.tietokantaToimintoTiedot,key=str.lower):
            s.__paaIkkunaLista.insert('end', toiminto)
        s.__paaIkkunaOrjaPoista.config(state=DISABLED)
        pass

    def ListboxValinta(s, event):
        """
        Listbox funktio joka kutsuttaessa valitsee listan objektin ja hakee sen mukaan
        SQL tietokannasta toiminnon kuvauksen ja koodin, sekä asettaa ne omille paikoilleen. 
        """
        try:
            widget = event.widget
            selection=widget.curselection()
            value = widget.get(selection)
            s.__paaIkkunaOrjaPoista.config(state=NORMAL)
            s.__paaIkkunaOrjaKuvaus.config(state=NORMAL)
            s.__paaIkkunaKoodi.config(state=NORMAL)
            s.__paaIkkunaOrjaKuvaus.delete('1.0', END)
            s.__paaIkkunaOrjaKuvaus.insert('1.0', SQL.tuoToiminto(value))
            s.__paaIkkunaKoodi.delete('1.0', END)
            s.__paaIkkunaKoodi.insert('1.0', SQL.tuoKoodi(value))
            s.__paaIkkunaOrjaKuvaus.config(state=DISABLED)
            s.__paaIkkunaKoodi.config(state=DISABLED)
            s.__paaikkunaOikeaTallenna.config(state=DISABLED)
            s.__paaIkkunaOikeaMuokkaa.configure(text="Päälle")
            s.__paaIkkunaOrjaKuvaus.config(bg="grey95")
            s.__paaIkkunaKoodi.config(bg="grey95")
            s.__muokkaustila = 0
        except TclError:
            pass

    def UusiToiminto(s):
        """
        UusiToiminto funktio joka avaa uuden ikkunan, johon käyttäjä syöttää tiedot.
        Tallenna painikkeella tiedot kerätään kentistä ja lähetetään UusiToimintoSQL funktiolle.
        Peruuta painike sulkee ohjelman
        """
        s.__uusiToimintoIkkuna=Toplevel()
        s.__uusiToimintoIkkuna.attributes("-topmost", True)
        s.__uusiToimintoIkkuna.title("Lisää uusi toiminto")
        s.__toiminnonNimiLab=Label(s.__uusiToimintoIkkuna, text="Toiminnon nimi:", width=15).grid(row=1, column=0, sticky=E)
        s.__toiminnonKuvausLab=Label(s.__uusiToimintoIkkuna, text="Toiminnon kuvaus:", width=15).grid(row=2, column=0, sticky=E)
        s.__toiminnonKoodiLab=Label(s.__uusiToimintoIkkuna, text="Toiminnon koodi:", width=15).grid(row=3, column=0, sticky=E)
        #Entrykentät
        s.__toiminnonNimiEnt=Entry(s.__uusiToimintoIkkuna)
        s.__toiminnonNimiEnt.grid(row=1, column=1, columnspan=2, sticky=W+E)
        s.__toiminnonKuvausEnt=Text(s.__uusiToimintoIkkuna, width=30, height=3, wrap=WORD)
        s.__toiminnonKuvausEnt.grid(row=2, column=1, columnspan=2, sticky=W)
        s.__toiminnonKoodiEnt=Text(s.__uusiToimintoIkkuna, width=30, height=10, wrap=WORD)
        s.__toiminnonKoodiEnt.grid(row=3, column=1, columnspan=2, sticky=W)
        s.__scrollbar=Scrollbar(s.__uusiToimintoIkkuna, command=s.__toiminnonKoodiEnt.yview)
        s.__scrollbar.grid(row=3, column=4, rowspan=1, sticky='ns')
        s.__toiminnonKoodiEnt['yscrollcommand'] = s.__scrollbar.set
        s.__toiminnonTallennaPainike=Button(s.__uusiToimintoIkkuna, text="Tallenna", command=lambda: s.UusiToimintoSQL(
                        toiminto=s.__toiminnonNimiEnt.get(),
                        kuvaus=s.__toiminnonKuvausEnt.get("0.0", END),
                        koodi=s.__toiminnonKoodiEnt.get("0.0", END)))
        s.__toiminnonTallennaPainike.grid(row=5, column=1, sticky=E, pady=1)
        s.__toiminnonPeruutaPainike=Button(s.__uusiToimintoIkkuna, text="Peruuta", command=lambda: s.__uusiToimintoIkkuna.destroy())
        s.__toiminnonPeruutaPainike.grid(row=5, column=2, sticky=W, padx=2)
    def UusiToimintoSQL(s, toiminto, kuvaus, koodi):
        """
        Siirtää saamansa tiedot SQL moduulille käsiteltäväksi ja tallennettavaksi tietokantaan.
        kutsuu PäivitäOrja funktion ja sulkee UusiToiminto ikkunan
        """
        SQL.uusiToiminto(toiminto,kuvaus,koodi)
        s.PaivitaOrja()
        s.__uusiToimintoIkkuna.destroy()
        
    def PoistaToiminto(s):
        """
        PoistaToiminto funktio joka ottaa aktiivisen listbox objektin ja siirtää tiedon SQL moduulille käsiteltäväksi
        Tyhjentää kuvaus ja koodi ruudun
        """
        toiminto=s.__paaIkkunaLista.get(s.__paaIkkunaLista.curselection())
        s.__paaIkkunaKoodi.delete('1.0', END)
        s.__paaIkkunaOrjaKuvaus.delete('1.0', END)
        SQL.poistaToiminto(toiminto)
        s.PaivitaOrja()

    def TallennaMuokattuKoodi(s):
        """
        TallennaMuokattuKoodi funktio joka kerää aktiivisen listbox objektin, koodin, kuvauksen ja siirtää tiedon 
        SQL moduulille käsiteltäväksi.
        """
        toiminto=s.__paaIkkunaLista.get(s.__paaIkkunaLista.curselection())
        kuvaus=s.__paaIkkunaOrjaKuvaus.get("0.0", END)
        koodi=s.__paaIkkunaKoodi.get("0.0", END)
        SQL.tallennaKoodi(koodi, kuvaus, toiminto)
        s.__paaIkkunaOrjaKuvaus.config(state=DISABLED)
        s.__paaIkkunaKoodi.config(state=DISABLED)
        s.__paaIkkunaOrjaKuvaus.config(state=DISABLED, bg="grey95")
        s.__paaIkkunaKoodi.config(state=DISABLED, bg="grey95")
        s.__paaikkunaOikeaTallenna.config(state=DISABLED)
        s.__paaIkkunaOikeaMuokkaa.configure(text="Päälle")
        s.__muokkaustila = 0
    
    def lisaaNao(s):
        """
        lisaaNao funktio joka avaa uuden ikkunan, johon käyttäjä syöttää tiedot.
        Tallenna painikkeella tiedot kerätään kentistä ja lähetetään UusiToimintoSQL funktiolle.
        Peruuta painike sulkee ohjelman
        """
        s.__LisaaNaoIkkuna=Toplevel()
        s.__LisaaNaoIkkuna.attributes("-topmost", True)
        s.__LisaaNaoIkkuna.title("Lisää robotti")
        s.__LisaaNaoIkkuna.resizable(0,0)
        s.__LisaaNaoNimiLab=Label(s.__LisaaNaoIkkuna, text="Robotin nimi:", width=15).grid(row=2, column=0, sticky=E)
        s.__LisaaNaoKuvausLab=Label(s.__LisaaNaoIkkuna, text="Robotin kuvaus:", width=15).grid(row=3, column=0, sticky=E)
        s.__LisaaNaoIpLab=Label(s.__LisaaNaoIkkuna, text="Robotin IP:", width=15).grid(row=4, column=0, sticky=E)
        s.__LisaaNaoPortLab=Label(s.__LisaaNaoIkkuna, text="Portti", width=15).grid(row=5, column=0, sticky=E)
        #Entrykentät
        s.__LisaaNaoNimiEnt=Entry(s.__LisaaNaoIkkuna)
        s.__LisaaNaoNimiEnt.grid(row=2, column=1, columnspan=2, sticky=W+E)
        s.__LisaaNaoKuvausEnt=Text(s.__LisaaNaoIkkuna, width=30, height=3, wrap=WORD)
        s.__LisaaNaoKuvausEnt.grid(row=3, column=1, columnspan=2, sticky=W+E)
        s.__LisaaNaoIpEnt=Entry(s.__LisaaNaoIkkuna, width=30)
        s.__LisaaNaoIpEnt.grid(row=4, column=1, columnspan=2, sticky=W+E)
        s.__LisaaNaoPortEnt=Entry(s.__LisaaNaoIkkuna, width=30)
        s.__LisaaNaoPortEnt.grid(row=5, column=1, columnspan=2, sticky=W+E)
        s.__toiminnonTallennaPainike=Button(s.__LisaaNaoIkkuna, text="Tallenna", command=lambda: s.tallennaNao(
                        nimi=s.__LisaaNaoNimiEnt.get(),
                        kuvaus=s.__LisaaNaoKuvausEnt.get("0.0", END),
                        ip=s.__LisaaNaoIpEnt.get(),
                        portti=s.__LisaaNaoPortEnt.get()))
        s.__toiminnonTallennaPainike.grid(row=6, column=1, sticky=E, pady=1)
        s.__toiminnonPeruutaPainike=Button(s.__LisaaNaoIkkuna, text="Peruuta", command=lambda: s.__LisaaNaoIkkuna.destroy())
        s.__toiminnonPeruutaPainike.grid(row=6, column=2, sticky=W, padx=2)
    def tallennaNao(s, nimi, kuvaus, ip, portti):
        """
        Siirtää saamansa tiedot SQL moduulille käsiteltäväksi ja tallennettavaksi tietokantaan.
        kutsuu PäivitäNao funktion ja sulkee LisaaNao ikkunan
        """
        SQL.tallennaRobotti(nimi, kuvaus, ip, portti)
        s.__LisaaNaoIkkuna.destroy()
        s.PaivitaNao()

    def valitseNao(s):
        """
        ValitseNao funktio joka avaa uuden ikkunan, jossa käyttäjä voi valita listalta ennakkoon tallennetun tiedon.
        Tallenna painikkeella tiedot kerätään kentistä ja lähetetään UusiToimintoSQL funktiolle.
        Valitse painikkeella tiedot kerätään kentistä ja lähetetään ValitseNaoListalta funktiolle.
        Poista painike kutsuu PoistaNao funktion
        Peruuta painike sulkee ohjelman
        """
        s.__ValitseNaoIkkuna=Toplevel()
        s.__ValitseNaoIkkuna.attributes("-topmost", True)
        s.__ValitseNaoIkkuna.title("Valitse robotti")
        s.__ValitseNaoIkkuna.resizable(0,0)
        s.__ValitseNaoLisaa=Button(s.__ValitseNaoIkkuna, text="Lisää Robotti", command=lambda: s.lisaaNao()).grid(row=0, column=0, sticky=E+W)
        s.__ValitseNaoLista=Listbox(s.__ValitseNaoIkkuna, height=6)
        s.__ValitseNaoLista.config(exportselection=False)
        s.__ValitseNaoLista.bind("<<ListboxSelect>>", s.NaoListboxValinta)
        s.__ValitseNaoLista.grid(row=2, column=0, rowspan=4, sticky=E+W+S+N, pady=1, padx=1)
        for robotti in sorted(SQL.robottiTiedot):
            s.__ValitseNaoLista.insert('end', robotti)
        s.__valitseNaoNimiLab=Label(s.__ValitseNaoIkkuna, text="Robotin nimi:", width=15).grid(row=2, column=1, sticky=E)
        s.__valitseNaoKuvausLab=Label(s.__ValitseNaoIkkuna, text="Robotin kuvaus:", width=15).grid(row=3, column=1, sticky=E)
        s.__valitseNaoIpLab=Label(s.__ValitseNaoIkkuna, text="Robotin IP:", width=15).grid(row=4, column=1, sticky=E)
        s.__valitseNaoPortLab=Label(s.__ValitseNaoIkkuna, text="Portti", width=15).grid(row=5, column=1, sticky=E)
        #Entrykentät
        s.__valitseNaoNimiEnt=Entry(s.__ValitseNaoIkkuna)
        s.__valitseNaoNimiEnt.grid(row=2, column=2, columnspan=3, sticky=W+E, padx=1)
        s.__valitseNaoKuvausEnt=Text(s.__ValitseNaoIkkuna, width=30, height=3, wrap=WORD)
        s.__valitseNaoKuvausEnt.grid(row=3, column=2, columnspan=3, sticky=W+E, padx=1)
        s.__valitseNaoIpEnt=Entry(s.__ValitseNaoIkkuna, width=30)
        s.__valitseNaoIpEnt.grid(row=4, column=2, columnspan=3, sticky=W+E, padx=1)
        s.__valitseNaoPortEnt=Entry(s.__ValitseNaoIkkuna, width=30)
        s.__valitseNaoPortEnt.grid(row=5, column=2, columnspan=3, sticky=W+E, padx=1)
        s.__ValitseNaoPoistaPainike=Button(s.__ValitseNaoIkkuna, text="Poista", command=lambda: s.PoistaNao())
        s.__ValitseNaoPoistaPainike.grid(row=6, column=0, sticky=W+E)
        s.__ValitseNaoValitsePainike=Button(s.__ValitseNaoIkkuna, text="Valitse", command=lambda: s.ValitseNaoListalta(
                        nimi=s.__valitseNaoNimiEnt.get(),
                        ip=s.__valitseNaoIpEnt.get(),
                        portti=s.__valitseNaoPortEnt.get()))
        s.__ValitseNaoValitsePainike.grid(row=6, column=2, sticky=W+E)
        s.__ValitseNaoTallennaPainike=Button(s.__ValitseNaoIkkuna, text="Tallenna", command=lambda: SQL.paivitaRobotti(
                        nimi=s.__valitseNaoNimiEnt.get(),
                        kuvaus=s.__valitseNaoKuvausEnt.get("0.0", END),
                        ip=s.__valitseNaoIpEnt.get(),
                        portti=s.__valitseNaoPortEnt.get()))
        s.__ValitseNaoTallennaPainike.grid(row=6, column=3, sticky=W+E, pady=1)
        s.__ValitseNaoPeruutaPainike=Button(s.__ValitseNaoIkkuna, text="Peruuta", command=lambda: s.__ValitseNaoIkkuna.destroy())
        s.__ValitseNaoPeruutaPainike.grid(row=6, column=4, sticky=W+E, padx=2)
        s.PaivitaNao()
    def PoistaNao(s):
        """
        PoistaNao funktio joka valitsee aktiivisen objektin siirtää saamansa tiedon SQL moduulille käsiteltäväksi
        """
        value=s.__valitseNaoNimiEnt.get()
        SQL.poistaRobotti(value)
        s.PaivitaNao()

    def PaivitaNao(s):
        """
        PäivitäNao funktio joka tyhjentää ValitseNao ruudun kaikki tiedot ja tuo sen hetkiset tiedot palvelimelta,
        sekä asettaa saamansa tiedot paikoilleen ValitseNao ruutuun
        """
        try:
            s.__valitseNaoNimiEnt.config(state=NORMAL)
            s.__valitseNaoKuvausEnt.config(state=NORMAL)
            s.__valitseNaoKuvausEnt.config(bg="white")
            s.__valitseNaoIpEnt.config(state=NORMAL)
            s.__valitseNaoPortEnt.config(state=NORMAL)
            s.__ValitseNaoValitsePainike.config(state=NORMAL)
            s.__ValitseNaoTallennaPainike.config(state=NORMAL)
        except TclError:
            pass
        s.__ValitseNaoLista.delete(0, END)
        SQL.robottiLaajuus.clear()
        SQL.robottiTiedot.clear()
        SQL.tuoRobotit()
        s.__valitseNaoNimiEnt.delete(0, END)
        s.__valitseNaoKuvausEnt.delete('1.0', END)
        s.__valitseNaoIpEnt.delete(0, END)
        s.__valitseNaoPortEnt.delete(0, END)
        for robotti in SQL.robottiTiedot:
            s.__ValitseNaoLista.insert('end', robotti)
        try:
            s.__valitseNaoNimiEnt.config(state=DISABLED)
            s.__valitseNaoKuvausEnt.config(state=DISABLED)
            s.__valitseNaoKuvausEnt.config(bg="grey94")
            s.__valitseNaoIpEnt.config(state=DISABLED)
            s.__valitseNaoPortEnt.config(state=DISABLED)
            s.__ValitseNaoValitsePainike.config(state=DISABLED)
            s.__ValitseNaoTallennaPainike.config(state=DISABLED)
        except TclError:
            pass

    def NaoListboxValinta(s, event):
        """
        Listbox funktio joka kutsuttaessa valitsee listan objektin ja hakee sen mukaan
        SQL tietokannasta toiminnon kuvauksen ja koodin, sekä asettaa ne omille paikoilleen. 
        """
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection)
        try:
            s.__valitseNaoNimiEnt.config(state=NORMAL)
            s.__valitseNaoKuvausEnt.config(state=NORMAL)
            s.__valitseNaoKuvausEnt.config(bg="White")
            s.__valitseNaoIpEnt.config(state=NORMAL)
            s.__valitseNaoPortEnt.config(state=NORMAL)
            s.__ValitseNaoValitsePainike.config(state=NORMAL)
            s.__ValitseNaoTallennaPainike.config(state=NORMAL)
        except TclError:
            pass
        s.__valitseNaoNimiEnt.delete(0, END)
        s.__valitseNaoNimiEnt.insert(0, value)
        s.__valitseNaoKuvausEnt.delete('1.0', END)
        s.__valitseNaoKuvausEnt.insert('1.0', SQL.tuoRobottiKuvaus(value[-1]))
        s.__valitseNaoIpEnt.delete(0, END)
        s.__valitseNaoIpEnt.insert(0, SQL.tuoRobottiIp(value[-1]))
        s.__valitseNaoPortEnt.delete(0, END)
        s.__valitseNaoPortEnt.insert(0, SQL.tuoRobottiPortti(value[-1]))

    def ValitseNaoListalta(s, nimi, ip, portti):
        """
        Saa tiedot valitseNao funktiolta ja tietojen perusteella configuroi pääikkunan objekteja.
        """
        s.__alapalkkiYhdistetty.configure(text="(C)", fg="yellow")
        NAO.RobottiNimi=nimi
        NAO.RobottiIP=ip
        NAO.RobottiPort=portti
        s.__alapalkkiRobotti.config(text=NAO.RobottiNimi)
        s.__alapalkkiRobottiIP.config(text=NAO.RobottiIP)
        s.__alapalkkiRobottiPort.config(text=NAO.RobottiPort)
        if s.__yhdistetty == 0:
            s.Connect()
        else:
            s.Yhdistetty()
        NAO.tallennaRobotti()
        s.__ValitseNaoIkkuna.destroy()

    def Yhdista(s):
        """
        Yhdistä funktio avaa uuden ikkunan jossa käyttäjä saa yhdistettyä ohjelman palvelimeen, palvelimen tiedot 
        """
        s.__YhdistaIkkuna=Toplevel()
        s.__YhdistaIkkuna.attributes("-topmost", True)
        s.__YhdistaIkkuna.title("Yhdistä")
        s.__YhdistaIkkuna.resizable(0,0)
        s.__YhdistaHostLab=Label(s.__YhdistaIkkuna, text="HOST:", width=15).grid(row=2, column=0, sticky=E)
        s.__YhdistaPortLab=Label(s.__YhdistaIkkuna, text="PORT:", width=15).grid(row=3, column=0, sticky=E)
        s.__YhdistaUserLab=Label(s.__YhdistaIkkuna, text="USER:", width=15).grid(row=4, column=0, sticky=E)
        s.__YhdistaPasswordLab=Label(s.__YhdistaIkkuna, text="PASSWORD", width=15).grid(row=5, column=0, sticky=E)
        s.__YhdistaDatabaseLab=Label(s.__YhdistaIkkuna, text="Database", width=15).grid(row=6, column=0, sticky=E)
        #Entrykentät
        s.__YhdistaHostEnt=Entry(s.__YhdistaIkkuna)
        s.__YhdistaHostEnt.grid(row=2, column=1, columnspan=2, sticky=W+E)
        s.__YhdistaPortEnt=Entry(s.__YhdistaIkkuna, width=30)
        s.__YhdistaPortEnt.grid(row=3, column=1, columnspan=2, sticky=W+E)
        s.__YhdistaUserEnt=Entry(s.__YhdistaIkkuna, width=30)
        s.__YhdistaUserEnt.grid(row=4, column=1, columnspan=2, sticky=W+E)
        s.__YhdistaPasswordEnt=Entry(s.__YhdistaIkkuna, width=30)
        s.__YhdistaPasswordEnt.grid(row=5, column=1, columnspan=2, sticky=W+E)
        s.__YhdistaDatabaseEnt=Entry(s.__YhdistaIkkuna, width=30)
        s.__YhdistaDatabaseEnt.grid(row=6, column=1, columnspan=2, sticky=W+E)
        s.__toiminnonDefaultPainike=Button(s.__YhdistaIkkuna, text="Default", command=lambda: s.DefaultPalvelin())
        s.__toiminnonDefaultPainike.grid(row=7, column=0)
        s.__toiminnonTallennaPainike=Button(s.__YhdistaIkkuna, text="Tallenna", command=lambda: s.YhdistaKomento(
                HOST=s.__YhdistaHostEnt.get(),
                PORT=s.__YhdistaPortEnt.get(),
                USER=s.__YhdistaUserEnt.get(),
                PASSWORD=s.__YhdistaPasswordEnt.get(),
                DATABASE=s.__YhdistaDatabaseEnt.get()))
        s.__toiminnonTallennaPainike.grid(row=7, column=2, sticky=W+E, pady=1)
        s.__toiminnonPeruutaPainike=Button(s.__YhdistaIkkuna, text="Peruuta", command=lambda: s.__YhdistaIkkuna.destroy())
        s.__toiminnonPeruutaPainike.grid(row=7, column=3, sticky=W+E, padx=2)
        s.TuoPalvelinTiedot()

    def DefaultPalvelin(s):
        s.__YhdistaHostEnt.delete(0, END)
        s.__YhdistaPortEnt.delete(0, END)
        s.__YhdistaUserEnt.delete(0, END)
        s.__YhdistaPasswordEnt.delete(0, END)
        s.__YhdistaDatabaseEnt.delete(0, END)
        SQL.defaultPalvelin()
        s.TuoPalvelinTiedot()

    def TuoPalvelinTiedot(s):
        #Tuodaan palvelimen tiedot entry kenttään
        s.__YhdistaHostEnt.insert(INSERT, SQL.HOST)
        s.__YhdistaPortEnt.insert(INSERT, SQL.PORT)
        s.__YhdistaUserEnt.insert(INSERT, SQL.USER)
        s.__YhdistaPasswordEnt.insert(INSERT, SQL.PASSWORD)
        s.__YhdistaDatabaseEnt.insert(INSERT, SQL.DB)

    def YhdistaKomento(s,HOST,PORT,USER,PASSWORD,DATABASE):
        SQL.HOST=HOST
        SQL.PORT=int(PORT)
        SQL.USER=USER
        SQL.PASSWORD=PASSWORD
        SQL.DB=DATABASE
        SQL.tallennaPalvelin()
        SQL.testaaPalvelin()
        s.__YhdistaIkkuna.destroy()
 
def ViimeisinRobotti():
    try:
        robotti=open("RobottiAsetukset.txt", "r")
        rivit=robotti.readlines()
        NAO.RobottiNimi = rivit[0][:-1]
        NAO.RobottiIP = rivit[1][:-1]
        NAO.RobottiPort = int(rivit[2][:-1])
        robotti.close()
    except:
        print("VIRHE TUO VIIMEISIN ROBOTTI")

def main():
    SQL.tuoTietokanta()
    SQL.tuoRobotit()
    SQL.tuoViimeisinPalvelin()
    ViimeisinRobotti()

    Gui()
main()