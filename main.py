import json
from fastapi import FastAPI #framework per la creazione dei serizi API
from datetime import date
import aiomysql
import logger

app = FastAPI() #crea oggetto che si occupa di ricevere le varie chiamate e smistarle adeguatamente
log = logger.Logger() #crea oggetto logger (vedere classe Logger in file logger.py)

with open('config.json') as config_file: #apre il file di configurazione e ne importa il contenuto all'interno del dizionario configData
    configData = json.load(config_file)

@app.get("/") #greeting del servizio API. Viene chiamato con call GET senza impostare parametri
async def read_root():
    return {"Message": "Servizio API REST - test back end middle"}


@app.post("/send/{type}") #funzione send che si occupa dell'invio di una mail o un sms ad un utente casuale. Chiamata con call POST. Riceve il tipo di destinatario in formato stringa
async def read_item(type: str):
    if type in ["email","sms"]: #verifica che il tipo fornito dall'utente sia compreso nella lista di quelli definiti
        log.info("app","Chiamata effettuata - type: " + type) #log in file app.log
        try:
            MysqlDB = await aiomysql.connect(host=configData['mysql']['host'],db=configData['mysql']['database'],user=configData['mysql']['user'],password=configData['mysql']['password'],autocommit=True) #crea connessione al database mysql utilizzando come parametri quelli ricavati dal file di configurazione
        except:
            return {"Errore": "Database non raggiungibile"} #segnala l'utente che la connessione al db non è andata a buon fine
        cur = await MysqlDB.cursor(aiomysql.DictCursor) #oggetto di tipo cursore utilizzato per le query sul database. il parametro DictCursor fa in modo che i risultati delle query vengano forniti sottoforma di dizionario chiave-valore
        await cur.execute("select users.id,name,lastname,birthdate,isActive,email,phone from users left join emails on users.id=emails.id_user left join phones on users.id=phones.id_user order by rand() limit 1;") #seleziona in maniera randomica i dati dell'utente dalla tabella users, affiancandogli i relativi valori email ed sms. Se questi non sono presenti, vengono restituiti come null
        userData = await cur.fetchone()

        resDict = {"tipo":type, "nome":userData["name"], "cognome":userData["lastname"]} #crea dizionario per l'esito e lo valorizza con i dati iniziali dell'utente

        todayDate = date.today()
        resDict["anni"] = todayDate.year - userData["birthdate"].year - ((todayDate.month, todayDate.day) < (userData["birthdate"].month, userData["birthdate"].day)) #calcola l'età dell'utente preso in carico, facendo la differenza tra l'anno di nascita e quello odierno. Sottrae al risultato 1 anno se la combinazione mese-anno attuale è minore di quella di nascita
        if resDict["anni"] >= 18: #verifica che l'utente sia maggiorenne
            if userData["isActive"] > 0: #verifica che l'utente sia attivo
                if type == "email":
                    #perché siano considerati valorizzati, i valori email ed sms non devono essere NULL o ""
                    if userData["email"]:
                        resDict["invio"] = "[OK] " + userData["email"]
                        await cur.execute("update users set n_mails=if(n_mails is null,1,n_mails+1) where id=" + str(userData["id"])) #incrementa di 1 il contatore delle mail inviate all'utente (se il valore iniziale è null, lo imposta a 1)
                    else:
                        resDict["invio"] = "[ERRORE] Email non valorizzata"
                else:
                    if userData["phone"]:
                        resDict["invio"] = "[OK] " + userData["phone"]
                        await cur.execute("update users set n_sms=if(n_sms is null,1,n_sms+1) where id=" + str(userData["id"])) #incrementa di 1 il contatore degli sms inviati all'utente (se il valore iniziale è null, lo imposta a 1)
                    else:
                        resDict["invio"] = "[ERRORE] Numero di telefono non valorizzato"
            else:
                resDict["invio"] = "[ERRORE] Utente disattivo"
        else:
            resDict["invio"] = "[ERRORE] Utente minorenne"
        log.info(type,json.dumps(resDict)) #log in file email.log o sms.log, a seconda del tipo selezionato dall'utente in fase di chiamata
        return resDict #restituisce l'esito all'utente
    else:
        return {"Errore": "Tipo " + type + " inesistente"}