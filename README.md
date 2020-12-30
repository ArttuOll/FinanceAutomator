# Finance Automator

Henkilökohtaiseen tulojen ja kulujen seurantaan käytettävä komentoriviohjelma.

## Toiminnallisuus

Finance Automator lukee muodossa "Päivämäärä";"Saaja/Maksaja";"Selite";"Viite/Viesti";"Määrä" olevia
tilitapahtumatiedostoja ja niiden perusteella laskee arvon kutakin käyttäjän asettamaa laskenta-
kategoriaa kohti. Laskentakategoriat määritetään ohjelman asetustiedostossa kohdassa
`categories_tags` (ks. esimerkkiasetustiedosto alla). Tilitapahtumatiedoston lukeminen tapahtuu
komennolla `fina read TIEDOSTOPOLKU`.

Kun tilitapahtumatiedosto on luettu, kirjoittaa ohjelma siitä automaattisesti raportin (ks.
esimerkkiraportti alla). Raportti tallennetaan asetustiedoston kohdassa `save_dir` määritettyyn 
hakemistoon, tiedostoon nimeltä `fina_reports.txt`. Kaikki raportit tallennetaan tähän tiedostoon.
Samaan hakemistoon tallentuu myös tiedosto nimeltä `fina_reports_mr.txt`, joka on koneluettava
(JSON-muotoinen) versio raporttitiedostosta. Finance Automator käyttää sitä raporttien
ohjelmalliseen käsittelemiseen.

Raporttien kirjoittamisen lisäksi ohjelma kykenee tuottamaan myös alkeellista analytiikkaa.
Komennolla `fina avg` tuotetaan raportti, johon on laskettu kaikkien kategorioiden arvojen 
keskiarvo käyttäjän määrittämällä aikavälillä. (Lisätietoja ks. `fina avg --help`). Komennolla
`fina sum` puolestaan voidaan tuottaa vastaavanlainen summaraportti. Viimeiseksi, ohjelma kykenee
piirtämään kuvaajia tietyn kategorian arvoista viimeisen vuoden aikana komennon
`fina graph`-avulla.

## Asetusten asettaminen

Asetukset voidaan asettaa manuaalisesti luomalla tiedosto nimeltä `.fina_configs.json` käyttäjän
kotikansioon ja kirjoittamalla sen sisältö alla olevan mallin mukaisesti. Asetukset pystyy myös
asettamaan ohjatusti komennolla `fina guided-config`.

`save_dir` on polku siihen kansioon, johon raportit tallennetaan.
`categories_tags` -kohdan aaltosulkujen sisälle kirjoitetaan ensin kategoria, joka talousraporttiin
halutaan (esim. "Ruoka") ja sen perään lista tunnisteista, jotka esiintyvät tähän kategoriaan
kuuluvien tilitapahtumien Saaja/Maksaja-kentissä.

```
Esimerkki asetustiedosto.

{
    "save_dir": "path/to/dir/where/reports/are/saved",
    "categories_tags": {
        "Ruoka": [
            "market",
            "sale",
            "prisma"
        ],
        "Internet ja puhelin": [
            "internetpalveluntarjoaja X",
            "internetpalveluntarjoaja Y"
        ],
        "Sähkö": [
            "Sähköfirma X",
            "Sähköfirma K"
        ],
        "Urheilu": [
            "Saliketju"
        ]
    }
}
```
```
Esimerkkiraportti

Talousraportti 2020-12-30
Ruoka: -200
Internet ja puhelin: -80
Sähkö: -44.02
Urheilu: -7.9
Tulot yht.: POSITIIVISTEN TILITAPAHTUMIEN SUMMA
Muut tulot: KATEGORIOIHIN KUULUMATTOMAT POSITIIVISET TILITAPAHTUMAT
Menot yht.: NEGATIIVISTEN TILITAPAHTUMIEN SUMMA
Muut menot: KATEGORIOIHIN KUULUMATTOMAT NEGATIIVISET TILITAPAHTUMAT
Tase: TULOT - MENOT
```

## Käyttöliittymä

```
Usage: fina [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Lisää ulostulon määrää
  --help         Show this message and exit.

Commands:
  avg            Laske kulu- ja menokategorioiden keskiarvot aikaväliä kohti
  graph          Piirrä kuvaaja kategorian arvoista aikavälillä
  guided-config  Suorita ohjattu asetustiedoston luominen
  read           Lue tilitapahtumatiedosto ja kirjoita siitä raportti
  sum            Laske kulu- ja menokategorioiden arvoja yhteen aikavälillä
```
