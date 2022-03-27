#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Updated:
#  1. 使用async来update lastname，更加稳定
#  2. 增加emoji clock，让时间显示更加有趣味

import time
import os
import sys
import logging
import asyncio
import random
from time import strftime
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from emoji import emojize


dizzy = emojize(":dizzy:", use_aliases=True)
cake = emojize(":cake:", use_aliases=True)
all_time_emoji_name = ["clock12", "clock1230", "clock1", "clock130", "clock2", "clock230", "clock3", "clock330", "clock4", "clock430", "clock5", "clock530", "clock6", "clock630", "clock7", "clock730", "clock8", "clock830", "clock9", "clock930", "clock10", "clock1030", "clock11", "clock1130"]
time_emoji_symb = [emojize(":%s:" %s, use_aliases=True) for s in all_time_emoji_name]

api_auth_file = 'api_auth'
if not os.path.exists(api_auth_file+'.session'):
    api_id = input('api_id: ')
    api_hash = input('api_hash: ')
else:
    api_id = 123456
    api_hash = '00000000000000000000000000000000'

client1 = TelegramClient(api_auth_file, api_id, api_hash)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def change_name_auto():
    # Set time zone to UTC+8
    # ln -sf /usr/share/zoneinfo/Asia/Chongqing /etc/localtime
    # https://stackoverflow.com/questions/4788533/python-strftime-gmtime-not-respecting-timezone

    print('will change name')

    while True:
        try:
            time_cur = strftime("%H:%M:%S:%p:%a", time.localtime())
            hour, minu, seco, p, abbwn = time_cur.split(':')
            if seco=='00' or seco=='5'or seco=='10' or seco=='15' or seco=='20' or seco=='25'or seco=='30'or seco=='35'or seco=='40'or seco=='45'or seco=='50':
                shift = 0
                mult = 1
                if int(minu)>30: shift=1
                # print((int(hour)%12)*2+shift)
                # hour symbols
                hsym = time_emoji_symb[(int(hour)%12)*2+shift]
                # await client1.send_message('me', hsym)
                last_names = ['故事的小黄花','从出生那年就飘着','童年的荡秋千','随记忆一直晃到现在','ReSoSoSiDoSiLa','SoLaSiSiSiSiLaSiLaSo','吹着前奏望着天空','我想起花瓣试着掉落','为你翘课的那一天','花落的那一天','教室的那一间','我怎么看不见','消失的下雨天','我好想再淋一遍','没想到失去的勇气我还留着','好想再问一遍','你会等待还是离开','刮风这天我试过握着你手','但偏偏雨渐渐大到我看你不见','还要多久我才能在你身边','等到放晴的那天也许我会比较好一点','从前从前有个人爱你很久','但偏偏风渐渐把距离吹得好远','好不容易又能再多爱一天','但故事的最后你好像还是说了拜拜','为你翘课的那一天','花落的那一天','教室的那一间','我怎么看不见','消失的下雨天','我好想再淋一遍','没想到失去的勇气我还留着','好想再问一遍','你会等待还是离开','刮风这天我试过握着你手','但偏偏雨渐渐大到我看你不见','还要多久我才能在你身边','等到放晴的那天也许我会比较好一点','从前从前有个人爱你很久','偏偏风渐渐把距离吹得好远','好不容易又能再多爱一天','但故事的最后你好像还是说了拜拜','刮风这天我试过握着你手','但偏偏雨渐渐大到我看你不见','还要多久我才能够在你身边','等到放晴那天也许我会比较好一点','从前从前有个人爱你很久','但偏偏雨渐渐把距离吹得好远','好不容易又能再多爱一天','但故事的最后你好像还是说了拜']
                k=random.randint(0,49)
                first_name=last_names[k]
                last_name= '大脑斧 %s:%s  ' % (hour, minu)

        
                await client1(UpdateProfileRequest(first_name=first_name,last_name=last_name))
                logger.info('Updated -> %s' % first_name)
                logger.info('Updated -> %s' % last_name)
        
        except KeyboardInterrupt:
            print('\nwill reset last name\n')
            await client1(UpdateProfileRequest(last_name=''))
            sys.exit()

        except Exception as e:
            print('%s: %s' % (type(e), e))

        await asyncio.sleep(1)


# main function
async def main(loop):

    await client1.start()

    # create new task
    print('creating task')
    task = loop.create_task(change_name_auto())
    await task
     
    print('It works.')
    await client1.run_until_disconnected()
    task.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
