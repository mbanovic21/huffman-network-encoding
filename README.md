# huffman-network-encoding
Implementation of Huffman data compression for efficient network transmission, including web scraping, server-client communication, and traffic analysis in IMUNES.

# Huffman Network Data Encoding

Ovaj projekt demonstrira **kodiranje i prijenos podataka putem računalne mreže korištenjem Huffmanovog algoritma**. Cilj je smanjiti količinu podataka koji se prenose mrežom primjenom entropijskog kodiranja te analizirati mrežni promet u simuliranom okruženju.

Projekt kombinira:
- algoritme kompresije podataka
- klijent–poslužitelj arhitekturu
- simulaciju mreže u IMUNES-u
- analizu prometa pomoću Wiresharka


## Cilj projekta

- Implementirati Huffmanovo kodiranje za kompresiju tekstualnih podataka
- Smanjiti veličinu podataka prije mrežnog prijenosa
- Simulirati prijenos podataka u računalnoj mreži
- Dekodirati podatke na klijentskoj strani i potvrditi ispravnost
- Analizirati mrežni promet i tipove paketa



## Korištene tehnologije

- **Python**
  - `requests`
  - `BeautifulSoup`
- **Huffmanov algoritam**
- **IMUNES** – mrežna simulacija
- **Wireshark** – analiza mrežnog prometa
- **TCP/IP, HTTP**



## Arhitektura sustava

- **Poslužitelj**
  - dohvaća web stranicu (web scraping)
  - analizira tekst
  - generira Huffmanovo stablo i kodove
  - sprema kodirane podatke

- **Klijenti**
  - šalju zahtjeve poslužitelju
  - preuzimaju kodirane datoteke
  - dekodiraju podatke
  - uspoređuju rezultat s izvornim tekstom

- **Mreža**
  - simulirana u IMUNES-u
  - definirana IP adresama unutar subneta `172.16.0.0/16`



## Struktura projekta

```text
.
├── server/
│   ├── scraper.py
│   ├── huffman_encoder.py
│   ├── huffman_codes.json
│   └── encoded_data.bin
│
├── client/
│   ├── huffman_decoder.py
│   └── received_data.bin
│
├── network/
│   └── topology.imn
│
├── docs/
│   ├── wireshark_analysis.pdf
│   └── screenshots/
│
└── README.md
