# Prova per programmatore back end middle level

Il presente progetto consiste in un servizio API REST che si occupa di:

- Ricevere in POST all'indirizzo **/send/{type}** il tipo di destinatario. Le due possibili opzioni sono `email` e `sms`.
- Selezionare un utente da una tabella `users` presente su database
- Verificare che l'utente sia valido, ovvero:
  - Che sia maggiorenne
  - Che sia attivo
  - Che il relativo `type` fornito sia presente e valorizzato per l'utente in questione
- Eseguite queste verifiche, il servizio si occuperà quindi di incrementare il contatore del `type` scelto per l'utente preso in carico e inviare una conferma al mittente della richiesta
- Tutte queste operazioni, compreso l'esito, vengono tracciate nei relativi file di log presenti nella sottocartella log

## Requisiti

Il servizio è stato sviluppato per Windows 10, ma è funzionante e testato anche per Centos 7 e 8 su base Linux.
I requisiti necessari per la modifica e l'avvio del codice sorgente sono i seguenti:
- **Python v. 3.6** o superiore
- **pip**, con il quale installare i seguenti moduli:
  - FastApi: framework utilizzato per la gestione delle chiamate API - `pip install fastapi`
  - JSON: modulo per il parsing dei dizionari da e verso il formato JSON - `pip install json`
  - aioMySQL: versione asincrona della libreria PyMySQL, la quale verrà installata insieme alla presente, necessaria per la connessione al db - `pip install aiomysql`
  - Uvicorn: servizio necessario per l'avvio del server API - `pip install "uvicorn[standard]"`
- Un client o servizio web in grado di inviare richieste in POST (utilizzato per le prove e lo sviluppo: Postman)

## Struttura

Il servizio è strutturato da tre file principali:
- **main.py**: pagina principale, in cui sono presenti le dichiarazioni degli oggetti necessari e la struttura della chiamata POST sopra descritta. Per completismo, è presente anche una chiamata che fornisce una stringa di presentazione, accessibile chiamando l'API in GET senza fornire parametri
- **logger.py**: file contenente la dichiarazione della classe Logger, ovvero il sistema che si occupa di smistare i log da salvare nei relativi file `app.log` (log chiamate effettuate), `email.log` (log esito richiesta invio email) e `sms.log` (log esito richiesta invio sms). Questi tre file possono essere trovati all'interno della sottocartella **log**.
- **config.json**: file di configurazione contenente i parametri necessari alla connessione al database MySql

## Avvio

Per avviare il progetto, è sufficiente accedere da terminale alla cartella dov'è situato il file `main.py` e utilizzare la libreria **Uvicorn** precedentemente installata:
```
uvicorn main:app --reload
```
La dicitura `--reload` permette il ricaricamento automatico del codice da parte di Uvicorn in caso di modifiche dello stesso.

Una volta avviato il servizio, è possibile chiamare liberamente l'API sopra descritta, indicandone il relativo indirizzo ip. Di seguito vengono elencati degli esempi di chiamata effettuati in localhost (IP 127.0.0.1):

### Richiesta invio mail

![immagine](https://user-images.githubusercontent.com/94850016/153079116-124c2ad0-45af-467f-ac0b-0be4d44b6c98.png)

### Richiesta invio sms

![immagine](https://user-images.githubusercontent.com/94850016/153079227-792622c6-8938-48f0-aa55-654eedc95a85.png)

Una volta ricevuta la richiesta, il servizio risponderà con i dati dell'utente e l'indirizzo o il numero di telefono a cui è stato effettuato l'invio:

```json
{
    "tipo": "email",
    "nome": "Stephen",
    "cognome": "King",
    "anni": 74,
    "invio": "[OK] stephen.king@gmail.com"
}
```

Nel caso di errori, il motivo del mancato invio verrà visualizzato nell campo `invio`:

```json
{
    "tipo": "sms",
    "nome": "Paola",
    "cognome": "Miasmi",
    "anni": 37,
    "invio": "[ERRORE] Utente disattivo"
}
```
