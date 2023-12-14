import logging
import requests
import TeleBotAzureFUN.DataProvider as webData
import TeleBotAzureFUN.VaultProvider as vault

def __auxTelegramSender(acction:str,requestData:dict):

    try:
        ApItoken = vault.getApiToken()

        #logging.info("buiding telegram api request")

        requests.post('https://api.telegram.org/bot'+ApItoken+acction, json = requestData)

        pass

    except:

        logging.warning("telegram api request failture")

#echo to telegram
def echobot(msg:str,chat_id:str):
    
    #logging.info("calling aux method")
    __auxTelegramSender(
        acction='/sendmessage',
        requestData={'text':msg,'chat_id':chat_id,'parse_mode':'HTML'}
    )

    pass

def changeRallyId(id:int,chat_id:str):
    if id > 0:
        oldid = vault.getRallyId()
        vault.setRallyId(id)
        newid = vault.getRallyId()
        echobot("old rally id: "+ oldid +"\nnew rally id :"+ newid,chat_id)
    pass

def deployStart(chat_id:str):
    rallyid = vault.getRallyId()
    driversWRC,driversWRC2,RallyTittle =  webData.getRallyDrivers(rallyid)
    keyboard = __buildDriversKeyboard(driversWRC,driversWRC2)
    __sendinlineKeyboard(keyboard,str(RallyTittle) + "\nlista de pilotos",chat_id)

def deployStart2(chat_id:str):
    __buildAndSendStartKeyboard(chat_id)

def __buildAndSendStartKeyboard(chatid:str):
    
    kbutons = []
    
    kbutons.append([dict({"text": "WRC","callback_data": "lista 4x4"})])

    kbutons.append([dict({"text": "WRC2","callback_data": "lista wrc2"})])

    kbutons.append([dict({"text": "ALL","callback_data": "lista all"})])
    
    inlinekeyboard = dict({'inline_keyboard':kbutons})

    rallyid = vault.getRallyId()
    RallyTittle =  webData.getRallyTittle(rallyid)

    __auxTelegramSender(
        acction='/sendmessage',
        requestData={'text':RallyTittle,'chat_id':chatid,'reply_markup':inlinekeyboard}
    )

def sendRallytimes2(categoria:str,chat_id:str):
    if "all" in categoria:
        deployStart(chat_id=chat_id)
    elif "4x4" in categoria:
        rallyid = vault.getRallyId()
        driversWRC,driversWRC2,RallyTittle =  webData.getRallyDrivers(rallyid)
        keyboard = __buildDriversKeyboardSingle(driversWRC)
        __sendinlineKeyboard(keyboard,str(RallyTittle) + "\nlista de pilotos WRC",chat_id)
    elif "wrc2" in categoria:
        rallyid = vault.getRallyId()
        driversWRC,driversWRC2,RallyTittle =  webData.getRallyDrivers(rallyid)
        keyboard = __buildDriversKeyboardSingle(driversWRC2)
        __sendinlineKeyboard(keyboard,str(RallyTittle) + "\nlista de pilotos WRC2",chat_id)

def sendRallytimes(driver:str,chat_id:str):
    rallyid = vault.getRallyId()
    text =  webData.getRallyData(driver,rallyid)
    echobot(text,chat_id)


def __buildDriversKeyboardSingle(drivers:list) -> str:
    
    driversbuttons = []
    for d in drivers:
        driversbuttons.append([dict({"text": str(d),"callback_data": "tiempo "+str(d)})])
    
    inlinekeyboard = dict({'inline_keyboard':driversbuttons})

    return inlinekeyboard


def __buildDriversKeyboard(drivers:list,driversm:list) -> str:
    
    driversbuttons = []
    for d in drivers:
        driversbuttons.append([dict({"text": str(d),"callback_data": "tiempo "+str(d)})])
    for d in driversm:
        if not d in drivers:
            driverbutton = dict({"text": str(d),"callback_data": "tiempo "+str(d)})
            line = [driverbutton]
            driversbuttons.append(line)

    inlinekeyboard = dict({'inline_keyboard':driversbuttons})

    return inlinekeyboard

def __sendinlineKeyboard(keyboard:dict,text:str,chatid:str):
    
    __auxTelegramSender(
        acction='/sendmessage',
        requestData={'text':text,'chat_id':chatid,'reply_markup':keyboard}
    )








    

        


    
    

    