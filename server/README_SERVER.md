# Huffman Network Encoding – Server

Ovaj direktorij sadrži **serverski dio projekta** za kolegij NMR.
Server dohvaća tekstualni sadržaj web stranice, primjenjuje **Huffmanovo kodiranje**
i izlaže funkcionalnost putem **javnog REST API-ja**.

Server je **deployan na Render** i dostupan svim članovima tima.



## Javni server (Render)

**Base URL:**
```
https://huffman-network-encoding.onrender.com
```

### Dostupni endpointi

| Metoda | Ruta | Opis |
|------|------|------|
| GET | `/health` | Provjera dostupnosti servera |
| POST | `/encode` | Dohvat, kompresija i kodiranje web stranice |



## Funkcionalnost servera

Server radi sljedeće korake:

1. Prima URL web stranice
2. Dohvaća HTML sadržaj
3. Izdvaja tekst iz HTML oznaka:
   - `<h1>` – `<h6>`
   - `<p>`
4. Čisti i normalizira tekst
5. Tokenizira tekst (riječi + razmaci/interpunkcija)
6. Generira Huffmanovo stablo i kodove
7. Kodira tekst u binarni oblik
8. Vraća rezultat klijentu



## Struktura direktorija

```
server/
├── app.py               # Flask API (Render entry point)
├── server.py            # Lokalno pokretanje server pipeline-a
├── scraper.py           # Web scraping logika
├── huffman_encoder.py   # Huffman kodiranje
├── __init__.py
```



## Pokretanje servera (lokalno)

### Preduvjeti
- Python 3.10+
- Instalirane ovisnosti

Instalacija:
```bash
python -m pip install -r requirements.txt
```

### Lokalno pokretanje API-ja
```bash
python -m server.app
```

Server će biti dostupan na:
```
http://localhost:8000
```



## Korištenje API-ja

### Health check
```http
GET /health
```

Primjer odgovora:
```json
{"ok": true}
```



### Encode web stranice

```http
POST /encode
Content-Type: application/json
```

Body:
```json
{
  "url": "https://en.wikipedia.org/wiki/Lionel_Messi"
}
```



## Povratni podaci

| Polje | Opis |
|-----|-----|
| `title` | Naslov web stranice |
| `meta` | Statistika kompresije |
| `codes` | Huffmanov rječnik |
| `encoded_b64` | Binarnim podaci kodirani u Base64 |



## Namjena za tim

Ovaj server je namijenjen da ga:
- **klijentska aplikacija** koristi za dekodiranje
- **mrežna simulacija** koristi za prijenos podataka
- **Wireshark analiza** koristi za mjerenje prometa



## Napomene

- Server koristi **Render Free plan**
- Server se može “uspavati” nakon neaktivnosti
- Prvi zahtjev nakon pauze može biti sporiji



## Autor - Matej Banović

**Član 1 – Server**
- Web scraping
- Huffman kodiranje
- REST API
- Cloud deployment (Render)



Projekt je izrađen u edukativne svrhe u sklopu kolegija **NMR**.
