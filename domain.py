import sqlite3              # IMPORTALI SQLITE BAZU
import logging              #IMPORTALI LOGGING
from uuid import uuid4      # IMPORTALI uuid da mozemo raditi hex string za id

#   S 'def' se oznacava funkcija i svaka zavrsava s ':'


#   Funkcija za spajanje s bazom. Pokusa napraviti konekciju preko sqlite3 biblioteke
#   'baza.db' se zove tvoja baza
def create_connection():
    try:
        conn = sqlite3.connect('baza.db') # Kako bi se uspjesno spoio put do baze mora biti pravi. Put se pise u zagradi
        return conn                         # Vraca konekciju kako bi mogli raditi operacije nad bazom
    except:
        return None                         # AKo ne uspije ne vraca nista

def close_connection(conn):             # Funkcija za zatvaranje konekcije
    conn.close()


##################################################################################
# Provjera postoje li vec navedene vrijednosti u bazi prije upisa novog objekta #
def provjera_vrijednosti(email):
    conn = create_connection()  # Pozivamo funkciju za otvarenje konekcije na bazu i spremamo konekciju u varijablu 'conn'
    c = conn.cursor()       # Instanciramo kursor u varijabli 'c' kako bi se mogli kretati po bazi, po recima i slicno
    c.execute("SELECT id FROM korisnici WHERE email = ?", (email, )) # S 'EXECUTE' se izvrsava naredba upita
    e = c.fetchone()    #   'fetchone' dohvaca prvu vrijednost i sprema u var 'e'
    close_connection(conn)
    if e == None:   #    Ako je 'e' prazan znaci da ne postoji vec takav email u bazi i moze se unijeti novi korisnik s tim mailom
        return True
    else:           #   Ako postoji onda vraca false i ne mozes unjeti taj emaill
        return False

#############################
# Operacije nad korisnikom #
def novi_korisnik(ime, prezime, email, lozinka, grad_studiranja, sveuciliste, smjer):
    try:
        conn = create_connection()
        c = conn.cursor()
        korisnik_id = uuid4().hex      # Pravimo id za korisnika pomocu uuid
        v = provjera_vrijednosti(email) # Provjeravamo jel postoji taj meil vec u bazi i odgovor spremamo u var 'v'
        if v:   # Ako je 'v' true, odnosno email ne postoji u bazi spremamo korisnika
            c.execute("INSERT INTO korisnici VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(korisnik_id, ime, prezime, lozinka, email, grad_studiranja, sveuciliste, smjer))
            conn.commit()   # S 'COMMIT' se spremaju sve promjene u bazi. Bez commita se nista ne save-a
                            # Upit je samo obican upit. Ako hoces spremiti nesto preko upita moras na kraju commitati
                            # A ako hoces dohvatiti nesto iz baze preko upita moras fetch-ati: fetchall, fetchone
            odgovor = korisnik_id
        else:
            odgovor = 0
        close_connection(conn)
        return odgovor
    except Exception as e:
        logging.exception("Nije moguce spremiti novog korisnika.") # Za ovo je potreban logging kojeg smo gore importali

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

################################
# Operacije nad skriptama #
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
            
# Kada obrisemo skriptu s prvim upitom, drugi upit dohvaca sve skripte i onda se salju na front
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

# Kada spremimo ocjene s prvim upitom, drugi upit dohvaca ponovno sve skripte i salje ih na front
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

##########################
# Operacije nad obavijestima #
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
