# -*- coding:utf-8 -*-

"""
Palvelimen tiedot
"""
HOST = "127.0.0.1"
PORT = 3306
USER = "root"
PASSWORD = ""
DB = "nao_tietokanta"

tietokantaLaajuus = []
tietokantaToimintoTiedot = []

robottiLaajuus = []
robottiTiedot = []

import pymysql
from pymysql import IntegrityError, InternalError
from tkinter import messagebox


"""
Testataan yhteys palvelimeen
"""
try:
	yhteys = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
	cursor = yhteys.cursor()
except ConnectionError:
    messagebox.showerror("VIRHE!","Yhteys virhe. \nTietokantaan ei saatu yhteyytä")

def tuoTietokanta():
    try:
        cursor.execute("SELECT nro FROM nao_tiedot")
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            else:
                row=row[-1]
                tietokantaLaajuus.append(row)
        index = 0
        for i in range(len(tietokantaLaajuus)):
            tuoTieto(index)
            index = index+1
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoTietokanta")

def tuoTieto(index):
    sql = ("SELECT toiminto FROM nao_tiedot WHERE nro = {0}").format(tietokantaLaajuus[index])
    try:
        cursor.execute(sql)
        tieto = cursor.fetchone()
        tieto = tieto[-1]
        tietokantaToimintoTiedot.append(tieto)
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoTieto")

def tuoToiminto(value):
    sql = ("SELECT kuvaus FROM nao_tiedot WHERE toiminto = '{0}'").format(value)
    try:
        cursor.execute(sql)
        kuvaus = cursor.fetchone()
        kuvaus = kuvaus[-1]
        return kuvaus
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoToiminto")

def tuoKoodi(value):
    sql = ("SELECT koodi FROM nao_tiedot WHERE toiminto = '{0}'").format(value)
    try:
        cursor.execute(sql)
        koodi = cursor.fetchone()
        koodi = koodi[-1]
        koodi = str.replace(koodi, "HEITTOMERKKI", "'")
        return koodi
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoKoodi")

def uusiToiminto(toiminto, kuvaus, koodi):
    if len(toiminto) > 0:
        koodi = str.replace(koodi, "'", "HEITTOMERKKI")
        sql = ("INSERT INTO nao_tiedot(toiminto, kuvaus, koodi) VALUES('{0}','{1}','{2}')").format(toiminto,kuvaus,koodi)
        try:
            cursor.execute(sql)
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:uusiToiminto")
    else:
        messagebox.showerror("VIRHE","Nimi on pakollinen")

def poistaToiminto(toiminto):
    vastaus=messagebox.askquestion("Poista Toiminto", "Oletko varma?\n Tätä toimintoa ei voi peruuttaa")
    if vastaus == 'yes':
        sql = ("DELETE FROM nao_tiedot WHERE toiminto = '{0}'").format(toiminto)
        try:
            cursor.execute(sql)
            messagebox.showinfo("Onnistui", "Tapahtuma suoritettu onnistuneesti")
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:PoistaToiminto")
    else:
        pass
        
def tallennaKoodi(koodi, kuvaus, toiminto):
    vastaus=messagebox.askquestion("Poista Toiminto", "Oletko varma?\n Tätä toimintoa ei voi peruuttaa")
    if vastaus == 'yes':
        koodi = str.replace(koodi, "'", "HEITTOMERKKI")
        sql = ("UPDATE nao_tiedot SET koodi = '{0}', kuvaus = '{1}' WHERE toiminto= '{2}'").format(koodi, kuvaus, toiminto)
        print(sql)
        try:
            cursor.execute(sql)
            messagebox.showinfo("Onnistui", "Koodin tallennus suoritettu onnistuneesti")
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tallennaKoodi")
    else:
        pass

def tuoRobotit():
    try:
        cursor.execute("SELECT nro FROM nao_robotti")
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            else:
                row=row[-1]
                robottiLaajuus.append(row)
        index = 0
        for i in range(len(robottiLaajuus)):
            tuoRobotti(index)
            index = index+1
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoRobotit")

def tuoRobotti(index):
    sql = ("SELECT nimi FROM nao_robotti WHERE nro = {0}").format(robottiLaajuus[index])
    try:
        cursor.execute(sql)
        tieto = cursor.fetchone()
        tieto = tieto
        robottiTiedot.append(tieto)
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoTieto")

def tallennaRobotti(nimi, kuvaus, ip, portti):
    if len(nimi) > 0 and len(ip) > 0 and len(portti) > 0:
        sql = ("INSERT INTO nao_robotti (nimi, kuvaus, ip, port) VALUES ('{0}', '{1}', '{2}', '{3}')").format(nimi, kuvaus, ip, portti)
        try:
            cursor.execute(sql)
            messagebox.showinfo("ONNISTUI", "Uusi Robotti tallennettu onnistuneesti")
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tallennaRobotti")
    else:
        messagebox.showerror("VIRHE","Tarkista nimi, ip ja portti")

def tuoRobottiKuvaus(value):
    sql = ("SELECT kuvaus FROM nao_robotti WHERE nimi = '{0}'").format(value)
    try:
        cursor.execute(sql)
        kuvaus = cursor.fetchone()
        kuvaus = kuvaus[-1]
        return kuvaus
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoRobottiKuvaus")

def tuoRobottiIp(value):
    sql = ("SELECT ip FROM nao_robotti WHERE nimi = '{0}'").format(value)
    try:
        cursor.execute(sql)
        ip = cursor.fetchone()
        ip = ip[-1]
        return ip
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoRobottiIp")

def tuoRobottiPortti(value):
    sql = ("SELECT port FROM nao_robotti WHERE nimi = '{0}'").format(value)
    try:
        cursor.execute(sql)
        portti = cursor.fetchone()
        portti = portti[-1]
        return portti
    except:
        yhteys.rollback()
        messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:tuoRobottiPortti")

def poistaRobotti(value):
    vastaus=messagebox.askquestion("Poista robotti", "Oletko varma?\n Tätä toimintoa ei voi peruuttaa")
    if vastaus == 'yes':
        sql = ("DELETE FROM nao_robotti WHERE nimi = '{0}'").format(value)
        try:
            cursor.execute(sql)
            messagebox.showinfo("Onnistui", "Tapahtuma suoritettu onnistuneesti")
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:PoistaToiminto")
    else:
        pass

def paivitaRobotti(nimi, kuvaus, ip, portti):
    vastaus=messagebox.askquestion("Päivitä robotin tiedot", "Oletko varma?\n Tätä toimintoa ei voi peruuttaa")
    if vastaus == 'yes':
        sql = ("UPDATE nao_robotti SET kuvaus = '{1}', ip = '{2}', port = '{3}' WHERE nimi = '{0}'").format(nimi, kuvaus, ip, portti)
        try:
            cursor.execute(sql)
            messagebox.showinfo("Onnistui", "Koodin tallennus suoritettu onnistuneesti")
        except:
            yhteys.rollback()
            messagebox.showerror("YHTEYS VIRHE", "YHTEYSVIRHE\nkoodi:paivitaRobotti")
    else:
        pass

