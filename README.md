# SD Organizer (Applicativo Desktop)

> Un'applicazione desktop Python/PyQt per automatizzare l'archiviazione, la rinomina e il backup di migliaia di foto in pochi secondi, risolvendo il problema dell'ordinamento manuale.

---

## 💡 Il Problema (Perché questo progetto?)

Dopo ogni shooting fotografico, mi trovavo a perdere ore in un processo manuale, noioso e ad alto rischio di errore:
* Copiare migliaia di file (JPG, RAW, video) da diverse schede SD.
* Creare manualmente cartelle per data e per evento.
* Rinominare ogni singolo file con un formato coerente.
* Assicurarmi che nulla andasse perso o sovrascritto.

## 🚀 La Soluzione (Cosa fa il progetto?)

Ho sviluppato **SD Organizer**, un'applicazione desktop con interfaccia grafica (PyQt) che automatizza l'intero processo.

L'utente collega la SD, sceglie la destinazione, inserisce un nome per l'evento e l'app analizza i metadati EXIF per leggere la data/ora di scatto, rinominare e spostare i file in una struttura di cartelle pulita e standardizzata (es: `Destinazione/NomeEvento/YYYY-MM-DD_Mese/`).

## 🎥 Demo Video

*(Questa è la prova per i recruiter non tecnici. Inserisci qui il link al tuo video)*

**[Guarda la Demo su YouTube](https://www.youtube.com/watch?v=L3OiWyBArJU)**

## 🛠️ Tecnologie Utilizzate (Skills Dimostrate)

*(Questa è la prova per i manager tecnici)*

* **Linguaggio:** Python
* **GUI:** PyQt6 (per l'interfaccia grafica)
* [cite_start]**Database:** SQLite (per catalogare i metadati delle foto e gestire i log) [cite: 13, 138]
* **Librerie Principali:** `Pillow` (per l'analisi dei metadati EXIF), `os`/`shutil` (per la gestione del file system)
* **Sviluppo AI:** Codice base generato e ottimizzato tramite "dialogo" con modelli LLM (Claude/Gemini) e poi integrato e debuggato manualmente.

## 🔑 Caratteristiche Principali

[cite_start]*(Elenco basato sul tuo Manuale Utente [cite: 1, 3, 10, 15, 16, 21])*

* [cite_start]**Importazione Flessibile:** Opzioni "Organize & Move" (sposta) o "Copy Only" (copia sicura)[cite: 3].
* [cite_start]**Rilevamento Automatico:** Refresh e rilevamento automatico delle SD Card collegate[cite: 1].
* [cite_start]**Funzione Multi-Evento:** Rileva automaticamente se sulla SD ci sono foto di date diverse e chiede all'utente di assegnare nomi evento diversi a ogni data[cite: 8, 9].
* [cite_start]**Struttura Logica:** Creazione automatica di cartelle (es: `NomeEvento/YYYY-MM-DD_Mese/`)[cite: 4, 14].
* [cite_start]**Rinomina Standardizzata:** Rinomina i file in un formato pulito (es: `IMG_0001_YYYYMMDD_HHMMSS.jpg`)[cite: 5].
* [cite_start]**Funzione "Annulla":** Possibilità di annullare l'ultima operazione tramite file di log dedicati[cite: 6].
* [cite_start]**Temi Personalizzabili:** Include diversi temi (Dark Mode, Forest, Professional, ecc.)[cite: 21].

## 📜 Licenza e Proprietà

*(Questa è la tua protezione anti-furto)*

**© 2024 Dmitrij Musella - Tutti i diritti riservati.**

Il codice sorgente di questo progetto è **privato** e non può essere copiato, modificato o distribuito senza esplicito consenso scritto da parte dell'autore.

Le demo video sono fornite a solo scopo dimostrativo del portfolio.
