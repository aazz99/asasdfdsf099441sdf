import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from time import sleep
from json import dumps, loads
from random import randint
import re
from re import findall
from Api_DataTime import ___date____time
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
import arabic_reshaper
from bidi.algorithm import get_display
from random import choice,randint
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from difflib import SequenceMatcher

from api_rubika import Bot,encryption

green = '\033[32m' 
red = '\033[31m' 
blue = '\033[36m' 
pink = '\033[35m' 
yellow = '\033[93m' 
darkblue = '\033[34m' 
white = '\033[00m'

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], guid)
                    bot.sendMessage(chat['object_guid'], 'کاربر حذف شد @User_Coder 👺' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def get_jok(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        
        
        return False

def get_hagh(text,chat,bot):
    try:                        
        jd = requests.get('http://haji-api.ir/angizeshi/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        
        
        return False

def info_AmoBot(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False
        
def phoshe(text,chat,bot):
    try:
        res = requests.get('https://cdn01.zoomit.ir/2021/8/tortoise.jpg?w=700')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def photo_random(text,chat,bot):
    try:
        res = requests.get('http://haji-api.ir/photography/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz random api bug')
        return False
        
def photo_time(text,chat,bot):
    try:
        res = requests.get('https://haji-api.ir/phototime/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended photo_time')                       
        return True
    except:
        print('code bz random api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            bot.banGroupMember(chat['object_guid'], [chat['last_message']['message_id']])
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.banGroupMember(chat['object_guid'], guid)
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ping/?url=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ping/?url=' + city).text)
            #text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], jd , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_gold(text,chat,bot):
    try:
        site = text[7:-1]
        r = json.loads(requests.get('https://api.codebazan.ir/ping/?url=' + site).text)
        bot.sendMessage(chat['object_guid'], r , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_deghat(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/deghat').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz deghat err')
    return True

def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_khabar(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/khabar/?kind=iran').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khabar err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
    return True

def get_sebt(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/monasebat/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz sebt err')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True

def get_gang(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/gang').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz gang err')
    return True

def get_zeikr(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/zekr').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zekr err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_qzal(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/ghazalsaadi/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz qazal err')
    return True

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        group = chat['abs_object']['title']
        date = ___date____time.historyIran()
        time = ___date____time.hourIran()
        send_text = '❌یک کاربر در تاریخ:\n' + date + '\n' + time + '\n از گروه  ' + group + ' لفت داد ❌\n @User_Coder | کانال رسمی عموبات'   
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        date = ___date____time.historyIran()
        time = ___date____time.hourIran()
        send_text = '✅یک کاربر در تاریخ:\n' + date + '\n' + time + '\n به گروه  ' + group + ' پیوست ✅\n @User_Coder | کانال رسمی عموبات'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], '🔴 راهـنـمای DiGiBoT - ver 1.2.2\n\n📜 لیست ابزارهای ربات:\n/Commands \n\n💬 سرویس موتور جستجو:\n/search ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌\n\n⚠ قوانین ربات:\n/Rules \n\n⚙ گروه های فعال :\n/Group \n\n🔸 فعال کردن سرویس بازی :\n/Sargarmi ‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍\n\n🔹- user support @User_Coder 👺', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_grat(text,chat,bot):                                
    text = open('byb.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], ""'🔷 نتایج کامل به پیوی شما ارسال گردید 🔷'"", chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_listone(text,chat,bot):                                
    text = open('grat1.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_listtwo(text,chat,bot):                                
    text = open('grat2.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def get_car(text,chat,bot):                                
    text = open('Sargarmi.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('sar guid sended')
    
def get_sargarmi(text,chat,bot):                                
    text = open('car.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('sar guid sended')
    
def get_srch(text,chat,bot):                                
    text = open('srch.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
       # bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('srch guid sended')
    
    #کاربردی
def gets_karborde(text,chat,bot):                                
    text = open('karborde.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('karborde guid sended')
    
    #کاربردی

def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '/usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                t8 = str(random.choice(f2[shabih_tarin2]))
                jj = hasInsult(t8)
                if jj[0] != True:
                    bot.sendMessage(chat['object_guid'], t8, chat['last_message']['message_id'])
            t = True
        except:
            print('test error new server or code')

def code_run(text,chat,bot,lang_id):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                h = {
                    "Origin":"https://sourcesara.com",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                }
                p = requests.post('https://sourcesara.com/tryit_codes/runner.php',{'LanguageChoiceWrapper':lang_id,'Program':txt_xt},headers=h)
                p = p.json()
                jj = hasInsult(p['Result'])
                jj2 = hasInsult(p['Errors'])
                time_run = p['Stats'].split(',')[0].split(':')[1].strip()
                if jj[0] != True and jj2[0] != True:
                    if p['Errors'] != None:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\nپاسخ بیش از حد تصور بزرگ است' , chat['last_message']['message_id'])
                    else:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\nپاسخ بیش از حد تصور بزرگ است', chat['last_message']['message_id'])
    except:
        print('server code runer err')
#توکن
#Token
g_usvl = ''
test_usvl = ''
auths = open('DiGiBotAuth.txt','r').read().split('\n')
auth = auths[0]
bot = Bot(auth)
list_message_seened = []
time_reset = math.floor(datetime.datetime.today().timestamp()) + 350
while True:
    try:
        chats_list:list = bot.get_updates_all_chats()
        AmoBotAdmins = open('AmoBotAdmins.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == '!start' or text == '!Start' or text == 'start' or text == 'Start' or text == '!استارت' or text == 'استارت' or text == '/on' or text == '!on' or text == '!On' or text == '!ON' or text == 'روشن' or text == '/start' or text == '/Start':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام به دیجی بات خوش اومدی 👋🏼\n' + '\n' + 'برای دریافت فهرست دستورات ربات\n' + '\n' ' /help ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍ \n' + 'را بفرستید.\n' + '\n' + '🔹- user ad Bot @User_Coder 👹',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
#Start-Texts
                            if text == 'گروه' or text == '/Group' or text == '/group':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹لینکهایی که تاکنون ثبت شده‌اند🔹\n' + '\n' + ' https://rubika.ir/joing/CHGEDEHB0AONEJASLTHSCNMUKPUPPFZX \n' + '\n' + '🔹جهت خرید ربات به ایدی زیر مراجعه کنید.\nuser ad Bot @User_Coder 👹',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'اصل' or text == 'اصل بده':
                                
                                try:
                                    emoji = ["❤️","👽","🐣","🐋","🦕","🌱","🌿","☘️","🍃","🌚","🌻","🌼","💫","🐸","🌾","💐","🌷","🌹","🪷","🌸","🌺","🍂","🍁","🌵","🌳","🌴","🌲","🐉","🌊","🐢","🤖","👻","🤡","😻","😺",]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], 'دیجی بات هستم :)' + renn + '',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'دا' or text == 'داداش' or text == 'داوش' or text == 'داپش' or text == 'داش':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جونم حاجی؟👀👑',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                                   
                            if text.startswith('هکرم') or text.startswith('هکر') or text.startswith('هک') or text.startswith('هککر') or text.startswith('حکر'):
                                
                                try:
                                    emoji = ["🗿","👽","👺","😰","🤣","🤖",]
                                    emj= choice(emoji)
                                    rew = [f"تـرو خـدا هـکـم نـکـن {emj} .",f"هـاکـر روبـیــکا{emj} .",f"بــا گــوشــی؟{emj}",]
                                    renn= choice(rew)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/listone' or text == '!listone':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                
113🍓چه کسی توی این جمع از همه خوشگلتره؟

114🍓یکی از فانتزی‌هات رو تعریف کن؟

115🍓یک ویژگی بد از خودت بگو؟‌

116🍓اگر دوست‌دخترت از دوست صمیمیت متنفر باشه، چکار می‌کنی؟

117🍓تا به حال مواد مخدر مصرف کردی؟

118🍓تا به حال کسی پیشنهاد دوستی تو رو رد کرده؟

119🍓تا به حال از دوستِ دوست‌دخترت خوشت اومده؟

120🍓مرد یا زن رویا‌های تو چه شکلیه؟

121🍓جذابترین آدم توی این اتاق از نظر تو کیه؟

122🍓به نظرت مخاطب خاص تو، کیس ازدواج هست؟

123🍓تا حالا شده به همسرت دروغ بگی تا از نزدیک شدن بهش اجتناب کنی؟

124🍓دوست داری چه چیزی در مورد مخاطب خاصت تغییر کنه؟

125🍓چه کسی رو پنهانی دوست داری؟

126🍓تا به حال به همسرت / مخاطب خاصت خیانت کردی؟

127🍓اصلی‌ترین چیزی که توی جنس مقابل برای تو جذابه چیه؟

128🍓معیارهات برای ورود به یک رابطه چی هستن؟

129🍓در مورد اولین تجربه‌ی عاشقانه‌ ات بگو ؟

130🍓یه قسمت خنده‌دار از اولین تجربه‌ی پرحرارت زندگیت رو تعریف کن؟

131🍓بدترین ویژگی بغل دستیت چیه؟

132🍓بدترین قرارت با یه پسر چطوری بوده؟

133🍓تا به حال از دوست‌پسر یا دوست‌دختر دوستت خوشت اومده؟

134🍓تا به حال شده پسری که دوستش داری بفهمه، و بهت جواب منفی بده؟

135🍓برای اینکه جذاب به نظر برسی چه کار می‌کنی؟

136🍓در حال حاضر از کی خوشت میاد؟

137🍓اگر می‌تونستی یک چیز در بدنت رو تغییر بدی اون چی بود؟

138🍓به کی حسودی می‌کنی؟

پنج پسر اولی که به نظرت جذابن رو نام ببر؟

139🍓اگر می‌تونستی نامرئی بشی چکار می‌کرد؟

140🍓جذابترین دختران کلاس (جمع یا مدرسه) کدامند؟

141🍓دختر ایده‌آلت چه ویژگی‌هایی داره؟

142🍓تا به حال عاشق شدی؟

143🍓چه رفتاری برای تو بیشتر از همه جذاب است؟

144🍓به کی حسودی می‌کنی؟

145🍓تا به حال به پارتنرت دروغ گفتی؟ چه دروغی؟

146🍓معیارهاتو از فرد رویاهات بگو

147🍓هیجان‌ انگیزترین چیز برای تو چیه؟

148🍓با کدوم دوستت می‌خوای به یک دانشگاه بری؟

149🍓آخرین باری که خودتو خیس کردی کی بوده؟

150🍓آخرین کار غیرقانونی که انجام دادی چی بوده؟

151🍓اگر هرچیزی که می‌خواستی رو می‌تونستی بخری، چی می‌خریدی؟

152🍓اسم کسی که توی این جمع خیلی خیلی دوسش داری چیه ؟

153🍓زیباترین خاطرت با کیه ؟

154🍓پنج خصوصیت ویژه ای که رابطه زناشویی تو باید داشته باشه رو نام ببر

155🍓به شریکت بگو که چه ویژگی هایی رو در اون دوست داری

156🍓سخترین و تلخ ترین لحظات زندگیت با عشقت و بازگو کن .

157🍓در چه مورد دوست نداری کسی با عشقت شوخی کنه ؟

158🍓اولین برداشت تو از عشقت چه بوده؟

159🍓بهترین ویژگی‌ فیزیکی عشقت چیست؟

160🍓شیطنت و بازی کردن در رخت خواب را دوست داری ؟

🔹- user support @User_Coder 👺
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'دختری؟' or text == 'سلام دختری؟' or text == 'دختر':
                                
                                try:
                                    emoji = ["🗿","👽","👺","👻",]
                                    emj= choice(emoji)
                                    rew = [f"فـاز دخـتـر بـازی ؟ {emj}",f"از دخـتـرا بدم میاد {emj} .","دخـتـر بازی تو مـجـازی؟🤣",]
                                    renn= choice(rew)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('چ خبر') or text == ('چخبر') or text == ('چه خبر') or text == ('چه خبرا') or text == ('چخبرا؟') or text == ('چخبر؟') or text == ('چ خبرا'):
                                
                                try:
                                    emoji = ["❤️","👽","🐣","🐋","🦕","🌱","🌿","☘️","🍃","🌚","🌻","🌼","💫","🐸","🌾","💐","🌷","🌹","🪷","🌸","🌺","🍂","🍁","🌵","🌳","🌴","🌲","🐉","🌊","🐢","🤖","👻","🤡","😻","😺",]
                                    emj= choice(emoji)
                                    rando = [f"سـلامتــی .{emj}","سلامـتـیـت تـو چـخـبـر ؟ .","خـبـری نـی .","خــبـرارو تـو بایـد بـگـی"]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('شوخش') or text == ('شوبخیر') or text == ('شب بخیر') or text == ('شب خوش') or text == ('شبت خوش') or text == ('شو خش') or text == ('شو بخیر'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=شب%20بخیر').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('صو بخیر') or text == ('صب بخیر') or text == ('صوبخیر') or text == ('صبحتون بخیر') or text == ('صبحت  بخیر') or text == ('صبح همگی بخیر') or text == ('صبح مه گی بخیر'):
                                
                                try:
                                    rando = ["صو شده؟","بـنـازم سحر خیز شدی ؟ 👹 .","گود مورنینگ 😂 .","صـبـح بـخیـر سـحر خـیز گـپ .","صبح بخیر جون دل ."]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('چطوری') or text == ('چطوری؟') or text == ('چطوری تو') or text == ('چطوری تو؟') or text == ('حالت چطوره؟') or text == ('حالت چطوره'):
                                
                                try:
                                    rando = ["خوب نیستم","خـوبـم مـرسـی 😺 .","مـرسـی خـوبـم تـو خـوبـی؟🌝🫶🏻","تـو خـوبـی ؟"]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith('عه') or text.startswith('عه؟') or text.startswith('عه😐') or text.startswith('عه؟😐😂') or text.startswith('عه😂') or text.startswith('عه😂😐'):
                                
                                try:
                                    rando = ["والـا😐 .","آره نـامـوسـا🫤 .","هاره !😼","نه ."]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('آها') or text == ('اها') or text == ('عاها'):
                                
                                try:
                                    rando = ["خـوبـه فـهـمیدی .","چـه عـجـب فـهـمـیـدی .","انـتـظاری نـداشتـم از مـغـز کـوچـیـکـت ."]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith('😕') or text.startswith('😕😕') or text.startswith('💔') or text.startswith('😿') or text.startswith('🚶‍♂️') or text.startswith('👨‍🦯') or text.startswith('👩‍🦯') or text.startswith('🚶') or text.startswith('🚶‍♀️'):
                                
                                try:
                                    emoji = ["🗿","👽","👺","👻",]
                                    emj= choice(emoji)
                                    rando = [f"حـاجـی نـاراحـت نـباش زنـدگـی گـذراسـت . {emj}","چـی شـدی؟😿 .","نـشکـن حـاجـی .🫶🏻","فـاز دپ؟","فـاز دارک؟","فـاز قـم؟","فاز نـگـیر ."]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '🗿' or text == '🗿🗿' or text == '🗿🗿🗿' or text == '🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿🗿':
                                
                                try:
                                    rando = ["سـیـد فـاز کـاکـا سـنگـی؟","کـاکـا سنـگی؟","کاکا سنگی با سیگار؟🗿",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'رلپی' or text == 'رل پی' or text == 'رل میخام' or text == 'برلیم؟' or text == 'برلیم' or text == 'عاشقتم' or text == 'عشقم' or text == 'عشقمی' or text == 'دوست دارم':
                                
                                try:
                                    rando = ["حاجی بجای اینکه تو مجازی رل بزنی برو حضوری رل بزن بی اُرزه😂🙁","رل مـجازی؟😂","دوره مجازی گذشت حاجی .","مجازی؟🗿",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], rando,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '😐😂' or text == '😂😐' or text == '😐🤣' or text == '🤣😐' or text == '😐😹' or text == '😹😐' or text == '😐😂🤣' or text == '🙂' or text == '🙃' or text == '😸':
                                
                                try:
                                    rando = ["تو فقد بخند 🤤 .","جوون میخنده .","خنده مَکونی ؟","خنده میکونی چون کش؟",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'وایجر' or text == 'وای جر' or text == 'جر' or text == 'وایجر😂' or text == 'وایجر😐😂' or text == 'جر😐😂' or text == 'جر😂😐' or text == 'جرر' or text == 'جر😂' or text == 'جر😐' or text == 'جر🤣':
                                
                                try:
                                    rando = ["شت جـ‍‌ر خورد که !😂 .","کجات پاره شد؟🙀 .","جـ‍‌ر خوردی؟ 😧","پـارگی هم حدی داره .",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'ایجان' or text == 'ای جان' or text == 'عیجان' or text == 'عی جان':
                                
                                try:
                                    rando = ["کم نیاری حاجی ! .","ترسیدی کم بیاری؟ .","کم نیاری ی وقت ! .",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'چی' or text == 'چی؟' or text == 'چ میگی' or text == 'چیمیگی' or text == 'چمیگی' or text == 'چ':
                                
                                try:
                                    rando = ["تـو نمیفهمی .","هـیـچـی حاجی .","بدرد تـو نـمـیخوره .","ب مغزت فـشـار نیار .","فهمیدنش لزومی نداره .",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'هن' or text == 'ها؟' or text == 'هان؟' or text == 'هان' or text == 'ها' or text == 'هن؟':
                                
                                try:
                                    rando = ["ها و کـ‍‌یــ‍‌ر خر .","مدرسه گذاشتن واسه پدرت؟","بلد نیستی چت کنی؟","بلد نیستی مث آدم بگی جون؟ , میگی ها؟",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'مشخصات' or text == 'اطلاعات':
                                
                                try:
                                    emoji = ["❤️","👽","🐣","🐋","🦕","🌱","🌿","☘️","🍃","🌚","🌻","🌼","💫","🐸","🌾","💐","🌷","🌹","🪷","🌸","🌺","🍂","🍁","🌵","🌳","🌴","🌲","🐉","🌊","🐢","🤖","👻","🤡","😻","😺",]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], '@User_Coder ' + renn + '' ,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'آفرین' or text == 'افرین' or text == 'آفری' or text == 'افری' or text == 'ن خشم اومد' or text == 'خوشم میاد ازش' or text == 'ن خوشم اومد':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'کیف میخوای؟👜',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'خب' :
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خب ب جمالت',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'فقر' or text == 'فقیرم':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حاجی ایران همینه😔',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '[سرگرمی ها]' or text == '[سرگرمی]' or text == 'سرگرمی' or text == '!sargarmi' or text == '/Sargarmi' or text == 'سرگرمی ها':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                🔴 به منوی سرگرمی دیجی بات خوش آمدید.

🔹 لیست بازی جرعت حقیقت .
/jrat 

🔹 لیست سرگرمی بیو ، جوک و...
/Tools 

🔹- user support @User_Coder 👺
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '🏳️‍🌈' or text == '💜💜':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پرچم سفید؟👺',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'ریستارت' or text == 'ری استارت' or text == '/restart':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'LodinG...',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'LodinG...' or text == 'لودینگ':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ReStartinG...✅️',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'نه' or text == 'ن' or text == 'No' or text == 'no' or text == 'نع' or text == 'نح':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'دقیقا چرا نه؟ 🌝',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '‌' or text == '‌‌' or text == '‌‌‌':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'پیام خالی؟😱 \n الان هاک میشیم .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '♥️' or text == '💜' or text == '❤️' or text == '❣️' or text == '💘':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حاجی ایموجی قلب دیدم؟ 🤖 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('اره') or text == ('آره') or text == ('آرع') or text == ('ارع') or text == ('آرح') or text == ('ارح') or text == ('رح') or text == ('رع'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=آره').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('کی') or text == ('کی؟') or text == ('کی!؟') or text == ('کی!'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=کی').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('ریدم') or text == ('ریدوم'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=ریدم').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'سلام دا' or text == 'سلام داش' or text == 'سلام داداش':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام حاجی حالت چطوره؟🦖 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1') 
                            if text == 'جالب' or text == 'گانگ' or text == 'گنگ' or text == 'جذاب':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'گانگستر🗿🔥',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'کص میگی' or text == 'کصمیگی' or text == 'کسمیگی' or text == 'کس میگی':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره حاجی ملت علاف توعن بشینی کـ‍‌س بگی😐🚶🏻‍♂',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')   
                            if text == 'رباتی؟' or text == 'رباتی':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره حاجی رباتم آدم نیستم که 😟 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/listtwo' or text == '!listtwo':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                ۱🔓عاشق شدی؟اسمش❤️
۲🔓رل زدی تاحالا؟اسمش
۳🔓کراش داری؟اسمش
۴🔓چند بار تا الان رابطه جنسی داشتی؟با کی😐💦
۵🔓از کی خوشت میاد؟
۶🔓از کی بدت میاد؟
۷🔓منو دوس داری؟بهم ثابت کن
۸🔓کی دلتو شکونده؟
۹🔓دل کیو شکوندی؟
۱۰🔓وقتی عصبانی هستی چجوری میشی؟
۱۱🔓دوس داری کیو بزنی یا بکشی؟
۱۲🔓دوس داری کیو بوس کنی؟😉💋
۱۳🔓از تو گالریت عکس بده
۱۴🔓از مخاطبینت عکس بده
۱۵🔓از صفحه چت روبیکات عکس بده
۱۶🔓لباس زیرت چه رنگیه؟🙊
۱۷🔓از وسایل آرایشت عکس بده
۱۸🔓از لباسای کمدت عکس بده
۱۹🔓از کفشات عکس بده
۲۰🔓تالا بهت تجاوز شده؟😥
۲۱🔓تاحالا مجبور شدی به زور به کسی بگی دوست دارم؟
۲۲🔓تاحالا یه دخترو بردی خونتون؟
۲۳🔓تاحالا یه پسرو بردی خونتون؟
۲۴🔓با کی ل....ب گرفتی؟😜
۲۵🔓خود ار.ض..ای..ی کردی؟😬💦
۲۶🔓خانوادت یا رفیقت یا عشقت؟
۲۷🔓سلامتی یا علم یا پول؟
۲۸🔓شهوتی شدی تاحالا؟😂
۲۹🔓خونتون کجاس؟
۳۰🔓خاستگار داری؟عکسش یا اسمش
۳۱🔓به کی اعتماد داری؟
۳۲🔓تاحالا با کسی رفتی تو خونه خالی؟
۳۳🔓چاقی یا لاغر؟
۳۴🔓قد بلندی یا کوتاه؟
۳۵🔓رنگ چشمت؟
۳۶🔓رنگ موهات؟
۳۷🔓موهات فرفریه یا صاف و تا کجاته؟
۳۸🔓تاریخ تولدت؟
۳۹🔓تاریخ تولد عشقت؟
۴۰🔓عشقت چجوری باهات رفتار میکنه؟
۴۱🔓با دوس پسرت عشق بازی کردی؟🤤
۴۲🔓پیش عشقت خوابیدی؟
۴۳🔓عشقتو بغل کردی؟
۴۴🔓حاضری ۱۰ سال از عمرتو بدی به عشقت؟
۴۵🔓مامان و بابات چقد دوست دارن؟
۴۶🔓دعوا کردی؟
۴۸🔓چند بار کتک زدی؟
۴۹🔓چند بار کتک خوردی؟
۵۰🔓تاحالا تورو دزدیدن؟
۵۱🔓تاحالا کسی ل..خ....ت تورو دیده؟🤭
۵۲🔓تاحالا ل...خ...ت کسیا دیدی؟
۵۳🔓دست نام....حرم بهت خورده؟
۵۴🔓دلت برا کی تنگ شده؟
۵۵🔓دوس داشتی کجا بودی؟
۵۶🔓به خودکشی فکر کردی؟
۵۷🔓عکستو بده
۵۸🔓ممه هات بزرگ شدن؟🙈
۵۹🔓با دیدن بدن خودت ح...ش....ری میشی؟
۶۰🔓پیش کسی ضایع شدی؟
۶۱🔓از مدرسه فرار کردی؟
۶۲🔓میخوای چند سالگی ازدواج کنی؟
۶۳🔓اگه مامان و بابات اجازه ندن با عشقت ازدواج کنی چیکار میکنی؟
۶۴🔓چند سالگی پ....ری....و..د شدی؟😶
۶۵🔓وقتی پریودی چجوری هستی؟
۶۶🔓رنگ مورد علاقت؟
۶۷🔓غذای مورد علاقت؟
۶۸🔓پولدارین یا فقیر؟
۶۹🔓دوس داری با من بری بیرون؟
۷۰🔓منو بوس میکنی؟☺️😚
۷۱🔓منو میکنی؟😬
۷۲🔓س...ک...س چت داشتی؟
۷۳🔓خوشت میاد از س....ک.....س؟
۷۴🔓خجالتی هستی یا پررو؟
۷۵🔓دوس داری بکنمت؟🤤
۷۶🔓تاحالا کسی برات خورده؟😁
۷۷🔓من ببوسمت خوشحال میشی؟
۷۸🔓خفن ترین کاری که تا الان کردی؟
۷۹🔓آرزوت چیه؟
۸۰🔓سیگار یا قلیون میکشی؟
۸۱🔓منو میبری خونتون؟
۸۲🔓میذاری بیام خونتون؟
۸۳🔓تاحالا شکست عشقی خوردی؟💔
۸۴🔓اگه به زور شوهرت بدن تو چیکار میکنی؟
۸۵🔓اگه به زور زنت بدن تو چیکار میکنی؟
۸۶🔓تاحالا با پسر غریبه خوابیدی؟
۸۷🔓تاحالا با دختر غریبه خوابیدی؟
۸۸🔓با همجنست خوابیدی؟
۸۹🔓مدرسه یا گوشی؟
۹۰🔓سر کار میری؟
۹۱🔓کلن اخلاقت چجوریه؟
۹۲🔓هنوز پرده داری؟😐
۹۳🔓قلقلکی هستی؟
۹۴🔓سکس خشن دوس داری یا ملایم؟
۹۵🔓کصکش ناله های دختر مردمو میخوای ببینی😐⚔
۹۶🔓چند بار سوتی میدی؟
۹۷🔓مواظب کصت باش تا بیام بگیرمت باشه؟🤭👍🏻
۹۸🔓تاحالا مچ عشقتو موقع لب بازی با یه دختر دیگه گرفتی؟
۹۹🔓تاحالا مچ عشقتو موقع لب بازی با یه پسر دیگه گرفتی؟
۱۰۰🔓اگه یه نفر مزاحم ناموست بشه باهاش چجوری رفتار میکنی؟
۱۰۱🔓شمارتو بده
۱۰۲🔓چقد آرایش میکنی؟
۱۰۳🔓پسر بازی رو دوس داری؟
۱۰۴🔓دختر بازی رو دوس داری؟
۱۰۵🔓اگه یه کص مفتی گیرت بیاد بازم پسش میزنی؟😁👍🏻
۱۰۶🔓پشمالو دوس داری؟🤧
۱۰۷🔓دوس داری شوهر آیندت چجوری باشه؟
۱۰۸🔓دوس داری زن آیندت چجوری باشه؟
۱۰۹🔓دوس داری چند تا بچه داشته باشی؟
۱۱۰🔓قشنگ ترین اسم پسر بنظرت؟
۱۱۱🔓قشنگ ترین اسم دختر بنظرت؟
۱۱۲🔓من خوشگلم یا زشت؟
۱۱۳🔓خوشگل ترین پسر گپ کیه؟
۱۱۴🔓خوشگل ترین دختر گپ کیه؟
۱۱۵🔓کی صداش از همه زیباتره؟
۱۱۶🔓خانومت خوشگله یا زشته؟
۱۱۷🔓خوشتیپ هستی یا خوش قیافه؟
۱۱۸🔓تاحالا احساس کردی یکی روت کراش زده باشه؟
۱۱۹🔓اگه یکی رو ناراحت ببینی چیکار میکنی؟
۱۲۰🔓بی رحمی یا دلت زود به رحم میاد؟
۱۲۱🔓تاحالا پیش کسی گوزیدی؟
۱۲۲🔓تاحالا خودتو خیس کردی؟
۱۲۳🔓اگه بیدار شی ببینی یکی خوابیده روت واکنشت چیه؟
۱۲۴🔓اگه روی یه صندلی کیک باشه یکیش کیر باشه،رو کدوم میشینی و کدومو میخوری؟
۱۲۵🔓جنسیتتو دوس داری عوض کنی؟
۱۲۶🔓دوس داری بری سربازی؟
۱۲۷🔓عکس یهوی بده؟
۱۲۸🔓شام دعوتت کنم قبول میکنی؟
۱۲۹🔓اگه همین الان بهت بگم دوست دارم واکنشت چیه؟
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('خوبه') or text == ('خوب') or text == ('خبه'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=خوبه').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '😐🚶' or text == '😐🚶‍♀️' or text == '😐🚶🏿‍♀' or text == '😐🚶🏿‍♂' or text == '🚶' or text == '🚶‍♀️':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خب ک چی حاجی ؟',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '؟' or text == '؟؟' or text == '?' or text == '??' or text == '?!' or text == '؟!':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فاز پرسشی برداشتی ؟ 🙁.',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'حقیقت' or text == '/jrat' or text == '/gh' or text == '!GH' or text == 'جرات' or text == 'جرعت' or text == 'جرعت حقیقت' or text == 'ج ح':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                به منوی بازی (جرعت و حقیقت خوش آمدید)

لیست سوالات اول -
/listone 

لیست سوالات دوم -
/listtwo 

🔹- user support @User_Coder 👺
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '!' or text == '!!' or text == '!!!':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عجب🗿',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/tools' or text == '!Tools' or text == '/Tools':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                🎮ســرگـرمی هـا💸


😂📣 جوک: 
/jok 
 
👻خاطره:
/khatere 
 
🤓 جملات معروف
/dialog 
 
😑 جوک الکی مثلا:
/alaki 
 
📿 دانستنی به صورت متن :
/danesh  
 
✏️ جملات سنگین :
/gang 
 
📿 ذکر روزانه :
/zekr 
 
🤔 دقت کردین؟ :
/deghat 
 
🤠 داستان:
/dastan 
 
✏️ بیوگرافی :
/bio 
 
🖼 دانستنی به صورت عکس :
/danpic 

📊 مناسبت های ماه:
/mont 

🔹- تمام دستورات این بخش بصورت فارسی هم کار میکنند مانند (/jok=جوک)

🔹-@User_Coder | کانال رسمی دیجی بات
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'عجب' or text == 'اجب' or text == 'عجب😐😂' or text == 'عجب😂😐' or text == 'عجب😐' or text == 'عجب😂':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'مش رجب🗿🖐🏿',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'رباته؟😐' or text == 'رباته؟' or text == 'رباته؟😐😂' or text == 'رباته😂😐' or text == 'ربات نی' or text == 'ربات نیست':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حاجی رباتم والا 😂 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'شاهرخ' or text == 'شاهی':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اقا شاهرخ|@User_Coder',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/help' or text == 'Help' or text == 'پنل' or text == 'دستورات' or text == '!help':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔴 راهـنـمای DiGiBoT - ver 1.2.2\n\n📜 لیست ابزارهای ربات:\n/Commands \n\n💬 سرویس موتور جستجو:\n/search ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌\n\n⚠ قوانین ربات:\n/Rules \n\n⚙ گروه های فعال :\n/Group \n\n🔸 فعال کردن سرویس بازی :\n/Sargarmi ‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍\n\n🔹- user support @User_Coder 👺', chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'کاربردی' or text == '/Commands' or text == '!commands' or text == 'commands' or text == 'ابزار کاربردی':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                ➕📣موارد کاربــردی دیجی بات:

⏰ساعت دقیق:
/time  = ساعت = تایم
 
⏳ساعت در عکس
/photo_time  = فوتو تایم
 
💹دریافت نرخ ارز:
/arz  = ارز
 
👑دریافت قیمت طلا:
/Golds  = طلا
♻️نیم بها کننده لینک:
/nim  https://....
به جای https لینکتون رو بزارید
 
💱💬ترجمه کننده متن:
/trans  [ln:DiGiBoT]
به جای ln زبان مورد نظر رو بنویسید مثال:
فارسی   fa
انگلیسی   en
و به جای DiGiBoT متنی که میخواید ترجمه بشه
 
💻🌐دریافت پینگ سایت:
/ping  [DiGiBoT]
به جای DiGiBoT ادرس سایت رو بنویسید
 
⌨🖥فونت اسم فارسی:
/font-fa  [DiGiBoT]
به جای دیجی بات کلمه فارسی یا انگلیسی مورد نظر رو بنویسید
 
📟🕹فونت اسم انگلیسی:
/font-en  [DiGiBoT]
به جای دیجی بات کلمه فارسی یا انگلیسی مورد نظر رو بنویسید
 
📡دریافت اطلاعات دامنه:
/whois  [domin]
به جای domin دامنه خودتونو بزارید
 
📠دریافت معنی واژه:
/vaj  [DiGiBoT]
به جای شیبا کلمه فارسی مورد نظر رو بنویسید 
 
🌦هواشناسی شهر مورد نظر:
/hvs  [DiGiBoT]
به جای DiGiBoT شهر خودتون رو بنویسید 

🌪دریافت ای پی ای:
/io  [DiGiBoT]
به جای DiGiBoT مال خودتونو بزارید
 
➗ماشین حساب دقیق:
/math  [3 * 4]=حساب
به جای عدد ها عددای مورد نظرتونو بنویسید
علامت ضرب  *
علامت منها   -
علامت به اضافه   +
علامت تقسیم   /
علامت توان  **
 
📸عکس گرفتن از متن:
/shot  = شات
این کلمه رو روی متنتون ریپلای بزنید
 
🗣🌐⚠️تبدیل متن انگلیسی به ویس:
/Speak  = بگو
این کلمه رو روی متنتون ریپلای بزنید

 -------------------------------------
- دستورات ویژه ادمین ها -

➕✅افزودن عضو به گروه با آیدی:
/add  [@id]
به جای @id آیدی فرد مورد نظر رو بنویسید 
توجه کنید که اون فرد باید از قسمت تنظیمات
حریم خصوصی عضو شدن به گروه و کانال برای 
همه باز باشه و گرنه نمیشه عضوش کرد
 
❌ریم زدن‌افراد از گروه:
/ban  [@id]
به جای @id ایدی فرد رو بزارید
 
❌🤖ریم زدن‌ افراد از طریق ریپلای:
/ban  = بن
را روی فرد ریپلای کنید
 
-------------------------------------

🔹-@User_Coder | کانال رسمی دیجی بات
 
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'چنل' or text == 'پشتیبانی':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹- user support @ID_Coder 👺\n' + '🔹- user ad Bot @User_Coder 👹',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'دیجی' or text == 'دیجی بات' or text == 'بات دیجی' or text == 'دیجیبات' or text == 'دیجی جون' or text == 'دیجی😐😂' or text == 'دیجی😐' or text == 'دیجی😂' or text == 'دیجی😂😐' or text == 'Digi' or text == 'Digi bot' or text == '/Digi' or text == '/DigiBot' or text == 'دیجی بات جونم' or text == 'دیجی بات عشقه':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جونم من فداتم.😍',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'کسمادرت' or text == 'کس مادرت' or text == 'کصمادرت' or text == 'کص مادرت' or text == 'مادر جنده':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فحاشی ممنوع 👺',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'جون' or text == 'جان':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عمو بخوره تورو 🤤 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/Rules' or text == 'قوانین' or text.startswith('[قوانین]'):
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                    📁• قوانین گروه •
📁• فحش و لینک ممنوع 
📁• توهین به کاربران و ادمین ها ممنوع
📁• تبلیغات ممنوع 
📁• دستورات مستهجن به ربات ممنوع
🗑• در صورت مشاهده و زیر پا گذاشتن قوانین فورا شما از گروه حذف میشوید!
=================================
جهت خرید ربات به ایدی زیر مراجعه کنید.
user ad Bot @User_Coder 👹
                                    """,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'عجیبه' or text == 'اجیبه' or text == 'اجیب است' or text == 'عجیب'  or text == 'عجیب است':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'خیلی عجیب 🧐 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('کسی نی؟') or text == ('کسی نی') or text == ('کسی نیست') or text == ('نی کسی') or text == ('نیست کسی؟') or text == ('نیست کسی'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=کسی%20نیست').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'رباتم میشی' or text == 'ربات میخام' or text == 'بات میخام' or text == 'خرید ربات' or text == 'ربات گپم میشی' or text == 'خرید' or text == 'فروشی' or text == 'فروش':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], '- دیجی بات | DiGiBoT -\n' + '\n' + 'مطلب را کامل مطالعه فرمایید\n' + '\n' + 'قیمت پنل یک ماه 100 هزارتون👍\n' + '\n' + 'ابتدا یکی از ادمینای ربات عضو گروهتون میشه ادمینش میکنید در حد افزودن عضو بعدش رباتو واستون اد میزنه و اضافه میکنه به گروهتون و بعدش شارژو واسش ارسال کنید همراه یا ایرانسل فرقی نداره بعدش که ربات در گروهتون اد شد باید ادمین باشه تا بتونه ریم و اد بزنه واستون\n' + '\n' + 'نکته مهم‼️\n' + 'اگه بعد از اد زدن ربات تو گروهتون شارژو ارسال نکنید از طریق همون ادمین ربات از گروهتون لف میده سعی کنید زرنگ بازی در نیارید😂\n' + '\n' + '✅ویژگی ها :\n' + '\n' + 'جوک - فاز سنگین - بیو - اسم شاخ - دانستنی تصویری - دانستنی متنی - داستان - خاطره - نیم بها کننده لینک - محاسبات ریاضی - گوگل! - سرچ از ویکی پدیا - نرخ ارز - نرخ طلا - اطلاعات اکانت - ساعت و تاریخ دقیق - فونت فارسی و انگلیسی - مترجم - اطلاعات آی پی - کلمه و جمله ای رو که میخواین به صورت ویس میگه! 🌹\n' + '\n' + '\n' + '⚓️و سخنگو بودن جواب همه پیاماتونو تو پیوی و گروه میده 🔥\n' + '\n' + '\n' + '🆔آیدی ربات\n' + '🤖 @User_Coder 🤖\n' + '\n' + '🔹برای سفارش با ایدی های زیر در ارتباط باشید\n' + '\n' + '🔹- user ad Bot @User_Coder 👹\n',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'ابوالفضل' or text == 'تکس کدر' or text == 'سازنده' or text == 'سازندت کیه' or text == 'سازندت کیه؟':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سازنده دیجی بات | @ID_Coder',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('سلام'):
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام خوبی؟🌚🍂' , chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('/search') or text == '/Search' or text == 'جستجو':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], """
                                سرچ کامل متنی و سراسری:
/srch  [DiGiBoT]
به جای کلمه DiGiBoT موضوعتونو بنویسید.

سرچ متن در گوگل عنوانها:
/srch-k  [DiGiBoT]
به جای کلمه DiGiBoT موضوعتونو بنویسید.

سرچ عکس در گوگل :
/srch-i  [DiGiBoT]
به جای کلمه DiGiBoT موضوعتونو بنویسید.

    
جستجو در مقاله های ویکی پدیا :
/wiki-s  [DiGiBoT]
        به جای DiGiBoT موضوعتون رو بنویسید تمام مقاله های مرتبط براتون لیست میشه 
    
   آوردن متن مقاله از ویکی پدیا : 
ویکی [page:name]
        به جای page صفحه چندم مقاله رو بزارید مثلا 1 یعنی صفحه اول و به جای name موضوع مقالتون و بعد بفرستید اگر اسم دقیق موضوع مقالتون رو نمیدونید از دستور بعدی جستجو اش کنید

🔹- user support @User_Coder👺
                                """, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('سیلام') or text == ('صلام') or text == ('سل') or text == ('های') or text == ('سالام') or text == ('سلم'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=صلام').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith('کص') or text == ('کس') or text == ('کث'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=کص').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'س' or text == 'ص' or text == 'ث':
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=س').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('خبی') or text == ('خوبی') or text == ('خبی؟') or text == ('خمبی') or text == ('خوبی؟') or text == ('تو خوبی') or text == ('تو خوبی؟'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=خوبی').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '.' or text == '..':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'نت نداری؟😐😂',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'شکر' or text == 'شک':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلامت باشی 😚 .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '😞' or text == '🙁' or text == '😔' or text == '☹' or text == '️😣' or text == '😖' or text == '😫' or text == '😩' or text == '😭' or text == '🤕' or text == '💔' or text == '😓' or text == '😟' or text == '😰' or text == '🤒' or text == '😥' or text == '😢':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اوخی چی شدی؟☹💔',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'نمال' or text == 'بمال' or text == 'کصکش' or text == 'کسکش':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فاحشی ممنوع میباشد ❌',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'کسنگو' or text == 'کس نگو' or text == 'کصنگو' or text == 'کص نگو':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'داش کس نمیگن میکنن کبیر شدی بلف🗿♥️',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('😐') or text == ('😐😐') or text == ('😐😐😐') or text == ('😐😐😐😐'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=😐').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('بای') or text == ('بحی') or text == ('خداحافظ') or text == ('بابای') or text == ('فلن') or text == ('فعلا') or text == ('خدافز') or text == ('خدافظ') or text == ('من برم'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=بای').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'اخی' or text == 'آخی' or text == 'اوخی' or text == 'اوخ':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بچگانه حرف نزن 👹.',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('😂') or text == ('😂😂') or text == ('😂😂😂') or text == ('😂😂😂😂'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=😂').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '🤣' or text == '🤣🤣' or text == '🤣🤣🤣' or text == '🤣🤣🤣🤣' or text == '🤣🤣🤣🤣🤣':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جر نخوری 😐.',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith('ربات') or text.startswith('روبات') or text.startswith('رباط') or text.startswith('روباط') or text.startswith('عموبات') or text.startswith('عمو بات'):
                                
                                try:
                                    rando = ["هـــا؟ چــیـــه ؟😐","جـــون ربـــات؟😺","حـاجـی ولـم کـن نـامـوسـا","ولــم کــن حــاجــی","بــیـکاری؟","بـیـا بـرو","اسـمـتـو هـر دیـقـه بــگـم بـفـهـمی چ حـس خــوبـیه؟😐","کـسـیـو پـیـدا نـکـردی ب مـن بـیـچـاره گـیـر مـیـدی؟😐",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith('باط') or text.startswith('بات') or text.startswith('باتت') or text.startswith('بات'):
                                
                                try:
                                    rando = ["هـــا؟ چــیـــه ؟😐","جـــون ربـــات؟😺","حـاجـی ولـم کـن نـامـوسـا","ولــم کــن حــاجــی","بــیـکاری؟","بـیـا بـرو","اسـمـتـو هـر دیـقـه بــگـم بـفـهـمی چ حـس خــوبـیه؟😐","کـسـیـو پـیـدا نـکـردی ب مـن بـیـچـاره گـیـر مـیـدی؟😐",]
                                    renn= choice(rando)
                                    bot.sendMessage(chat['object_guid'], renn, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('هعب') or text == ('هعی') or text == ('هعیب') or text == ('هیب') or text == ('هب') or text == ('هی') or text == ('هی روزگار'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=هعی').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('چراا') or text == ('چر') or text == ('چرا؟') or text == ('چرااا') or text == ('چررا') or text == ('چرا خو') or text == ('برای چی'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=چرا').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('درد') or text == ('درد 😐') or text == ('درد'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=درد').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('گونخور') or text == ('گوه نخور') or text == ('گه نخور') or text == ('گو نخور'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=گوه').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('وای') or text == ('وایی') or text == ('اوه') or text == ('اوو') or text == ('او'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=وای').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('الاغ') or text == ('الاق') or text == ('خر') or text == ('احمق') or text == ('گاو'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=الاغ').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('گم شو') or text == ('گمشو') or text == ('سیکیتیر') or text == ('سیک') or text == ('گم شو'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=گمشو').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('کانی') or text == ('کونی') or text == ('چونی') or text == ('کونی'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=کونی').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text.startswith ('یص') or text.startswith ('یسس') or text.startswith ('یس'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=یس').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('خش') or text == ('خوش') or text == ('خشم') or text == ('خوشم'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=خوش').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('نمد') or text == ('نم') or text == ('نیمیدونم') or text == ('نمدونم') or text == ('نمیدونم') or text == ('نمیدانم') or text == ('نمودونم') or text == ('نمیدنم') or text == ('نمدنم'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=نمد').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('خدتی') or text == ('خودتی') or text == ('خددتیییی') or text == ('خدت') or text == ('تویی') or text == ('ختی'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=خودتی').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('کجا') or text == ('کوجا') or text == ('کوچا') or text == ('کو') or text == ('کجاس'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=کجا').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('اوک') or text == ('اک') or text == ('اکی') or text == ('اوکی') or text == ('عوکی') or text == ('عوک'):
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'حله' , chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('واقعا') or text == ('واقعن') or text == ('واقعا؟'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=واقعا').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('مرصی') or text == ('مرس') or text == ('مرسی') or text == ('مرص'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=واقعا').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == ('ت') or text == ('ط') or text == ('تو') or text == ('توو'):
                                
                                try:
                                    jd = requests.get('http://haji-api.ir/sokhan?text=تو').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'من خودام' or text == 'من خدام' or text == 'خودام' or text == 'خدام':
                                
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آره حاجی تو مجازی معلومه خدا میشی🤣🚶🏻‍♂',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
#End-Texts
                            if text == '!zaman' or text == '/zaman' or text == 'زمان' :
                                
                                try:
                                    date = ___date____time.historyIran()
                                    time = ___date____time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ: \n' + date + '\nساعت:\n'+ time,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '!date' or text == 'تاریخ' or text == '/date' :
                                
                                try:
                                    date = ___date____time.historyIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ \n' + date ,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == '/time' or text == '/Time' or text == 'ساعت' or text == 'تایم' :
                                
                                try:
                                    time = ___date____time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'ساعت  \n' + time ,chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'منم خبم' or text == 'منم خوبم' or text == 'منم خبمح' or text == 'خوبم' or text == 'خبم' or text == 'خبمح':
                                
                                try:

                                    bot.sendMessage(chat['object_guid'], 'شٌکر خوب بمونی',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            if text == 'تست' or text == 'test' or text == '!test' or text == '/test' or text == '/Test' or text == '!Test':
                                
                                try:

                                    bot.sendMessage(chat['object_guid'], 'RoBot is Ok .',chat['last_message']['message_id'])
                                      
                                except:
                                    print('server bug1')
                            elif text.startswith('/nim http://') == True or text.startswith('/nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                          
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('/info @'):
                                tawd10 = Thread(target=info_AmoBot, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('/srch ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('/wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + 'ویکی پدیا'
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '/wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')              
                            elif text.startswith('/zekr') or text.startswith('ذکر'):
                                tawd219 = Thread(target=get_zeikr, args=(text, chat, bot,))
                                tawd219.start()
                            elif text.startswith('حدیث') or text.startswith('!hadis'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()
                            elif text.startswith('/name_shakh')  or text.startswith('نام شاخ'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                                
                            elif text.startswith('/jok') or text.startswith('جوک'):
                                tawd21 = Thread(target=get_jok, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('/hagh') or text.startswith('حرف حق'):
                                tawd21 = Thread(target=get_hagh, args=(text, chat, bot,))
                                tawd21.start()
                                
                            elif text.startswith('/khatere')  or text.startswith('خاطره'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('/danesh')  or text.startswith('دانستنی'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('/deghat')  or text.startswith('دقت کردین'):
                                tawd20 = Thread(target=get_deghat, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('جملات سنگین') or text.startswith('/gang'):
                                tawd215 = Thread(target=get_gang, args=(text, chat, bot,))
                                tawd215.start()
                            elif text.startswith('/alaki_masala')  or text.startswith('الکلی مثلا'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('/dastan')  or text.startswith('داستان'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('/bio')  or text.startswith('بیو'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!mont') or text.startswith('/mont') or text.startswith('مناسبت'):
                                tawd27 = Thread(target=get_sebt, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('/srch-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                            elif text.startswith('/ban [') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'کاربر به همراه ایدی حذف شد @User_Coder 👺' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('https') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    bot.banGroupMember(chat['object_guid'], guid)
                                    bot.sendMessage(chat['object_guid'], 'کاربر به همراه ایدی حذف شد @User_Coder 👺' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('/srch-p ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('بن') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('/trans ['):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('/myket ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('/viki ['):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('/arz'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('/Ping ['):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('/Golds'):
                                tawd22 = Thread(target=get_golds, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('/font-en ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('/font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('/whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('/vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('/hvs ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('/ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                            elif text.startswith("/add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'کاربر اضافه شد @User_Coder 👺' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                            elif text.startswith('/math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                                    #شات
                            elif text.startswith('/shot') or text.startswith('شات'):
                                tawd516 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd516.start()
                                #شات
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0EgifW0ee160ca703e33a157fc8c98d' and chat['abs_object']['type'] == 'Group' and not text.startswith('!'):
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            elif text.startswith('/bgo') or text.startswith('بگو') or text.startswith('بنال') or text.startswith('ویس') or text.startswith('/speak'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('/danpic') or text.startswith('عکس دانستنی') or text.startswith('دانش') or text.startswith('!danpic'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('کیرم') or text.startswith('کیر') or text.startswith('کییر'):
                                tawd12 = Thread(target=phoshe, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('فال') or text.startswith('کیر') or text.startswith('کییر'):
                                tawd12 = Thread(target=fall, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('منتقیه') or text.startswith('منطق') or text.startswith('منطقیه') or text.startswith('منتطقیه'):
                                tawd15 = Thread(target=photo_random, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('فوتوتایم') or text.startswith('فوتو تایم') or text.startswith('تایم در عکس') or text.startswith('/photo_time'):
                                tawd16 = Thread(target=photo_time, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('/write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                bot.banGroupMember(chat['object_guid'], guid)
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('!help') or text.startswith('/help') or text.startswith('دستورات') or text.startswith('پنل') or text.startswith('Help'):
                                #bot.sendMessage(chat['object_guid'], '🔴 راهـنـمای DiGiBoT - ver 1.2.2\n\n📜 لیست ابزارهای ربات:\n/Commands \n\n💬 سرویس موتور جستجو:\n/search ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌\n\n⚠ قوانین ربات:\n/Rules \n\n⚙ گروه های فعال :\n/Group \n\n🔸 فعال کردن سرویس بازی :\n/Sargarmi ‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍\n\n🔹- user support @User_Coder 👺', chat['last_message']['message_id'])
                                tawd112 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd112.start()
                            elif text.startswith('ج ح') or text.startswith('جرعت حقیقت') or text.startswith('جرعت') or text.startswith('جرات') or text.startswith('!GH') or text.startswith('/gh') or text.startswith('/jrat') or text.startswith('حقیقت'):
                                tawd412 = Thread(target=get_grat, args=(text, chat, bot,))
                                tawd412.start()
                            elif text.startswith('!listone') or text.startswith('!listone') or text.startswith('/listone'):
                                tawd912 = Thread(target=get_listone, args=(text, chat, bot,))
                                tawd912.start()
                            elif text.startswith('/listtwo') or text.startswith('!listtwo'):
                                tawd512 = Thread(target=get_listtwo, args=(text, chat, bot,))
                                tawd512.start()
                            elif text.startswith('سرگرمی ها') or text.startswith('/Sargarmi') or text.startswith('!sargarmi') or text.startswith('سرگرمی') or text.startswith('[سرگرمی]') or text.startswith('[سرگرمی ها]'):
                                tawd3668 = Thread(target=get_car, args=(text, chat, bot,))
                                tawd3668.start()        
                            elif text.startswith('tool') or text.startswith('/Tools') or text.startswith('Tools') or text.startswith('!Tools') or text.startswith('!tool') or text.startswith('/tools'):
                                tawd3606 = Thread(target=get_sargarmi, args=(text, chat, bot,))
                                tawd3606.start()                         
                            elif text.startswith('جستجو') or text.startswith('/Search') or text.startswith('/search'):
                                tawd358 = Thread(target=get_srch, args=(text, chat, bot,))
                                tawd358.start()
 #کاربردی
                            elif text.startswith('کاربردی') or text.startswith('ابزار کاربردی') or text.startswith('/Commands') or text.startswith('Commands') or text.startswith('commands') or text.startswith('!commands'):
                                tawd238 = Thread(target=gets_karborde, args=(text, chat, bot,))
                                tawd238.start()
#کاربردی                         
                            elif text.startswith('66') or text.startswith('666'):
                                tawd348 = Thread(target=get_sar, args=(text, chat, bot,))
                            elif text.startswith('شروع') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'یادگیری فعال شد', chat['last_message']['message_id'])
                            elif text.startswith('پایان') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'یادگیری غیرفعال شد.', chat['last_message']['message_id'])  
                            elif text.startswith('فعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی فعال شد.', chat['last_message']['message_id'])
                            elif text.startswith('غیرفعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی غیرفعال شد.', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in AmoBotAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0DcA7S0def8612b339488bb4he20f50' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0DcA7S0gek8612b332488bbhfe40f50' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print(red+'Update Chats Messenger')
    except:
        print(yellow+'Err Koli')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
