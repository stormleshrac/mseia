#Creadores ~UserDev~ y ~TechDev~
from cProfile import run
import pstats
from pyobigram.utils import sizeof_fmt,get_file_size,createID,nice_time
from pyobigram.client import TechDevClient,inlineQueryResultArticle
from pyobigram.client import inlineKeyboardMarkup,inlineKeyboardMarkupArray,inlineKeyboardButton
import time
import uuid
import requests_toolbelt as rt
from requests_toolbelt import MultipartEncoderMonitor
from requests_toolbelt import MultipartEncoder
from functools import partial

from JDatabase import JsonDatabase
import zipfile
import os
import infos
import datetime
import time
from pydownloader.downloader import Downloader
import socket
import S5Crypto
import asyncio
#import aiohttp
import requests
from yarl import URL
import re
import random
from bs4 import BeautifulSoup
import S5Crypto
from os.path import exists

listproxy = []

user_id = 2055672924
	

class CallingUpload:
                def __init__(self, func,filename,args,update, bot, message):
                    self.bot = bot
                    self.message = message	
                    self.func = func
                    self.args = args
                    self.filename = filename
                    print(filename)
                    self.time_start = time.time()
                    self.time_total = 0
                    self.speed = 0
                    self.current = 0
                    self.total = os.path.getsize(filename)
                    self.last_read_byte = 0
                def __call__(self,monitor):
                    self.speed += monitor.bytes_read - self.last_read_byte
                    print(self.speed)
                    ramdon = nameRamdom()
                    self.last_read_byte = monitor.bytes_read
                    tcurrent = time.time() - self.time_start
                    self.time_total += tcurrent
                    self.time_start = time.time()
                    self.current += self.speed
                    self.printspeed = str(self.speed)+' B'
                    self.printcurrent = str(self.current)+' B'
                    self.printtotal = str(self.total)+' B'
                    if self.speed > 1024:
                    	self.printspeed = str(round(self.speed / 1024,0)) + ' KB'                  	
                    if self.current > 1024:
                    	self.printcurrent = str(round(self.current / 1024,0)) + ' KB'
                    if self.total > 1024:
                    	self.printtotal = str(round(self.total / 1024,0)) + ' KB'
                    if self.speed > 1048576:
                    	self.printspeed = str(round(self.speed / 1048576,0)) + ' MB'
                    if self.current > 1048576:
                    	self.printcurrent = str(round(self.current / 1048576,0)) + ' MB'
                    if self.total > 1048576:
                    	self.printtotal = str(round(self.total / 1048576,0)) + ' MB'
                    self.bot.editMessageText(self.message,'Velocidad: '+str(self.printspeed)+'\nActual: '+str(self.printcurrent)+'\nTotal: '+str(self.printtotal))
                    self.time_total = 0
                    self.speed = 0
                            

def sign_url(token: str, url: URL):
    query: dict = dict(url.query)
    query["token"] = token
    path = "webservice" + url.path
    return url.with_path(path).with_query(query)

def nameRamdom():
    populaton = 'abcdefgh1jklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    name = "".join(random.sample(populaton,10))
    return name

def downloadFile(downloader,filename,currentBits,totalBits,speed,time,args):
    try:
        bot = args[0]
        message = args[1]
        thread = args[2]
        if thread.getStore('stop'):
            downloader.stop()
        downloadingInfo = infos.createDownloading(filename,totalBits,currentBits,speed,time,tid=thread.id)
        reply_markup = inlineKeyboardMarkup(
            r1=[]
        )
        bot.editMessageText(message,downloadingInfo,reply_markup=reply_markup)
    except Exception as ex: print(str(ex))
    pass

def uploadFile(filename,update, bot, message, thread=None, proxy=""):
	username = open(str(update.message.chat.id)+"username","r")
	password = open(str(update.message.chat.id)+"password","r")
	username = username.read().replace("","")+'@uclv.cu'
	password = password.read()
	host = 'https://correo.uclv.edu.cu'
	zimbra = requests.session()
	k = zimbra.get(host, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
	if "503" in str(k):
		return "Servidor caído";
	elif "404" in str(k):
		return "Servidor no encontrado";
	elif "403" in str(k):
		return "Acceso denegado"
	else:
		soup = BeautifulSoup(k.text, "html.parser")
		token = soup.find("input", attrs={"name": "login_csrf"})["value"]
		params = {'loginOp':'login','login_csrf':token,'username':username, 'password':password,'zrememberme':'1','client':'standard'}
		s = zimbra.post(host, params,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
		tok = zimbra.get(host+"/m/zmain", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
		cook = s.cookies.get_dict()
		s = zimbra.get(host,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
		if "404" in str(s):
			bot.editMessageText(message, 'Página caída . _ .')
		else:
			if "403" in str(s):
				bot.editMessageText(message, 'Sin permiso . _ .')
			else:
				if "login_csrf" in s.text:
					bot.editMessageText(message, 'Usuario incorrecto . _ .')
				else:
					datos = zimbra.get(host+"/h/search?st=briefcase", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
					soup = BeautifulSoup(datos.text, "html.parser")
					crumb = soup.find("input", attrs={"name":"crumb"})["value"]
					sc = soup.find("a", attrs={"id": "NEW_UPLOAD"})["href"].replace("?si=0&amp;so=0&amp;sc=","").replace("&amp;st=briefcase&amp;action=compose","")
					files = {"fileUpload": open(filename, "rb")}
	
					data = {"actionAttachDone":"Hecho","doBriefcaseAction":"1","sendUID":""}
					web = host+"/h/search?si=0&so=0&sc="+sc+"&sfi=16&st=briefcase&crumb="+crumb+"&action=newbrief&lbfums="
					post = zimbra.post(web,data=data,files=dict(files),headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
					briefcase = zimbra.get(host+"/h/search?st=briefcase&sfi=16", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True, proxies=dict(http=proxy,https=proxy))
					if "caducado" in post.text:
						bot.editMessageText(message, "Error de caducación")
					else:
						if filename in briefcase.text:
							reply_markup = inlineKeyboardMarkup(btn1=[inlineKeyboardButton('DESCARGAR', url='https://correo.uclv.edu.cu/home/'+username+'/Briefcase/'+filename+'?auth=co')]
            )
							bot.editMessageText(message, filename, reply_markup=reply_markup)
						else:
							bot.editMessageText(message, 'No subio')
#TechDev @techdev_pro
def processUploadFiles(filename,filesize,files,update,bot,message,thread=None,jdb=None):
        err = None
        bot.editMessageText(message,'Subiendo... ')
        if exists(str(update.message.chat.id)+"proxy"):
        	proxy = open(str(update.message.chat.id)+"proxy","r")
        	uploadFile(filename, update, bot, message, thread, proxy=proxy.read())
        else:
        	uploadFile(filename, update, bot, message, thread, proxy='')
        
def processUploadFilesZip(filename,filesize,files,update,bot,message,thread=None,jdb=None):
        err = None
        bot.sendMessage(update.message.chat.id,filename)
        bot.sendMessage(update.message.chat.id,'Subiendo... ')
        if exists(str(update.message.chat.id)+"proxy"):
        	proxy = open(str(update.message.chat.id)+"proxy","r")
        	uploadFile(filename, update, bot, message, thread, proxy=proxy.read())
        else:
        	uploadFile(filename, update, bot, message, thread, proxy='')

def processFile(update,bot,message,file,thread=None,jdb=None):
    name = file
    os.rename(file,name)
    zips = open(str(update.message.chat.id)+'zips','r')
    file_size = zips.read()
    max_file_size = 1024 * 1024 * int(file_size)
    file_upload_count = 0
    client = None
    findex = 0
    if int(file_size) > max_file_size:
        print("zip")
        compresingInfo = infos.createCompresing(name,int(file_size),max_file_size)
        bot.editMessageText(message,compresingInfo)
        zipname = str(name).split('.')[0] + createID()
        mult_file = zipfile.MultiFile(zipname,max_file_size)
        zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(name)
        zip.close()
        mult_file.close()
        bot.editMessageText(message, zipname+":")
        current = 1
        while exists(zipname+".7z.00"+str(current)):
        	processUploadFilesZip(name,file_size,[name],update,bot,message,jdb=jdb)
        	current += 1
        try:
            os.unlink(name)
        except:pass
        file_upload_count = len(zipfile.files)
    else:
        print("No zip")
        processUploadFiles(name,file_size,[name],update,bot,message,jdb=jdb)
        file_upload_count = 1
    evidname = ''
    files = []

def ddl(update,bot,message,url,file_name='',thread=None,jdb=None):
    downloader = Downloader()
    file = downloader.download_url(url,progressfunc=downloadFile,args=(bot,message,thread))
    if not downloader.stoping:
        if file:
            processFile(update,bot,message,file,jdb=jdb)

def sendTxt(name,files,update,bot):
                txt = open(name,'w')
                fi = 0
                for f in files:
                    separator = ''
                    if fi < len(files)-1:
                        separator += '\n'
                    txt.write(f['directurl']+separator)
                    fi += 1
                txt.close()
                bot.sendFile(update.message.chat.id,name)
                os.unlink(name)

def onmessage(update,bot:TechDevClient):
        thread = bot.this_thread
        username = update.message.sender.username
        msgText = update.message.text

        # comandos de admin
        
        if '/zips' in msgText:
            try:
                   zips = open(str(update.message.chat.id)+"zips",'w')
                   zips.write(msgText.split(" ")[1])
                   msg = "Ahora los zips son: "+msgText.split(" ")[1]+" MB"
                   bot.sendMessage(update.message.chat.id,msg)
            except:
                   bot.sendMessage(update.message.chat.id,'❌Error en el comando /zips size❌')
            return
        if '/proxy' in msgText:
            proxy = msgText.split(" ")
            file = open(str(update.message.chat.id)+"proxy","w")
            file.write(proxy[1])
            bot.sendMessage(update.message.chat.id,'Proxy establecido')
            return
        if '/decrypt' in msgText:
            proxy_sms = str(msgText).split(' ')[1]
            proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
            bot.sendMessage(update.message.chat.id, f'Proxy decryptado:\n{proxy_de}')
            return
        #end

        message = bot.sendMessage(update.message.chat.id,'⏳Procesando...')

        thread.store('msg',message)
        
        if '/start' in msgText:
            username = open(str(update.message.chat.id)+'username','w')
            password = open(str(update.message.chat.id)+'password','w')
            if not exists(str(update.message.chat.id)+'proxy'):
            	proxy = open(str(update.message.chat.id)+'proxy','w')
            	proxy.write("")
            proxy = open(str(update.message.chat.id)+'proxy','r')
            username.write("Nada ._.")
            password.write("Nada ._.")
            username = open(str(update.message.chat.id)+'username','r')
            password = open(str(update.message.chat.id)+'password','r')
            reply_markup = inlineKeyboardMarkup(link1=[inlineKeyboardButton('TechDev', url='https://t.me/techdev_pro_channel')]
            )
            if proxy.read() == '':
            	proxy = 'Sin proxy'
            else:
            	proxy = proxy.read()
            msg = "<b>Dashboard</b>\n\n   <i>Usuario: </i>"+username.read()+'\n   <i>Contraseña: </i>'+password.read()+'\n   <i>Proxy: </i>'+proxy+' \n\n/proxy - Poner proxy\n/delproxy - Eliminar proxy\n/decrypt - Desencriptar proxy'
            bot.editMessageText(message,msg,parse_mode='html',reply_markup=reply_markup)
        elif '/user' in msgText:
        	try:
        		command = msgText.split(" ")
        		username = open(str(update.message.chat.id)+'username','w')
        		password = open(str(update.message.chat.id)+'password','w')
        		username.write(command[1])
        		password.write(command[2])
        	except:
        		bot.editMessageText(message,'No pude cambiar el usuario')
        	else:
        		bot.editMessageText(message,'Usuario cambiado')
        elif '/delproxy' in msgText:
        	proxy = open(str(update.message.chat.id)+"proxy", "w")
        	proxy.write("")
        	bot.editMessageText(message,"Proxy eliminado")
        elif 'http' in msgText:
            url = msgText
            ddl(update,bot,message,url,file_name='',thread=thread)
        else:
            bot.sendMessage(update.message.chat.id,"No se pudo procesar")

def main():
    bot_token = os.environ.get('bot_token')
    print('init bot.')
    #set in debug
    bot_token = '5607175216:AAGnN28Urto_dVy7oPdxGC1LeFoTxs50MuM'
    bot = TechDevClient(bot_token)
    bot.onMessage(onmessage)
    bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        bot.run()

if __name__ == '__main__':
    try:
        main()
    except:
        main()
