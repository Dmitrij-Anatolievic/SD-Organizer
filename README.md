# SD Organizer (Applicativo Desktop)

> Un'applicazione desktop Python/PyQt per automatizzare l'archiviazione, la rinomina e il backup di migliaia di foto in pochi secondi, risolvendo il problema dell'ordinamento manuale.

---

## 💡 Il Problema (Perché questo progetto?)

Dopo ogni shooting fotografico, mi trovavo a perdere ore in un processo manuale, noioso e ad alto rischio di errore:
* Copiare centinaia di file (JPG, RAW, video) da diverse schede SD.
* Creare manualmente cartelle per data e per evento.
* Rinominare ogni singolo file con un formato coerente.
* Assicurarmi che nulla andasse perso o sovrascritto.

## 🚀 La Soluzione (Cosa fa il progetto?)

Ho sviluppato **SD Organizer**, un'applicazione desktop con interfaccia grafica (PyQt) che automatizza l'intero processo.

L'utente collega la SD, sceglie la destinazione, inserisce un nome per l'evento e l'app analizza i metadati EXIF per leggere la data/ora di scatto, rinominare e spostare i file in una struttura di cartelle pulita e standardizzata (es: `Destinazione/NomeEvento/YYYY-MM-DD_Mese/`).

## 🎥 Demo Video

**[Guarda la Demo su YouTube](https://www.youtube.com/watch?v=L3OiWyBArJU)**

## 🛠️ Tecnologie Utilizzate

* **Linguaggio:** Python
* **GUI:** PyQt6 (per l'interfaccia grafica)
* **Librerie Principali:** `Pillow` (per l'analisi dei metadati EXIF), `os`/`shutil` (per la gestione del file system)
* **Sviluppo AI:** Codice base generato e ottimizzato tramite "dialogo" con modelli LLM (Claude/Gemini) e poi integrato e debuggato manualmente.

## 🔑 Caratteristiche Principali

* **Importazione Flessibile:** Opzioni "Organize & Move" (sposta) o "Copy Only" (copia sicura).
* **Rilevamento Automatico:** Refresh e rilevamento automatico delle SD Card collegate.
* **Funzione Multi-Evento:** Rileva automaticamente se sulla SD ci sono foto di date diverse e chiede all'utente di assegnare nomi evento diversi a ogni data.
* **Struttura Logica:** Creazione automatica di cartelle (es: `NomeEvento/YYYY-MM-DD_Mese/`)
* **Rinomina Standardizzata:** Rinomina i file in un formato pulito (es: `IMG_0001_YYYYMMDD_HHMMSS.jpg`).
* **Funzione "Annulla":** Possibilità di annullare l'ultima operazione tramite file di log dedicato.
* **Temi Personalizzabili:** Include diversi temi (Dark Mode, Forest, Professional, ecc.).

## 📜 Licenza e Proprietà

**© 2025 Dmitrij Musella - Tutti i diritti riservati.**

Il codice sorgente di questo progetto è **privato** e non può essere copiato, modificato o distribuito senza esplicito consenso scritto da parte dell'autore.

Le demo video sono fornite a solo scopo dimostrativo del portfolio.
