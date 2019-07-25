#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import signal
import shutil
import queue
import threading
import subprocess
import datetime
import time
import codecs
import glob

print(os.path.dirname(__file__))
print(os.path.basename(__file__))
print(sys.version_info)



# インターフェース
qCtrl_control_main       = 'temp/control_main.txt'
qCtrl_control_audio      = 'temp/control_audio.txt'
qCtrl_control_video      = 'temp/control_video.txt'
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_web        = 'temp/control_web.txt'
qCtrl_control_chatting   = 'temp/control_chatting.txt'
qCtrl_control_knowledge  = 'temp/control_knowledge.txt'

# Python
qPython_main_audio = '_v5__main_audio.py'
qPython_main_video = '_v5__main_video.py'
qPython_bgm        = '_v5__sub_bgm.py'
#qPython_bgm        = '_v5_sub_bgm_control.py'
qPython_web        = '_v5_sub_web_control.py'
qPython_chatting   = '_v5_sub_chatting_control.py'
qPython_knowledge  = '_v5_sub_knowledge_control.py'

qPython_selfcheck  = '_v5_sub_self_check.py'
qPython_smartSpk   = '_v5_sub_smart_speaker.py'
qPython_rssSearch  = '_v5_sub_rss_search.py'
qPython_weather    = '_v5_sub_weather_search.py'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS            = qFunc.getValue('qOS'           )
qHOSTNAME      = qFunc.getValue('qHOSTNAME'     )
qPath_log      = qFunc.getValue('qPath_log'     )
qPath_work     = qFunc.getValue('qPath_work'    )
qPath_rec      = qFunc.getValue('qPath_rec'     )

qPath_a_ctrl   = qFunc.getValue('qPath_a_ctrl'  )
qPath_a_inp    = qFunc.getValue('qPath_a_inp'   )
qPath_a_wav    = qFunc.getValue('qPath_a_wav'   )
qPath_a_jul    = qFunc.getValue('qPath_a_jul'   )
qPath_a_STT    = qFunc.getValue('qPath_a_STT'   )
qPath_a_TTS    = qFunc.getValue('qPath_a_TTS'   )
qPath_a_TRA    = qFunc.getValue('qPath_a_TRA'   )
qPath_a_play   = qFunc.getValue('qPath_a_play'  )
qPath_v_ctrl   = qFunc.getValue('qPath_v_ctrl'  )
qPath_v_inp    = qFunc.getValue('qPath_v_inp'   )
qPath_v_jpg    = qFunc.getValue('qPath_v_jpg'   )
qPath_v_detect = qFunc.getValue('qPath_v_detect')
qPath_v_cv     = qFunc.getValue('qPath_v_cv'    )
qPath_v_photo  = qFunc.getValue('qPath_v_photo' )
qPath_v_msg    = qFunc.getValue('qPath_v_msg'   )
qPath_v_screen = qFunc.getValue('qPath_v_screen')

qBusy_dev_cpu  = qFunc.getValue('qBusy_dev_cpu' )
qBusy_dev_com  = qFunc.getValue('qBusy_dev_com' )
qBusy_dev_mic  = qFunc.getValue('qBusy_dev_mic' )
qBusy_dev_spk  = qFunc.getValue('qBusy_dev_spk' )
qBusy_dev_cam  = qFunc.getValue('qBusy_dev_cam' )
qBusy_dev_dsp  = qFunc.getValue('qBusy_dev_dsp' )
qBusy_a_ctrl   = qFunc.getValue('qBusy_a_ctrl'  )
qBusy_a_inp    = qFunc.getValue('qBusy_a_inp'   )
qBusy_a_wav    = qFunc.getValue('qBusy_a_wav'   )
qBusy_a_STT    = qFunc.getValue('qBusy_a_STT'   )
qBusy_a_TTS    = qFunc.getValue('qBusy_a_TTS'   )
qBusy_a_TRA    = qFunc.getValue('qBusy_a_TRA'   )
qBusy_a_play   = qFunc.getValue('qBusy_a_play'  )
qBusy_v_ctrl   = qFunc.getValue('qBusy_v_ctrl'  )
qBusy_v_inp    = qFunc.getValue('qBusy_v_inp'   )
qBusy_v_jpg    = qFunc.getValue('qBusy_v_jpg'   )
qBusy_v_CV     = qFunc.getValue('qBusy_v_CV'    )
qBusy_v_rec    = qFunc.getValue('qBusy_v_rec'   )



# debug
runMode      = 'hud'

qApiInp     = 'free'
qApiTrn     = 'free'
qApiOut     = qApiTrn
if (qOS == 'windows'):
    qApiOut = 'winos'
if (qOS == 'darwin'):
    qApiOut = 'macos'
qLangInp    = 'ja'
#qLangTrn    = 'en,fr,'
qLangTrn    = 'en'
qLangTxt    = qLangInp
qLangOut    = qLangTrn[:2]



# シグナル処理
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス

    qFunc.init()

    # ログ設定

    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )

    qFunc.logOutput(main_id + ':init')
    qFunc.logOutput(main_id + ':exsample.py runMode, ..., ')

    #runMode  debug, handsfree, translator, speech, number, hud, camera,

    # パラメータ

    if (True):

        #runMode     = 'handsfree'
        micDev      = '0'
        micType     = 'bluetooth'
        micGuide    = 'on'
        micLevel    = '777'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        if (runMode == 'debug'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        if (runMode == 'handsfree'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        if (runMode == 'translator'):
            micType   = 'bluetooth'
            micGuide  = 'display'
        if (runMode == 'speech') or (runMode == 'number'):
            micType   = 'usb'
            micGuide  = 'display'
        if (runMode == 'hud'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        if (runMode == 'camera'):
            micType   = 'bluetooth'
            micGuide  = 'off'

        if (len(sys.argv) >= 3):
            micDev   = str(sys.argv[2]).lower()
            if (not micDev.isdigit()):
                micGuide = 'off' 
        if (len(sys.argv) >= 4):
            micType  = str(sys.argv[3]).lower()
        if (len(sys.argv) >= 5):
            micGuide = str(sys.argv[4]).lower()
        if (len(sys.argv) >= 6):
            p = str(sys.argv[5]).lower()
            if (p.isdigit() and p != '0'):
                micLevel = p

        if (len(sys.argv) >= 7):
            qApiInp  = str(sys.argv[6]).lower()
            if (qApiInp == 'google') or (qApiInp == 'watson') \
            or (qApiInp == 'azure')  or (qApiInp == 'nict'):
                qApiTrn  = qApiInp
                qApiOut  = qApiInp
            else:
                qApiTrn  = 'free'
                qApiOut  = 'free'
            if (qApiInp == 'nict'):
                #qLangTrn = 'en,fr,es,id,my,th,vi,zh,ko,'
                qLangTrn = 'en,fr,es,id,zh,ko,'
                qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 8):
            qApiTrn  = str(sys.argv[7]).lower()
        if (len(sys.argv) >= 9):
            qApiOut  = str(sys.argv[8]).lower()
        if (len(sys.argv) >= 10):
            qLangInp = str(sys.argv[9]).lower()
            qLangTxt = qLangInp
        if (len(sys.argv) >= 11):
            qLangTrn = str(sys.argv[10]).lower()
            qLangOut = qLangTrn[:2]
        if (len(sys.argv) >= 12):
            qLangTxt = str(sys.argv[11]).lower()
        if (len(sys.argv) >= 13):
            qLangOut = str(sys.argv[12]).lower()

        qFunc.logOutput(main_id + ':runMode  =' + str(runMode  ))
        qFunc.logOutput(main_id + ':micDev   =' + str(micDev   ))
        qFunc.logOutput(main_id + ':micType  =' + str(micType  ))
        qFunc.logOutput(main_id + ':micGuide =' + str(micGuide ))
        qFunc.logOutput(main_id + ':micLevel =' + str(micLevel ))

        qFunc.logOutput(main_id + ':qApiInp  =' + str(qApiInp  ))
        qFunc.logOutput(main_id + ':qApiTrn  =' + str(qApiTrn  ))
        qFunc.logOutput(main_id + ':qApiOut  =' + str(qApiOut  ))
        qFunc.logOutput(main_id + ':qLangInp =' + str(qLangInp ))
        qFunc.logOutput(main_id + ':qLangTrn =' + str(qLangTrn ))
        qFunc.logOutput(main_id + ':qLangTxt =' + str(qLangTxt ))
        qFunc.logOutput(main_id + ':qLangOut =' + str(qLangOut ))

    # 初期設定

    if (True):

        # インターフェースリセット

        qFunc.remove(qCtrl_control_main      )
        qFunc.remove(qCtrl_control_audio     )
        qFunc.remove(qCtrl_control_video     )
        qFunc.remove(qCtrl_control_bgm       )
        qFunc.remove(qCtrl_control_web       )
        qFunc.remove(qCtrl_control_chatting  )
        qFunc.remove(qCtrl_control_knowledge )

        qFunc.busySet(qBusy_dev_cpu, False)
        qFunc.busySet(qBusy_dev_com, False)
        qFunc.busySet(qBusy_dev_mic, False)
        qFunc.busySet(qBusy_dev_spk, False)
        qFunc.busySet(qBusy_dev_cam, False)
        qFunc.busySet(qBusy_dev_dsp, False)

        # 起動条件

        main_audio_run    = None
        main_audio_switch = 'on'
        main_video_run    = None
        main_video_switch = 'off'
        bgm_run           = None
        bgm_switch        = 'off'
        web_run           = None
        web_switch        = 'off'
        chatting_run      = None
        chatting_switch   = 'off'
        knowledge_run     = None
        knowledge_switch  = 'off'

        if   (runMode == 'debug'):
            main_video_switch = 'on'
        elif (runMode == 'handsfree'):
            main_video_switch = 'on'
            bgm_switch        = 'off'
        elif (runMode == 'translator'):
            pass
        elif (runMode == 'speech'):
            pass
        elif (runMode == 'number'):
            pass
        elif (runMode == 'hud'):
            main_video_switch = 'on'
        elif (runMode == 'camera'):
            main_video_switch = 'on'
        else:
            main_video_switch = 'on'

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

    # 待機ループ

    onece = True
    last_alive = time.time()

    while (True):

        # 終了確認

        control = ''
        txts, txt = qFunc.txtsRead(qCtrl_control_main)
        if (txt == '_close_'):
            break
        else:
            qFunc.remove(qCtrl_control_main)
            control = txt

        # コントロール
        if (control == 'bgm_start'):
            bgm_switch = 'on'
        if (control == 'bgm_stop'):
            bgm_switch = 'off'

        # 活動メッセージ

        if  ((time.time() - last_alive) > 30):
            qFunc.logOutput(main_id + ':alive')
            last_alive = time.time()

        # プロセス設定

        speechs = []

        if (main_audio_run is None) and (main_audio_switch == 'on'):
            main_audio_run = subprocess.Popen(['python', qPython_main_audio, 
                                runMode, micDev, micType, micGuide, micLevel,
                                qApiInp, qApiTrn, qApiOut,
                                qLangInp, qLangTrn, qLangTxt, qLangOut, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            if   (runMode == 'debug'):
                speechs.append({ 'text':u'ハンズフリーコントロールシステムをデバッグモードで、起動しました。', 'wait':0, })
            elif (runMode == 'handsfree'):
                speechs.append({ 'text':u'ハンズフリー翻訳機能を、起動しました。', 'wait':0, })
            elif (runMode == 'hud'):
                speechs.append({ 'text':u'ヘッドアップディスプレイ機能を、起動しました。', 'wait':0, })
            elif (runMode == 'camera'):
                speechs.append({ 'text':u'ハンズフリーカメラ機能を、起動しました。', 'wait':0, })

        if (not main_audio_run is None) and (main_audio_switch != 'on'):
            #main_audio_run.wait()
            main_audio_run.terminate()
            main_audio_run = None

        if (main_video_run is None) and (main_video_switch == 'on'):
            main_video_run = subprocess.Popen(['python', qPython_main_video, 
                                runMode, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'カメラ機能を、起動しました。', 'wait':0, })

        if (not main_video_run is None) and (main_video_switch != 'on'):
            #main_video_run.wait()
            main_video_run.terminate()
            main_video_run = None

            speechs.append({ 'text':u'カメラ機能を、終了しました。', 'wait':0, })

        if (bgm_run is None) and (bgm_switch == 'on'):
            bgm_run = subprocess.Popen(['python', qPython_bgm, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ＢＧＭ再生機能を、起動しました。', 'wait':0, })

        if (not bgm_run is None) and (bgm_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_bgm       ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #bgm_run.wait()
            bgm_run.terminate()
            bgm_run = None

            speechs.append({ 'text':u'ＢＧＭ再生機能を、終了しました。', 'wait':0, })

        if (web_run is None) and (web_switch == 'on'):
            web_run = subprocess.Popen(['python', qPython_web, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ブラウザー連携機能を、起動しました。', 'wait':0, })

        if (not web_run is None) and (web_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_web       ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #web_run.wait()
            web_run.terminate()
            web_run = None

            speechs.append({ 'text':u'ブラウザー連携機能を、終了しました。', 'wait':0, })

        if (chatting_run is None) and (chatting_switch == 'on'):
            chatting_run = subprocess.Popen(['python', qPython_chatting, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ドコモ雑談連携機能を、起動しました。', 'wait':0, })

        if (not chatting_run is None) and (chatting_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_chatting  ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #chatting_run.wait()
            chatting_run.terminate()
            chatting_run = None

            speechs.append({ 'text':u'ドコモ雑談連携機能を、終了しました。', 'wait':0, })

        if (knowledge_run is None) and (knowledge_switch == 'on'):
            knowledge_run = subprocess.Popen(['python', qPython_knowledge, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ドコモ知識データベースを、起動しました。', 'wait':0, })

        if (not knowledge_run is None) and (knowledge_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_knowledge ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #knowledge_run.wait()
            knowledge_run.terminate()
            knowledge_run = None

            speechs.append({ 'text':u'ドコモ知識データベースを、終了しました。', 'wait':0, })

        if (len(speechs) != 0):
            qFunc.speech(id=main_id, speechs=speechs, lang='', )

        if (onece == True):
            onece = False

            if   (runMode == 'debug') \
            or   (runMode == 'handsfree'):
                time.sleep(40)
                speechs = []
                speechs.append({ 'text':u'全ての準備が整いました。スタンバイしています。', 'wait':0, })
                qFunc.speech(id=main_id, speechs=speechs, lang='', )

        # アイドリング
        if  (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy'):
            time.sleep(1.00)
        time.sleep(0.25)



    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        # プロセス終了(音声以外)

        qFunc.txtsWrite(qCtrl_control_main      ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_audio     ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_video     ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_bgm       ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_web       ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_chatting  ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_knowledge ,txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )
        
        time.sleep(60.00)

        if (not main_audio_run is None):
            #main_audio_run.wait()
            main_audio_run.terminate()
            main_audio_run = None

        if (not main_video_run is None):
            #main_video_run.wait()
            main_video_run.terminate()
            main_video_run = None

        if (not bgm_run is None):
            #bgm_run.wait()
            bgm_run.terminate()
            bgm_run = None

        if (not web_run is None):
            #web_run.wait()
            web_run.terminate()
            web_run = None

        if (not chatting_run is None):
            #chatting_run.wait()
            chatting_run.terminate()
            chatting_run = None

        if (not knowledge_run is None):
            #knowledge_run.wait()
            knowledge_run.terminate()
            knowledge_run = None

        # プロセス終了(音声)

        #qFunc.txtsWrite(qCtrl_control_audio, txts=['_close_'], encoding='utf-8', exclusive=True, mode='w', )

        #time.sleep(30.00)

        #if (not main_audio_run is None):
        #    #main_audio_run.wait()
        #    main_audio_run.terminate()
        #    main_audio_run = None

        time.sleep(30.00)

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)


