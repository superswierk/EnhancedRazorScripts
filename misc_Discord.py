import clr
clr.AddReference('System.Web.Extensions') # Dodaj referencję do biblioteki zawierającej JavaScriptSerializer
from System.Web.Script.Serialization import JavaScriptSerializer
from System.Collections.Generic import Dictionary, List # Potrzebne do tworzenia obiektów, które serializator zrozumie

serializer = JavaScriptSerializer()

'''
config_data = {
    "auto_loot_items": [
        {"graphic": 0x098A, "color": 0x0000, "name": "Gold"},
        {"graphic": 0x0F0C, "color": 0x0000, "name": "Bandages"}
    ],
    "healing_settings": {
        "use_bandages": True,
        "min_hp_percent": 70
    },
    "player_name": Player.Name
}
'''



# JavaScriptSerializer najlepiej działa ze słownikami .NET (Dictionary) i listami .NET (List)
# Chociaż IronPython często konwertuje słowniki Pythona, jawna konwersja jest bezpieczniejsza.
def python_dict_to_net_dict(py_dict):
    net_dict = Dictionary[str, object]()
    for key, value in py_dict.items():
        if isinstance(value, dict):
            net_dict[key] = python_dict_to_net_dict(value)
        elif isinstance(value, list):
            net_dict[key] = python_list_to_net_list(value)
        else:
            net_dict[key] = value
    return net_dict

def python_list_to_net_list(py_list):
    net_list = List[object]()
    for item in py_list:
        if isinstance(item, dict):
            net_list.Add(python_dict_to_net_dict(item))
        elif isinstance(item, list):
            net_list.Add(python_list_to_net_list(item))
        else:
            net_list.Add(item)
    return net_list
    

def sendDiscord(message, color = 14696255, thumbnail = "", scriptName = Misc.ScriptCurrent(False)):
    try:
        Misc.Resync()
        if thumbnail == "":
            config_data = {
                "attachments": [
                    
                ],
                "embeds": [
                    {"title": Player.Name, "color": color, "description": "**"+message+"**", "footer": { "text": scriptName } },
                ],
                "content": None,
                "avatar_url": "https://i.imgur.com/l1xQeLU.jpeg",
                "username": "UltimaBot"
            }
        else:
            config_data = {
                "attachments": [
                    
                ],
                "embeds": [
                    {"title": Player.Name, "color": color,"thumbnail" :  { "url": thumbnail } , "description": "**"+message+"**", "footer": { "text": scriptName } },
                ],
                "content": None,
                "avatar_url": "https://i.imgur.com/l1xQeLU.jpeg",
                "username": "UltimaBot"
            }
        net_config_data = python_dict_to_net_dict(config_data)
        json_string = serializer.Serialize(net_config_data)
        print(json_string)
        URI = 'https://discord.com/api/webhooks/XXXXXXXXXXXXX'# your webhook url string 
        report = json_string
        PARAMETERS=report
        from System.Net import WebRequest
        request = WebRequest.Create(URI)
        request.ContentType = "application/json"
        request.Method = "POST"
        from System.Text import Encoding
        bytes = Encoding.ASCII.GetBytes(PARAMETERS)
        request.ContentLength = bytes.Length
        reqStream = request.GetRequestStream()
        reqStream.Write(bytes, 0, bytes.Length)
        reqStream.Close()
        response = request.GetResponse()
        rdata = response.GetResponseStream()
        from System.IO import StreamReader
        result = StreamReader(rdata).ReadToEnd().replace('\r', '\n')
        response.Close()
        rdata.Close()
    except Exception as e:
        print("Error Discord Sending : ",e)
