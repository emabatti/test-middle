from typing import Optional
from urllib import response
from fastapi import FastAPI
import aiomysql

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/send/{type}")
async def read_item(type: str):
    if type in ["email","sms"]:
        try:
            MysqlDB = await aiomysql.connect(host="127.0.0.1",db="Test_middle",user="root",password="",autocommit=True)
        except:
            return {"Errore": "Database non raggiungibile"}
        cur = await MysqlDB.cursor()
        await cur.execute("select users.id,name,lastname,email,phone from users left join emails on users.id=emails.id_user left join phones on users.id=phones.id_user order by rand() limit 1;")
        userData = await cur.fetchone()
        resDict = {"Tipo selezionato": type, "Nome":userData[1], "Cognome":userData[2]}
        if type == "email":
            if userData[3]:
                resDict["Email"] = userData[3]
            else:
                resDict["Email"] = "Email non valorizzata"
        else:
            if userData[4]:
                resDict["Phone"] = userData[4]
            else:
                resDict["Phone"] = "Phone non valorizzato"
        return resDict
    else:
        return {"Errore": "Tipo " + type + " inesistente"}