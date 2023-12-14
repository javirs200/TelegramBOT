import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# module for azure keyvault

try:
    __credential = DefaultAzureCredential()
    __secret_client = SecretClient(vault_url="https://telebot.vault.azure.net//", credential=__credential)
except:
    logging.warning("keyvault credentials warning")

def getApiToken() -> str : 
    try:
        ApItoken = str(__secret_client.get_secret("apitoken").value)
        return ApItoken
    except:
        logging.warning("azure credential warning , claimApiToken")
        return "  "

def getRallyId() -> str : 
    try:
        RallyID = str(__secret_client.get_secret("RallyID").value)
        return RallyID
    except:
        logging.warning("azure credential warning , GettRallyId method")
        return "  "

def setRallyId(id:int): 
    try:
        __secret_client.set_secret("RallyID",id)
    except:
        logging.warning("setRallyId warning not set value")