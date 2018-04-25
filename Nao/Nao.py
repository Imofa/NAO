import sys
import time
import builtins
#sys.path.append('..') #Kansiossa olevan modulin importtaamista varten
from tkinter import *
from tkinter import messagebox
from tkinter import TclError

import NAO_toiminnot as NAO #Tuodaan NAO_toiminnot moduuli
import SQL_toiminnot as SQL #Tuodaan SQL_toiminnot moduuli

Robotit=["Robotti_01", "Robotti_02", "Robotti_03", "Robotti_04"]

class Gui():
    def __init__(s):
        s.__muokkaustila = 0
        s.__root = Tk()
        s.__root.resizable(0,0)
        s.__root.title("NAO tietokanta\t by:Roope Romu")
        """
        Ohjleman valikkopalkki
        """
        s.__valikkoPalkki=Menu(s.__root, relief=RAISED)
        #s.__valikkoPalkki.config(background="lightgrey", activebackground="lightgrey")
        s.__valikkoFile=Menu(s.__valikkoPalkki, tearoff=0,)
        s.__valikkoPalkki.add_cascade(label="File", menu=s.__valikkoFile)
        s.__valikkoRobotti=Menu(s.__valikkoPalkki, tearoff=0)
        s.__valikkoPalkki.add_cascade(label="NAO", menu=s.__valikkoRobotti)
        s.__valikkoHelp=Menu(s.__valikkoPalkki, tearoff=0)
        s.__valikkoPalkki.add_cascade(label="Help", menu=s.__valikkoHelp)
        #valikkoFile objektit
        s.__valikkoFile.add_command(label="Päivitä", command=lambda: s.PaivitaOrja())
        s.__valikkoFile.add_command(label="Yhdistä", state=DISABLED, command=lambda: print())
        s.__valikkoFile.add_separator()
        s.__valikkoFile.add_command(label="Lopeta", command=lambda: s.__root.destroy())
        #valikkoHelp objektit
        s.__valikkoHelp.add_command(label="Toiminnot", command=lambda: print())
        s.__valikkoHelp.add_command(label="Tietoja", command=lambda: print())
        #valikkoRobotti objektit
        s.__valikkoRobotti.add_command(label="Valitse NAO", command=lambda: s.ValitseNao())
        s.__valikkoRobotti.add_command(label="Yhdistä NAO")

        """
        Ohjelman pää ikkuna jossa kaikki taika tapahtuu
        """
        s.__paaIkkuna=Frame(s.__root).grid(row=0, column=0, sticky='nsew')
        s.__paaIkkunaVasenSelite=Label(s.__paaIkkuna, text="", relief=GROOVE).grid(row=0, column=0, sticky='nsew')
        s.__paaIkkunaOikeaSelite=Label(s.__paaIkkuna, text="Käsiteltävä koodi", relief=GROOVE).grid(row=0, column=1, sticky='nsew')
       
        #"""
        #Popup ikkuna ohjelman eri toiminnoille
        #"""
        #s.popUpIkkuna = Menu(s.__root, tearoff=0)
        #s.popUpIkkuna.add_command(label="Print object", )
        #s.popUpIkkuna.add_command(label="Unlock")
        #s.popUpIkkuna.add_command(label="Modify")

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
        s.__paaIkkunaLista=Listbox(s.__paaIkkunaVasen, width=30, height=30)
        s.__paaIkkunaLista.config(exportselection=False)
        s.__paaIkkunaLista.bind("<<ListboxSelect>>", s.ListboxValinta)
        #s.__paaIkkunaLista.bind("<Button-3>", s.popup)
        s.__paaIkkunaLista.grid(row=2, column=0, sticky=E+W, pady=1, padx=1)

        #s.__paaIkkunaLista.bind('<<ListboxSelect>>', s.ValittuToiminto)
        for toiminto in SQL.tietokantaToimintoTiedot:
            s.__paaIkkunaLista.insert('end', toiminto)

        #paaIkkunaText ruudun oikeanpuolinen ruutu.
        s.__paaIkkunaOikea=Frame(s.__paaIkkuna)
        s.__paaIkkunaOikea.grid(row=1, column=1)
        s.__paaikkunaOikeaTallenna=Button(s.__paaIkkunaOikea, text="Tallenna kuvaus/koodi", state=DISABLED, command=lambda: s.TallennaMuokattuKoodi()) #Tallentaa koodin tietokantaan
        s.__paaikkunaOikeaTallenna.grid(row=0, column=1, sticky=E+W)
        s.__paaikkunaOikeaMuokkaustila=Label(s.__paaIkkunaOikea, text="Muokkaustila:").grid(row=0, column=2, sticky=E)
        s.__paaIkkunaOikeaMuokkaa=Button(s.__paaIkkunaOikea, text="Päällä", command=lambda: s.Muokkaa(), width=8) #Mahdollista muokkaus texti kenttiin
        s.__paaIkkunaOikeaMuokkaa.grid(row=0, column=3, sticky=W)
        s.__paaIkkunaKoodi=Text(s.__paaIkkunaOikea, width=80, height=50, wrap=WORD, state=DISABLED, bg="grey95")
        s.__paaIkkunaKoodi.grid(row=1, column=0, rowspan=2, columnspan=4, pady=1, padx=1)
        s.__scrollbar=Scrollbar(s.__paaIkkunaOikea, command=s.__paaIkkunaKoodi.yview)
        s.__scrollbar.grid(row=1, column=5, rowspan=2, sticky='ns')
        s.__paaIkkunaKoodi['yscrollcommand'] = s.__scrollbar.set
        s.__paaIkkunaOikeaSuorita=Button(s.__paaIkkunaOikea, text="Suorita")      #Suorittaa koodin robotilla
        s.__paaIkkunaOikeaSuorita.grid(row=4, column=2, sticky=E)     
        s.__paaIkkunaOikeaLaheta=Button(s.__paaIkkunaOikea, text="Laheta")        #Lähettää koodin robotin muistiin
        s.__paaIkkunaOikeaLaheta.grid(row=4, column=3, sticky=W)

        """
        Ohjelman alapalkki, Palkissa on kello/päivämäärä ja Naon yhteyden tilan osoitin
        """
        s.__alapalkki=Frame(s.__root, bd=1, relief=RAISED, background="lightgrey")
        s.__alapalkki.grid(row=10, columnspan=10, sticky=E+W, padx=1)
        s.__alapalkkiYhdistetty=Label(s.__alapalkki, text="", width=2, background="lightgrey", anchor=W)
        s.__alapalkkiYhdistetty.grid(row=0, column=0)
        s.__alapalkkiKello=Label(s.__alapalkki, text="", background="Lightgrey", anchor=E, width=90)
        s.__alapalkkiKello.grid(row=0, column=1)

        s.__root.config(menu=s.__valikkoPalkki)
        s.Kello()
        s.Yhdistetty()
        s.__root.mainloop()
        """
        Varmistetaan ohjelman sammuminen
        """
        try:
            s.__root.destroy()
        except:
            sys.exit()
            pass

    def Kello(s):       #Ohjelman kello, lyhyt funktio näyttämään aikaa, päivää ja päivämäärää
        now = time.strftime("%H:%M:%S\t%A %d/%m/%Y ")
        s.__alapalkkiKello.configure(text=now)
        s.__root.after(1000, s.Kello)
        return now
    def Yhdistetty(s):  #Ohjelman yhdistetty 
        X = NAO.testNaoYhteys()
        if X == "Y":
            s.__alapalkkiYhdistetty.configure(text="(Y)", fg="green")
            s.__paaIkkunaOikeaSuorita.configure(state=NORMAL)
            s.__paaIkkunaOikeaLaheta.configure(state=NORMAL)
            s.__root.after(5000, s.Yhdistetty)
        elif X == "N":
            s.__alapalkkiYhdistetty.configure(text="(N)", fg="red")
            s.__paaIkkunaOikeaSuorita.configure(state=DISABLED)
            s.__paaIkkunaOikeaLaheta.configure(state=DISABLED)
            s.__root.after(5000, s.Yhdistetty)
        else:
            s.__alapalkkiYhdistetty.configure(text="(C)", fg="yellow")
            s.__paaIkkunaOikeaSuorita.configure(state=DISABLED)
            s.__paaIkkunaOikeaLaheta.configure(state=DISABLED)
            s.__root.after(5000, s.Yhdistetty)

    def PaivitaOrja(s):
        s.__paaIkkunaLista.delete(0, END)
        SQL.tietokantaToimintoTiedot.clear()
        SQL.tietokantaLaajuus.clear()
        SQL.tuoTietokanta()
        for toiminto in SQL.tietokantaToimintoTiedot:
            s.__paaIkkunaLista.insert('end', toiminto)
        s.__paaIkkunaOrjaPoista.config(state=DISABLED)
        pass

    def ListboxValinta(s, event):
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
        s.__muokkaustila = 0


    def UusiToiminto(s):
        s.__uusiToimintoIkkuna=Toplevel()
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
        SQL.uusiToiminto(toiminto,kuvaus,koodi)
        s.PaivitaOrja()
        s.__uusiToimintoIkkuna.destroy()
        

    def PoistaToiminto(s):
        toiminto=s.__paaIkkunaLista.get(s.__paaIkkunaLista.curselection())
        SQL.poistaToiminto(toiminto)
        s.PaivitaOrja()

    def TallennaMuokattuKoodi(s):
        toiminto=s.__paaIkkunaLista.get(s.__paaIkkunaLista.curselection())
        kuvaus=s.__paaIkkunaOrjaKuvaus.get("0.0", END)
        koodi=s.__paaIkkunaKoodi.get("0.0", END)
        SQL.tallennaKoodi(koodi, kuvaus, toiminto)
        s.__paaIkkunaOrjaKuvaus.config(state=DISABLED)
        s.__paaIkkunaKoodi.config(state=DISABLED)

    def Muokkaa(s):
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
            s.__muokkaustila = 0
    
    def ValitseNao(s):
        s.__RobottiVar=StringVar()
        s.__RobottiVar.set(Robotit[0])

        s.__ValitseNaoIkkuna=Toplevel()
        s.__ValitseNaoIkkuna.title("Valitse Robotti")
        s.__valitseNaoListalta=Label(s.__ValitseNaoIkkuna, text="Valitse robotti", width=15).grid(row=0, column=0, sticky=E)
        s.__valitseNaoTai=Label(s.__ValitseNaoIkkuna, text="TAI LISÄÄ UUSI ROBOTTI").grid(row=1, column=0, columnspan=3)
        s.__valitseNaoNimiLab=Label(s.__ValitseNaoIkkuna, text="Robotin nimi:", width=15).grid(row=2, column=0, sticky=E)
        s.__valitseNaoKuvausLab=Label(s.__ValitseNaoIkkuna, text="Robotin kuvaus:", width=15).grid(row=3, column=0, sticky=E)
        s.__valitseNaoIpLab=Label(s.__ValitseNaoIkkuna, text="Robotin IP:", width=15).grid(row=4, column=0, sticky=E)
        s.__valitseNaoPortLab=Label(s.__ValitseNaoIkkuna, text="Portti", width=15).grid(row=5, column=0, sticky=E)
        #Dropdown listaus tallennetuista roboteista
        s.__RobottiLista=OptionMenu(s.__ValitseNaoIkkuna, s.__RobottiVar, *Robotit)
        s.__RobottiLista.config(width=30)
        s.__RobottiLista.grid(row=0, column=1, columnspan=2, sticky=W+E)
        #Entrykentät
        s.__valitseNaoNimiEnt=Entry(s.__ValitseNaoIkkuna)
        s.__valitseNaoNimiEnt.grid(row=2, column=1, columnspan=2, sticky=W+E)
        s.__valitseNaoKuvausEnt=Entry(s.__ValitseNaoIkkuna, width=30)
        s.__valitseNaoKuvausEnt.grid(row=3, column=1, columnspan=2, sticky=W+E)
        s.__valitseNaoIpEnt=Entry(s.__ValitseNaoIkkuna, width=30)
        s.__valitseNaoIpEnt.grid(row=4, column=1, columnspan=2, sticky=W+E)
        s.__valitseNaoPortEnt=Entry(s.__ValitseNaoIkkuna, width=30)
        s.__valitseNaoPortEnt.grid(row=5, column=1, columnspan=2, sticky=W+E)
        s.__toiminnonTallennaPainike=Button(s.__ValitseNaoIkkuna, text="Tallenna", command=lambda: print(
                        Nimi=s.__valitseNaoNimiEnt.get(),
                        kuvaus=s.__valitseNaoKuvausEnt.get(),
                        ip=s.__valitseNaoIpEnt.get(),
                        portti=s.__valitseNaoPortEnt()))
        s.__toiminnonTallennaPainike.grid(row=6, column=1, sticky=E, pady=1)
        s.__toiminnonPeruutaPainike=Button(s.__ValitseNaoIkkuna, text="Peruuta", command=lambda: s.__ValitseNaoIkkuna.destroy())
        s.__toiminnonPeruutaPainike.grid(row=6, column=2, sticky=W, padx=2)


    #def popup(s,event):
    #    widget = event.widget
    #    selection=widget.curselection()
    #    value = widget.get(selection)
    #    try:
    #        s.popUpIkkuna.post(event.x_root, event.y_root)
    #    finally:
    #        s.popUpIkkuna.grab_release()




def main():
    SQL.tuoTietokanta()
    Gui()
main()