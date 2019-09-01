from flask import Flask, Response, jsonify, request
import datetime as dt
import domain as db
import simplejson as json
from flask_cors import CORS          #Cross Origin Resource Sharing - komunikacija s frontendom

app = Flask(__name__)
# Dodajemo app u CORS kako bi bili u mogucnosti komunicirati s frontendom
CORS(app)

# Error funkcija
def error(status=500, text='Doslo je do greške'):
    return jsonify({"error": text}), status

@app.route('/')
def hello():
    return jsonify({
        'status' : 'uspješno'
    })



########### Za klasu Korisnik ############

#   Dodavanje novog korisnika  #
@app.route('/korisnik/registracija', methods=['GET', 'POST', 'PUT'])
def handle_korisnik_get_post():
    if request.method == 'POST':
        data = request.get_json()
        ime = data.get('ime')
        prezime = data.get('prezime')
        email = data.get('email')
        lozinka = data.get('lozinka')
        grad_studiranja = data.get('gradStudiranja')
        sveuciliste = data.get('sveuciliste')
        smjer = data.get('smjer')
        id_ = db.novi_korisnik(ime, prezime, email, lozinka, grad_studiranja, sveuciliste, smjer)
        if id_ == None:
            #Pozivamo error funkciju
            return error()
        else:
            return jsonify({
                'status' : 'success',
                'data' : id_
            })
    elif request.method == 'PUT':
        data = request.get_json()
        id = data.get('id')
        ime = data.get('ime')
        prezime = data.get('prezime')
        email = data.get('email')
        lozinka = data.get('lozinka')
        grad_studiranja = data.get('gradStudiranja')
        sveuciliste = data.get('sveuciliste')
        smjer = data.get('smjer')
        odg = db.uredi_korisnika(id, ime, prezime, email, lozinka, grad_studiranja, sveuciliste, smjer)
        if odg == False:
            #Pozivamo error funkciju
            return error()
        else:
            return jsonify({
                'status' : 'success',
                'data' : odg
            })

#   Prijava postojeceg korisnika  #
@app.route('/korisnik/prijava', methods=['POST'])
def prijava_korisnika():
    data = request.get_json()
    # U frontendu se mora navesti 'email' i 'password' u poketu koji saljes za backend kako bi ga mogao iscitati ovdje
    email = data.get('email')
    lozinka = data.get('lozinka')
    # Pozivamo klasu Korisnik s funkcijom prijava i saljemo parametre. Vracene podatke spremamo u objekt 'korisnik'
    korisnik = db.prijava(email, lozinka)
    if korisnik == None:
        return error()
    else:
        return jsonify({
            'status' : 'success',
            # vraca sve korisnikove podatke
            'korisnik' : korisnik
        })

@app.route('/korisnik/prijava/admin', methods=['POST'])
def prijava_admina():
    data = request.get_json()
    ime = data.get('email')
    lozinka = data.get('lozinka')
    admin = db.prijava_admin(ime, lozinka)
    if admin == None:
        return error()
    else:
        return jsonify({
            'status' : 'success',
            # vraca sve korisnikove podatke
            'admin' : admin
        })

##################################################

########### Za klasu Skripte ############

#   Dodavanje nove skripte   #
@app.route('/skripte', methods=['GET', 'POST', 'PUT'])
def handle_skripte():
    if request.method == 'GET':
        skripte = db.dohvati_skripte()
        return jsonify({
            'status' : 'success',
            'skripte' : skripte
        })
    elif request.method == 'POST':
        post_data = request.get_json()
        id_korisnik = post_data.get("korisnikId")
        naziv = post_data.get("naziv")
        ocjena = post_data.get("ocjena")
        dokument = post_data.get("skripta")
        datum_spremanja = post_data.get("datumSpremanja")
        skripta = db.spremi_skriptu(id_korisnik, naziv, ocjena, dokument, datum_spremanja)
        if skripta == None:
            return error()
        else:
            return jsonify({
                'status' : 'success',
                'skripta' : skripta
            })
    elif request.method == 'PUT':
        post_data = request.get_json()
        id_skripta = post_data.get("skriptaId")
        ocijena = post_data.get("ocijena")
        skripte = db.azurirajOcijene(id_skripta, ocijena)
        return jsonify({
            'status' : 'success',
            'skripte' : skripte
        })

@app.route('/skripte/brisanje', methods=['PUT'])
def handle_skripte_brisanje():
    post_data = request.get_json()
    id_skripta = post_data.get("skriptaId")
    skripte = db.obrisi_skriptu(id_skripta)
    return jsonify({
        'status' : 'success',
        'skripte' : skripte
    })

##################################################

########### Za klasu Obavijesti ############

@app.route('/obavijesti', methods=['GET', 'POST', 'PUT'])
def handle_obavijesti():
    if request.method == 'GET':
        obavijesti = db.dohvati_obavijesti()
        return jsonify({
            'status' : 'success',
            'obavijesti' : obavijesti
        })
    elif request.method == 'POST':
        post_data = request.get_json()
        naslov = post_data.get("naslov")
        tekst = post_data.get("tekst")
        datum_objave = post_data.get("datumObjave")
        id_ = db.spremi_obavjest(naslov, tekst, datum_objave)
        if id_ == None:
            return error()
        else:
            return jsonify({
                'status' : 'success'
        })
    elif request.method == 'PUT':
        post_data = request.get_json()
        naslov = post_data.get("naslov")
        tekst = post_data.get("tekst")
        db.azuriraj_obavjest(naslov, tekst, datum_objave)
        return jsonify({
            'status' : 'success',
            'obavijesti' : obavijesti
        })


if __name__ == "__main__":
    app.debug = True
    app.run()
