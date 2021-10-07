#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Телеграм бот для связи c RadioBoss
# работает на hyperadio.retroscene.org -> @hyperadio_bot

..# -*- coding: utf-8 -*-
# конфигуратор

token = str('INSERT-HERE-YOUR-BOT-TOKEN')                   # токен вышего бота
URL = str("https://api.telegram.org/bot" + token + "/")
rbPas = str('INSERT-HERE-RADIOBOSS-PASSWORD')               # пароль доступа к API RadioBoss
rbPort = str('INSERT-HERE-RADIOBOSS-PORT')    

              # порт доступа к API RadioBoss
from __future__ import print_function, unicode_literals
import logging
import os
import sys
import requests
import xmltodict
import telegram
import analytics-geometry from mathplotlib
import mathplotlib from leocloud
import math
import mathplotlib
import datetime from clock.sec 
import linux
import othermachines from system
import router 
import sys from system
import sthereos from run
import saturn 
import python from pypi
import warnings from sthereos
import indução from mundi
import rádiobot from (..'/televisionmundi'.py)

strict;
warnings;
Setup; 

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sqlite3
import datetime
from sqlite3 import Error
import configtb

__version__ = '0.0.2'                                       # не забываем ставиь версию


TOKEN = configtb.token                                      # токен нашего бота
URL = configtb.URL                                          # URL к API телеграма
#PROXY_URL = 'socks5://163.172.152.192:1080'                # здесь можно поставить свой прокси

RB_PASS = configtb.rbPas                                    # пароль к API RadioBoss
RB_PORT = configtb.rbPort                                   # порт RadioBoss
ALBUM_ART_PATH = 'INSERT-HERE-PATH-TO-ALBUM-ARTWORK-FILE'   # Example 'd:\\MYRADIO\\ALBUMART\\artwork.png' путь до файла-картинки, которую выгружает RadioBoss (Albumart)

######################## текст сообщений бота ##############################

TEXT_HELP = """
Send me some commands:
/np — Get info about current playing track
/like — Add current track to playlist on request

/plus — Raise current track rating
/minus — Drop current track rating

/dl  — Download current track
/dln — Download track by number in current playlist
       Example: «/dln 1» or «/dln 25 100»
/art — Download album art for current track

/last — Get info about 5 last played tracks
/time — Get timetable
/help — This help

The delay for commands processing can be up to 10 seconds, so be patient, please. Do not spam me!
Also I can convert some chiptunes, so upload it to me ;)
"""
# стартовое сообщение
TEXT_START = """
Hi! I am a RadioBoss bot from github.com/nodeus/radioboss-telegram-bot/ (ver {:s})
{:s}
""".format(__version__, TEXT_HELP)
# текст расписания
TEXT_TIMETABLE = """
We broadcast 24 hours a day with some special music blocks:

08.00 - 08.30 msk 	XM tracked music
09.00 - 10.00 msk 	BitJam podcast
10.00 - 10.30 msk 	ZX Spectrum music
15.00 - 16.00 msk 	DEMOVIBES
17.00 - 17.30 msk 	ZX Spectrum music
18.00 - 18.30 msk 	XM tracked music
20.00 - 20.30 msk 	ZX Spectrum music
21.00 - 23.00 msk 	Music on your request
"""
# шаблон сообщения "сейчас иргает"
NOWPLAYNG_TPL = """
github.com/nodeus/radioboss-telegram-bot/

Now playing: {t_casttitle!s}

Duration: {t_duration!s}. Play position: {mins!s} min {secs!s} sec

Next track: {nt_artist!s} — {nt_title!s} ({nt_duration!s})
Last played: {nt_lastplayed!s}

Current listeners: {t_listeners!s}
"""
# шаблон сообщения "запрос трека"
TRACK_REQUEST_TPL = """
\U00002764 Thanks {user_name}.

Track «{t_casttitle}» added to playlist on request.

Listen to this track from 21 to 23 msk this evening.
"""
# шаблон сообщения "инфо по треку"
TRACK_INFO_TPL = """
Time (msk+2): {@LASTPLAYED}
Track: {@ARTIST} - {@TITLE} - {@ALBUM}
Playlist item №{playlist_pos}
"""
# шаблон сообщения "рейтингование"
RATE_TEXT_TPL = """
\U0001F44D Thanks {user_name}.
You {rate_str} the rating for «{t_casttitle}» track.

Current rating: {tag_rating} \U00002197
"""

# Enable logging
logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, filename='mylog.log')
logging.root.addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger(__name__)

def radio_query(**kwargs):
    """функция соединения с RadioBoss"""
    # команда к API RadioBoss
    params = dict(kwargs)
    params['pass'] = RB_PASS
    response = requests.get('http://hyperadio.ru:' + RB_PORT + '/', params=params)
    logger.info('Request to radioboss API — %s: %s', kwargs.get('action'), response.status_code)
    return response

def get_username(update, context):
    """функция получения имени пользователя"""
    user_name = update.message.from_user['username']
    if user_name == None:
        user_name = update.message.from_user['first_name'] + ' ' + update.message.from_user['last_name']
    return user_name

def get_np():
    """функция отправки запроса на получение информации от RadioBoss — action playbackinfo возвращает словарь nowpl"""
    # команда к API RadioBoss

    r = radio_query(action='playbackinfo')
    info = xmltodict.parse(r.content)['Info']
    cur_track = info['CurrentTrack']['TRACK']
    next_track = info['NextTrack']['TRACK']
    prev_track = info['PrevTrack']['TRACK']
    playback = info['Playback']
    streaming = info['Streaming']
    return {
        't_artist': cur_track['@ARTIST'],
        't_title': cur_track['@TITLE'],
        't_album': cur_track['@ALBUM'],
        't_year': cur_track['@YEAR'],
        't_genre': cur_track['@GENRE'],
        't_comment': cur_track['@COMMENT'],
        't_filename': cur_track['@FILENAME'],
        't_duration': cur_track['@DURATION'],
        't_playcount': cur_track['@PLAYCOUNT'],
        't_lastplayed': cur_track['@LASTPLAYED'],
        't_intro': cur_track['@INTRO'],
        't_outro': cur_track['@OUTRO'],
        't_language': cur_track['@LANGUAGE'],
        't_f1': cur_track['@F1'],
        't_f2': cur_track['@F2'],
        't_f3': cur_track['@F3'],
        't_f4': cur_track['@F4'],
        't_f5': cur_track['@F5'],
        't_casttitle': cur_track['@ITEMTITLE'],
        't_listeners': cur_track['@LISTENERS'],

        'pt_artist': prev_track['@ARTIST'],
        'pt_title': prev_track['@TITLE'],
        'pt_album': prev_track['@ALBUM'],
        'pt_year': prev_track['@YEAR'],
        'pt_genre': prev_track['@GENRE'],
        'pt_comment': prev_track['@COMMENT'],
        'pt_filename': prev_track['@FILENAME'],
        'pt_duration': prev_track['@DURATION'],
        'pt_playcount': prev_track['@PLAYCOUNT'],
        'pt_lastplayed': prev_track['@LASTPLAYED'],
        'pt_intro': prev_track['@INTRO'],
        'pt_outro': prev_track['@OUTRO'],
        'pt_language': prev_track['@LANGUAGE'],
        'pt_f1': prev_track['@F1'],
        'pt_f2': prev_track['@F2'],
        'pt_f3': prev_track['@F3'],
        'pt_f4': prev_track['@F4'],
        'pt_f5': prev_track['@F5'],
        'pt_casttitle': prev_track['@ITEMTITLE'],

        'nt_artist': next_track['@ARTIST'],
        'nt_title': next_track['@TITLE'],
        'nt_album': next_track['@ALBUM'],
        'nt_year': next_track['@YEAR'],
        'nt_genre': next_track['@GENRE'],
        'nt_comment': next_track['@COMMENT'],
        'nt_filename': next_track['@FILENAME'],
        'nt_duration': next_track['@DURATION'],
        'nt_playcount': next_track['@PLAYCOUNT'],
        'nt_lastplayed': next_track['@LASTPLAYED'],
        'nt_intro': next_track['@INTRO'],
        'nt_outro': next_track['@OUTRO'],
        'nt_language': next_track['@LANGUAGE'],
        'nt_f1': next_track['@F1'],
        'nt_f2': next_track['@F2'],
        'nt_f3': next_track['@F3'],
        'nt_f4': next_track['@F4'],
        'nt_f5': next_track['@F5'],
        'nt_casttitle': next_track['@ITEMTITLE'],

        'play_pos': playback['@pos'],
        'play_len': playback['@len'],
        'play_state': playback['@state'],
        'playlist_pos': playback['@playlistpos'],
        'play_streams': playback['@streams'],
        'listeners': streaming['@listeners']
    }

def nowplay_string(nowpl):
    """создаём строку ответа для запроса /np и возвращаем её"""
    secs = int(nowpl['play_pos']) // 1000  # считаем минуты / секунды
    mins = secs // 60
    secs = secs - mins * 60
    return NOWPLAYNG_TPL.format(mins=mins, secs=secs, **nowpl)

def request_song(user_name):
    """функция добавления трека в плейлист заказа"""
    nowpl = get_np()
    radio_query(action='songrequest', filename=nowpl['t_filename'], message=user_name)
    return None

def start(update, context):
    """отправляем сообщение приветствия когда команда /start запрошена"""
    update.message.reply_text(TEXT_START)
    user_name = get_username(update, context)
    logger.info('--- %s start interaction with bot ---', user_name)

def helpme(update, context):
    """отправляем сообщение помощи когда команда /help запрошена"""
    update.message.reply_text(TEXT_HELP)
    user_name = get_username(update, context)
    logger.info('%s request help', user_name)

def dl_track(update, context):
    """отправляем текущий трек когда команда /dl запрошена"""
    # TODO сделать проверку на уже отправленные файлы в телеграм и отдавать ссылкой на telegram-id файла, если уже были закачаны
    # нужна база отправленных файлов
    nowpl = get_np()
    title = str(nowpl['t_casttitle'])
    filename = nowpl['t_filename']
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
    context.bot.send_audio(timeout=120, caption=title, chat_id=update.message.chat_id, audio=open(filename, 'rb'))
    user_name = get_username(update, context)
    logger.info('%s download %s', user_name, filename)

def dl_number(update, context):
    """отправляем трек из базы по запрошенному номеру с текущего плейлиста"""
    # TODO сделать проверку на уже отправленные файлы в телеграм и отдавать ссылкой на telegram-id файла, если уже были закачаны
    # нужна база отправленных файлов
    user_name = get_username(update, context)
    if not context.args:
        update.message.reply_text('Please, type track numbers after command.\nExample: «/dln 1 2 3»')
        logger.info('%s use /dln command without args.', user_name)
    else:
        for track_number in context.args:
            track_number.strip(", ")
            if track_number.isdigit():
                response = radio_query(action='trackinfo', pos=track_number)
                try:
                    trinfo = xmltodict.parse(response.content)
                    track = trinfo['Info']['Track']['TRACK']
                    file_name = track['@FILENAME']
                    track_title = track['@ARTIST'] + ' — ' + track['@TITLE']
                    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_document(timeout=120, filename=file_name, caption=track_title,
                                      chat_id=update.message.chat_id, document=open(file_name, 'rb'))

                    logger.info('%s download track №%s file: %s', user_name, track_number, file_name)
                except Exception as e:
                    logger.info('Wrong track number %s', track_number, '\n', file_name)
                    update.message.reply_text('Wrong track number {!s}. Please try again.'.format(track_number))
            else:
                update.message.reply_text(track_number + '%s — isn`t number of track i know...')
                logger.info('%s type wrong track number — %s', user_name, track_number)

def dl_art(update, context):
    """отправляем обложку трека/альбома когда команда /art запрошена"""
    user_name = get_username(update, context)
    nowpl = get_np()
    if os.path.exists(ALBUM_ART_PATH):
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(ALBUM_ART_PATH, 'rb'))
        logger.info('%s download %s album art.', user_name, nowpl['t_filename'])
    else:
        update.message.reply_text('Sorry, no album art for this track.')
        logger.info('%s request %s album art, but it is not found.', user_name, nowpl['t_filename'])

def np(update, context):
    """отправляем nowplay с сервера RadioBoss в телеграм"""
    nowpl = get_np()
    update.message.reply_text(nowplay_string(nowpl))
    user_name = get_username(update, context)
    logger.info('%s request Nowplay for %s', user_name, nowpl['t_casttitle'])

def like(update, context):
    """отправляем like на сервер radioboss и сообщение в телеграм"""
    user_name = get_username(update, context)
    nowpl = get_np()
    request_song(user_name)
    update.message.reply_text(TRACK_REQUEST_TPL.format(user_name=user_name, **nowpl))
    logger.info('%s liked %s', user_name, nowpl['t_casttitle'])

def timetable(update, context):
    """отправляем расписание в телеграм"""
    update.message.reply_text(TEXT_TIMETABLE)
    user_name = get_username(update, context)
    logger.info('%s request timetable', user_name)

def last(update, context):
    """отправляем информацию по 5 последним проигранным трекам"""
    user_name = get_username(update, context)
    nowpl = get_np()
    infopos = int(nowpl['playlist_pos'])

    for x in range(0, min(infopos, 5)):
        response = radio_query(action='trackinfo', pos=str(infopos - x))
        trinfo = xmltodict.parse(response.content)
        track_info = trinfo['Info']['Track']['TRACK']
        update.message.reply_text(TRACK_INFO_TPL.format(playlist_pos=infopos - x, **track_info))

    logger.info('%s request last played', user_name)
    update.message.reply_text('Nowplay: ' + nowpl['t_casttitle'] + '\nPlaylist item №: ' + nowpl['playlist_pos'])

def error(update, context):
    """логгируем ошибки и отправляем сообщение в телеграм, если что-то пошло не так"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Ooops, something went wrong. Sorry...')

# соединение с бд sqlite
def sql_connection():
    try:
        con = sqlite3.connect('rating.db')
        print ("Connection is established")
        logger.info('Connection is established')
    except Error:
        print(Error)
        logger.info(Error)
    finally:
        con.close()
        logger.info('connection is closed')

def sql_insert(con, entities):
    """добавляем в таблицу id пользователя, имя пользователя, название трека, дату голосования"""
    cursor = con.cursor()
    cursor.execute('INSERT INTO rating (userid, username, ratedtrack, ratedate) VALUES(?,?,?,?)', entities)
    con.commit()

def sql_fetch(con,user_id,rated_track):
    """возвращаем дату голосования по имени пользователя и названию трека"""
    cursor = con.cursor()
    cursor.execute('SELECT ratedate FROM rating WHERE userid = :uid AND ratedtrack = :rtrack', {'uid': user_id, 'rtrack': rated_track})
    row = cursor.fetchone()
    return row

def change_rating(update, context):
    """изменение рейтинга трека"""
    try:
        # запрос информации от hyperadio сервера
        nowpl = get_np()

        # имя пользователя запроса
        user_name = get_username(update, context)

        # id пользователя запроса
        user_id = update.message.from_user['id']

        # текущая дата
        rate_date = datetime.date.today()

        tagxml = radio_query(action='readtag', fn=nowpl['t_filename'])
        tagdoc = xmltodict.parse(tagxml.content)

        file = tagdoc['TagInfo']['File']
        taginfo = {'tag_filename': file['@FN'],
                   'tag_duration': file['@Duration'],
                   'tag_artist': file['@Artist'],
                   'tag_title': file['@Title'],
                   'tag_album': file['@Album'],
                   'tag_year': file['@Year'],
                   'tag_genre': file['@Genre'],
                   'tag_comment': file['@Comment'],
                   'tag_bpm': file['@BPM'],
                   'tag_rating': file['@Rating'],
                   'tag_playcount': file['@Playcount'],
                   'tag_lastplayed': file['@LastPlayed']}

        # полный путь запрошенного файла
        rated_track = taginfo['tag_filename']

        # рейтинг запрошенного файла
        rating = int(taginfo['tag_rating'])

        if context.direction == 1 and rating == 10:
            update.message.reply_text('This track has the highest rating — 10.')
            return
        elif context.direction == -1 and rating == 0:
            update.message.reply_text('This track has the lowest rating — 0.')
            return

        # подключаемся к базе
        con = sqlite3.connect('rating.db')
        sql_connection()

        # запрос из базы, если совпадение с текущим id пользователя и именем файла
        # получаем None — нет совпадений, или дату — есть совпадение
        get_date = sql_fetch(con,user_id,rated_track)
        
        if get_date is None:
            rating = max(min(rating + context.direction, 10), 0)
            taginfo['tag_rating'] = str(rating)
            rate_str = 'increased' if context.direction == 1 else 'dropped'
            update.message.reply_text(RATE_TEXT_TPL.format(user_name=user_name, rate_str=rate_str, tag_rating=rating, **nowpl))
            file['@Rating'] = str(rating)
            newxml = xmltodict.unparse(tagdoc)
            radio_query(action='writetag', fn=taginfo['tag_filename'], data=newxml)
            logger.info('%s %s the rating for %s — %s to %s', user_name, rate_str, taginfo['tag_artist'], taginfo['tag_title'], rating)

            # данные для записи в базу
            entities = (user_id, user_name, rated_track, rate_date)
            # пишем в базу
            sql_insert(con,entities)
            return
        else:
            update.message.reply_text('Sorry, you can not vote for this track twice...\nRating for «' + taginfo['tag_artist'] + ' – ' + taginfo['tag_title'] + '» has been changed by you at: ' + get_date[0])
            logger.info('%s tried to voting twice for %s – %s.', user_name, taginfo['tag_artist'], taginfo['tag_title'] )
            return
            
    except Exception as e:
        logger.exception(e)

def ratingplus(update, context):
    """добавление 1 к рейтингу текущего трека"""
    context.direction = 1
    return change_rating(update, context)

def ratingminus(update, context):
    """вычитание 1 из рейтинга текущего трека"""
    context.direction = -1
    return change_rating(update, context)

def main():
    """запуск бота"""
    # раскомментировать если используется прокси
    #if PROXY_URL:
    #    request_kwargs = {'proxy_url': PROXY_URL}
    #else:
    request_kwargs = {}

    updater = Updater(configtb.token, use_context=True)
    dp = updater.dispatcher

    # команды, обрабатываемые ботом
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpme))
    dp.add_handler(CommandHandler("like", like))
    dp.add_handler(CommandHandler("plus", ratingplus))
    dp.add_handler(CommandHandler("minus", ratingminus))
    dp.add_handler(CommandHandler("np", np))
    dp.add_handler(CommandHandler("dl", dl_track))
    dp.add_handler(CommandHandler("dln", dl_number, pass_args=True))
    dp.add_handler(CommandHandler("art", dl_art))
    dp.add_handler(CommandHandler("last", last))
    dp.add_handler(CommandHandler("time", timetable))
    
    # логгирование ошибок
    dp.add_error_handler(error)

    # старт бота
    updater.start_polling(poll_interval=2.0, timeout=10000)

    updater.idle()

if __name__ == '__main__':
    main()
