# -*- coding: utf-8 -*-
__author__ = "Øyvind Jekteberg and Kristian Gingstad"
__copyright__ = "Copyright 2018, The ArXivDigest Project"
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader


def mailrender(data, template, env):
    '''Puts data into mail template'''
    template = env.get_template(template + '.tmpl')
    return template.render(data)


def assembleMail(message, toadd, fromadd, subject):
    '''Adds to and from address and subject to mail'''
    message = MIMEText(message, 'html')
    message['From'] = fromadd
    message['To'] = toadd
    message['Subject'] = subject
    return message.as_string()


class mailServer():

    def __init__(self, fromadd, password, host, port, templates):
        '''Starts and logs into mail server'''
        self.fromadd = fromadd
        self.server = smtplib.SMTP(host, port)
        self.server.starttls()
        self.server.login(self.fromadd, password)
        self.env = Environment(loader=FileSystemLoader(templates))

    def close(self):
        self.server.quit()

    def sendMail(self, toadd, subject, data, template):
        '''Creates mail and sends it'''
        content = mailrender(data, template, self.env)
        mail = assembleMail(content, self.fromadd, toadd, subject)
        return self.server.sendmail(self.fromadd, toadd, mail)
