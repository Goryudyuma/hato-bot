# coding: utf-8
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from slacker import Slacker
import unicodedata
import os
from logging import getLogger
from library.weather import get_city_id_from_city_name
from library.weather import get_weather
from library.amesh import get_map
from PIL import Image
from datetime import datetime

logger = getLogger(__name__)

# 「hato help」を見つけたら、使い方を表示する
@respond_to('help')
def help(message):
    user = message.user['name']
    logger.debug("%s called 'hato help'", user)
    message.send(
        '\n使い方\n'
        '```'
        'help       ... botの使い方を表示する。\n'
        '天気 [地名] ... 地名の天気予報を表示する。\n'
        '>< [文字列] ... 文字列を吹き出しで表示する。\n'
        '```')

@respond_to('天気 .+')
def weather(message):
    user = message.user['name']
    logger.debug("%s called 'hato 天気'", user)
    text = message.body['text']
    tmp, word = text.split(' ', 1)
    city_id = get_city_id_from_city_name(word)
    if city_id == None:
        message.send('該当する情報が見つからなかったっぽ！')
    else:
        weather_info = get_weather(city_id)
        message.send('```' + weather_info +'```')

# 「hato >< 文字列」を見つけたら、文字列を突然の死で装飾する
@respond_to('^&gt;&lt; .+')
def totuzensi(message):
    user = message.user['name']
    text = message.body['text']
    tmp, word = text.split(' ', 1)
    logger.debug("%s called 'hato >< %s'", user, word)
    word = generator(word)
    msg = '\n```' + word + '```'
    message.send(msg)

@respond_to('^amesh')
def amesh(message):
    user = message.user['name']
    channel = message.channel._body['name']
    logger.debug("%s called 'hato amesh'", user)
    orgn_map_file = get_map()
    # 圧縮する
    im1 = Image.open(orgn_map_file)
    im1.save(orgn_map_file, 'JPEG', quality=80)
    file = orgn_map_file
    message.send('東京の雨雲状況をお知らせするっぽ！')
    slacker = Slacker(str(os.environ['SLACKBOT_API_TOKEN']))
    slacker.files.upload(file_=file, channels=channel)

@respond_to('^laboin')
def laboin(message):
    user = message.user['name']
    logger.debug("%s called 'laboin'", user)
    message.send('その機能にはまだ対応してないっぽ！')

@respond_to('^laborida')
def laborida(message):
    user = message.user['name']
    logger.debug("%s called 'laborida", user)
    hour = str(datetime.today().strftime('%H'))
    message.send('まだ'+ hour +'時なのに帰るっぽ? 進捗あったっぽ?')

# 突然の死で使う関数
# Todo: 別ファイルに移したい。
def text_len(text):
    count = 0
    for c in text:
        count += 2 if unicodedata.east_asian_width(c) in 'FWA' else 1
    return count

def generator(msg):
    length = text_len(msg)
    generating = '＿人'
    for i in range(length//2):
        generating += '人'
    generating += '人＿\n＞  ' + msg + '  ＜\n￣^Y'
    for i in range(length//2):
        generating += '^Y'
    generating += '^Y￣'
    return generating