import sys
from System.Net.Mail import SmtpClient, MailMessage, MailAddress
from System.Net import NetworkCredential
from Scripts.EnhancedRazorScripts.sys_Credentials import *

def sendEmailMessage(sub, tex):
    mail = MailMessage()
    mail.From = MailAddress(SERVICE_CREDENTIALS["gmail"]["email"]);


    smtp = SmtpClient()
    smtp.Port                  = 587;   
    smtp.EnableSsl             = True;
    #smtp.DeliveryMethod        = SmtpDeliveryMethod.Network; 
    ##smtp.UseDefaultCredentials = True; 
    smtp.Credentials = NetworkCredential(SERVICE_CREDENTIALS["gmail"]["email"],  SERVICE_CREDENTIALS["gmail"]["app_password"]);  
    smtp.Host        = SERVICE_CREDENTIALS["gmail"]["smtp"];            

    mail.To.Add(MailAddress(SERVICE_CREDENTIALS["mail_to"]["email"]));
    mail.IsBodyHtml = True;
    st              = "Test";
    mail.Subject = sub
    mail.Body = tex;
    smtp.Send(mail);