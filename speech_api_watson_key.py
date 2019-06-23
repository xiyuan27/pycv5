#!/usr/bin/env python
# -*- coding: utf-8 -*-



def getkey(api, key):

    # Watson 音声認識
    if (api == 'stt'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            return 'your name'
        if (key == 'password'):
            return 'your key'

    # Watson 翻訳機能
    if (api == 'tra'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            return 'your name'
        if (key == 'password'):
            return 'your key'

    # Watson 音声合成
    if (api == 'tts'):
        print('speech_api_watson_key.py')
        print('set your key!')
        if (key == 'username'):
            return 'your name'
        if (key == 'password'):
            return 'your key'

    return False


