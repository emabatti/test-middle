import logging
import logging.handlers

class Logger(object):

    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s %(message)s')

        #configurazione handler log app
        self.appLogger = logging.getLogger("appLogger")
        self.appLogger.setLevel(logging.INFO)
        self.appFH = logging.handlers.TimedRotatingFileHandler("log/app.log")
        self.appFH.setFormatter(self.formatter)
        #aggiungo handler su file
        self.appLogger.addHandler(self.appFH)

        #configurazione handler log email
        self.emailLogger = logging.getLogger("emailLogger")
        self.emailLogger.setLevel(logging.INFO)
        self.emailFH = logging.handlers.TimedRotatingFileHandler("log/email.log")
        self.emailFH.setFormatter(self.formatter)
        #aggiungo handler su file
        self.emailLogger.addHandler(self.emailFH)

        #configurazione handler log sms
        self.smsLogger = logging.getLogger("smsLogger")
        self.smsLogger.setLevel(logging.INFO)
        self.smsFH = logging.handlers.TimedRotatingFileHandler("log/sms.log")
        self.smsFH.setFormatter(self.formatter)
        #aggiungo handler su file
        self.smsLogger.addHandler(self.smsFH)

        self.loggingFunctions = {
            "app":self.app,
            "email":self.email,
            "sms":self.sms
        }

    def info(self,logType,msg):
        self.loggingFunctions[logType](msg)

    def app(self, msg):
        self.appLogger.info(msg)

    def email(self, msg):
        self.emailLogger.info(msg)

    def sms(self, msg):
        self.smsLogger.info(msg)