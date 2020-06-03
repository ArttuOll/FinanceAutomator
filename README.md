# FinanceAutomator
Automatisoi henkilökohtaisen talousseurannan ylläpitämällä xlsx-laskentataulukkoa, johon käyttäjän kuukausittaiset tulot ja menot kirjataan.

Ohjelman kulku:

1. Käyttäjä antaa ohjelmalle tiedostopolun hakemistoon, joka sisältää käyttäjän viime kuukauden tilitapahtumat.
2. Käyttäjä antaa ohjelmalle tiedostopolun hakemistoon, joka sisältää käyttäjän viime kuukauden tiliotteen.
2. Käyttäjä antaa ohjelmalle kategorian, jolle hän haluaa arvon laskettavan viime kuukauden tilitapahtumista. Esim. "ruokaostokset".
3. Käyttäjä antaa ohjelmalle tunnisteita, joita ohjelma käyttää tunnistaakseen tilitapahtumat, jotka kuuluvat edellä annettuun kategoriaan. Esim. "market" tai "lidl".
4. Ohjelma laskee tilitapahtumien summat annettujen kategorioiden ja tunnisteiden perusteella ja kirjoittaa tulokset tiedostoon "talousseuranta_<kuukauden numero>.xlsx aiemmin määritettyyn sijaintiin.
5. Seuraavilla käynnistyskerroilla ohjelma muistaa käyttäjän aiemmat asetukset, mutta niitä on mahdollisuus muuttaa. 
6. Uusien merkintöjen tekeminen tapahtuu poistamalla tilitapahtumat sisältävästä kansiosta edellinen tilitapahtumatiedosto ja korvaamalla se uudella ja ajamalla ohjelma uudelleen.
