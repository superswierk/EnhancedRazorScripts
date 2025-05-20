def sendDiscord(message):
    try:
        Misc.Resync()
        URI = 'https://discord.com/api/webhooks/XXXXXXXXXXXXX'# your webhook url string 
        alert = message  ####WHAT TO ALERT
        report = "username=" + Player.Name + "&content=" + alert
        PARAMETERS=report
        from System.Net import WebRequest
        request = WebRequest.Create(URI)
        request.ContentType = "application/x-www-form-urlencoded"
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
