import logging
import azure.functions as func
import TeleBotAzureFUN.Telebot as TelegramBot

def main(req: func.HttpRequest) -> func.HttpResponse:
    #debug trace for azure
    #logging.info('Python HTTP trigger function processed a request.')
    #logging.info(req)
    try:
        req_body = req.get_json()
        message = req_body.get('message')
        if not message == None:
            processMessage(message)
        else :
            callback_query = req_body.get('callback_query')
            processCallback_query(callback_query)
    except Exception as e:
        logging.error(str(e) + '  nothing sennd to telegram , __init__.py')

    # resoponse to azure insight
    return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
    )

def processMessage(message):

    text = str(message.get('text'))
    chatid = str(message.get('chat').get('id'))
    #logging.info(message)
    if text.__contains__("/start"):
        TelegramBot.deployStart2(chatid)
        #logging.info('new chat at id :' + chatid)
    elif text.__contains__("/cambio"):
        valores = text.split()
        if len(valores) > 1:
            newID = int(valores[1])
            TelegramBot.changeRallyId(newID,chatid)
            #logging.info('rally id change')
    elif text.__contains__("/rally"):
        valores = text.split()
        if len(valores) > 1:
            driver = str(valores[1])
            TelegramBot.sendRallytimes(driver,chatid)
            #logging.info('rally data send')
        if len(valores) == 1:
            TelegramBot.sendRallytimes(None,chatid)
            #logging.info('rally data send')
    else:
        TelegramBot.echobot(text,chatid)
        #logging.info('response send to telegram')


def processCallback_query(callback_query):
    
    data = str(callback_query.get('data'))
    chatid = str(callback_query.get('from').get('id'))

    valores = data.split()
    if(valores[0]=="tiempo"):
        driver = str(valores[1])
        TelegramBot.sendRallytimes(driver,chatid)
        #logging.info('rally data send')
    if(valores[0]=="lista"):
        categoria = str(valores[1])
        TelegramBot.sendRallytimes2(categoria,chatid)
        #logging.info('rally data send')
        
    


