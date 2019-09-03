import sqlite3
import logging
from uuid import uuid4  


def create_connection():
    try:
        conn = sqlite3.connect('baza.db')
        return conn
    except:
        return None

def close_connection(conn):
    conn.close()


def provjera_vrijednosti(email):
    conn = create_connection() konekciju u varijablu 'conn'
    c = conn.cursor()
    c.execute("SELECT id FROM korisnici WHERE email = ?", (email, ))
    e = c.fetchone()
    close_connection(conn)
    if e == None:
        return True
    else:
        return False

def novi_korisnik(ime, prezime, email, lozinka, grad_studiranja, sveuciliste, smjer):
    try:
        conn = create_connection()
        c = conn.cursor()
        korisnik_id = uuid4().hex
        v = provjera_vrijednosti(email)
        if v:
            c.execute("INSERT INTO korisnici VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(korisnik_id, ime, prezime, lozinka, email, grad_studiranja, sveuciliste, smjer))
            conn.commit() 
            odgovor = korisnik_id
        else:
            odgovor = 0
        close_connection(conn)
        return odgovor
    except Exception as e:
        logging.exception("Nije moguce spremiti novog korisnika.")

def prijava(email, lozinka):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM korisnici WHERE email = ?", (email,))
        k = c.fetchone()
        close_connection(conn)
        if (k[3] == lozinka):
            return k
        else:
            return odgovor
    except Exception as e:
        logging.exception("Krivi email ili lozinka")

def prijava_admin(ime, lozinka):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE korisnicko_ime = ?", (ime,))
        a = c.fetchone()
        close_connection(conn)
        if (a[2] == lozinka):
            return a
        else:
            return 0
    except Exception as e:
        logging.exception("Krivo ime ili lozinka")

def uredi_korisnika(id, ime, prezime, email, lozinka, grad_studiranja, sveuciliste, smjer):
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute("UPDATE korisnici SET ime = ?, prezime = ?, lozinka = ?, email = ?, grad_studiranja = ?, sveuciliste = ?, smjer = ? WHERE id = ?",(ime, prezime, lozinka, email, grad_studiranja, sveuciliste, smjer, id))
        conn.commit()
        odgovor = True
        close_connection(conn)
        return odgovor
    except Exception as e:
        logging.exception("Nije moguce napraviti promjene za odabranog korisnika.")

def spremi_skriptu(id_korisnik, naziv, ocjena, dokument, datum_spremanja):
    try:
        conn = create_connection()
        c = conn.cursor()
        id_skripta = uuid4().hex
        c.execute("INSERT INTO skripte VALUES (?, ?, ?, ?, ?, ?)",(id_skripta, id_korisnik, naziv, ocjena, dokument, datum_spremanja))
        conn.commit()
        close_connection(conn)
        odgovor = id_skripta
        return odgovor
    except Exception as e:
        logging.exception("Dogodila se greska kod spremanja skripte")

def dohvati_skripte():
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM skripte")
            r = c.fetchall()
            close_connection(conn)
            return r
        except Exception as e:
            logging.exception("Greska u citanju skripti")
            
def obrisi_skriptu(id_skripta):
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("DELETE FROM skripte WHERE id = ?", (id_skripta,))
            conn.commit()
            c.execute("SELECT * FROM skripte")
            r = c.fetchall()
            close_connection(conn)
            return r
        except Exception as e:
            logging.exception("Greska u brisanju skripte")

def azurirajOcijene(id_skripta, ocijena):
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("UPDATE skripte SET ocjena = ? WHERE id = ?", (ocijena, id_skripta))
            conn.commit()
            c.execute("SELECT * FROM skripte")
            r = c.fetchall()
            close_connection(conn)
            return r
        except Exception as e:
            logging.exception("Greska u azuriranju ocjene")

def dohvati_obavijesti():
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM obavijesti")
            o = c.fetchall()
            close_connection(conn)
            return o
        except Exception as e:
            logging.exception("Greska u citanju obavijesti")

def spremi_obavjest(naslov, tekst, datum_objave):
        try:
            conn = create_connection()
            c = conn.cursor()
            id_obavjest = uuid4().hex
            c.execute("INSERT INTO obavijesti VALUES (?, ?, ?, ?)",(id_obavjest, naslov, tekst, datum_objave))
            conn.commit()
            close_connection(conn)
            odgovor = id_obavjest
            return odgovor
        except Exception as e:
            logging.exception("Dogodila se greska kod spremanja obavjesti")

def azuriraj_obavjest(id_obavjest, naslov, tekst):
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute("UPDATE obavijesti SET naslov = ?, tekst = ? WHERE id = ?", (naslov, tekst, id_obavjest))
            conn.commit()
            c.execute("SELECT * FROM skripte")
            r = c.fetchall()
            close_connection(conn)
            return r
        except Exception as e:
            logging.exception("Greska u azuriranju ocjene")
