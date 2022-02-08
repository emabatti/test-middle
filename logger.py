import logging
import logging.handlers

class Logger(object): #classe che gestisce l'inserimento dei messaggi nei relativi file .log

    def __init__(self): #metodo costruttore
        self.formatter = logging.Formatter('%(asctime)s %(message)s') #definisce il formato che devono avere i log (<data-ora> <messaggio>)

        #configurazione handler log app
        self.appLogger = logging.getLogger("appLogger") #imposta il logger in maniera univoca, dandogli il nome appLogger
        self.appLogger.setLevel(logging.INFO) #tipologia di log che verranno inseriti nel file (INFO/DEBUG/ERR)
        self.appFH = logging.handlers.TimedRotatingFileHandler("log/app.log") #imposta il percorso e il nome del file di log. Eventualmente è possibile impostare un lasso di tempo dopo cui cancellare il file o rinominarlo e crearne uno nuovo parametrizzando la funzione TimedRotatingFileHandler
        self.appFH.setFormatter(self.formatter) #imposta il formato precedentemente definito
        #aggiungo handler su file
        self.appLogger.addHandler(self.appFH) #aggiunge l'handler al logger

        #configurazione handler log email
        self.emailLogger = logging.getLogger("emailLogger") #imposta il logger in maniera univoca, dandogli il nome emailLogger
        self.emailLogger.setLevel(logging.INFO)
        self.emailFH = logging.handlers.TimedRotatingFileHandler("log/email.log")
        self.emailFH.setFormatter(self.formatter)
        #aggiungo handler su file
        self.emailLogger.addHandler(self.emailFH)

        #configurazione handler log sms
        self.smsLogger = logging.getLogger("smsLogger") #imposta il logger in maniera univoca, dandogli il nome smsLogger
        self.smsLogger.setLevel(logging.INFO)
        self.smsFH = logging.handlers.TimedRotatingFileHandler("log/sms.log")
        self.smsFH.setFormatter(self.formatter)
        #aggiungo handler su file
        self.smsLogger.addHandler(self.smsFH)

        #dizionario contenente le varie funzioni di log. Viene utilizzato come switch statement per indirizzare correttamente i messaggi
        self.loggingFunctions = {
            "app":self.app,
            "email":self.email,
            "sms":self.sms
        }

    def info(self,logType,msg): #funzione che smista il messaggio da loggare verso il corretto file
        self.loggingFunctions[logType](msg)

    def app(self, msg): #inserimento messaggio in app.log
        self.appLogger.info(msg)

    def email(self, msg): #inserimento messaggio in email.log
        self.emailLogger.info(msg)

    def sms(self, msg): #inserimento messaggio in sms.log
        self.smsLogger.info(msg)