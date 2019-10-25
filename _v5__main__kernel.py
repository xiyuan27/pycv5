#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2019 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
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
qCtrl_control_kernel     = 'temp/control_kernel.txt'
qCtrl_control_speech     = 'temp/control_speech.txt'
qCtrl_control_vision     = 'temp/control_vision.txt'
qCtrl_control_desktop    = 'temp/control_desktop.txt'
qCtrl_control_self       = qCtrl_control_kernel

qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_browser    = 'temp/control_browser.txt'
qCtrl_control_player     = 'temp/control_player.txt'
qCtrl_control_chatting   = 'temp/control_chatting.txt'
qCtrl_control_knowledge  = 'temp/control_knowledge.txt'

# Python
qPython_main_speech      = '_v5__main_speech.py'
qPython_main_vision      = '_v5__main_vision.py'
qPython_main_desktop     = '_v5__main_desktop.py'
qPython_bgm              = '_v5__sub_bgm.py'
qPython_browser          = '_v5__sub_browser.py'
qPython_player           = '_v5__sub_player.py'
qPython_chatting         = '_v5__sub_chatting.py'
qPython_knowledge        = '_v5__sub_knowledge.py'

qPython_selfcheck        = '_v5_sub_self_check.py'
qPython_smartSpk         = '_v5_sub_smart_speaker.py'
qPython_rssSearch        = '_v5_sub_rss_search.py'
qPython_weather          = '_v5_sub_weather_search.py'



# qFunc 共通ルーチン
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qOS             = qFunc.getValue('qOS'            )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
qPath_cache     = qFunc.getValue('qPath_cache'    )
qPath_sounds    = qFunc.getValue('qPath_sounds'   )
qPath_fonts     = qFunc.getValue('qPath_fonts'    )
qPath_log       = qFunc.getValue('qPath_log'      )
qPath_work      = qFunc.getValue('qPath_work'     )
qPath_rec       = qFunc.getValue('qPath_rec'      )

qPath_s_ctrl    = qFunc.getValue('qPath_s_ctrl'   )
qPath_s_inp     = qFunc.getValue('qPath_s_inp'    )
qPath_s_wav     = qFunc.getValue('qPath_s_wav'    )
qPath_s_jul     = qFunc.getValue('qPath_s_jul'    )
qPath_s_STT     = qFunc.getValue('qPath_s_STT'    )
qPath_s_TTS     = qFunc.getValue('qPath_s_TTS'    )
qPath_s_TRA     = qFunc.getValue('qPath_s_TRA'    )
qPath_s_play    = qFunc.getValue('qPath_s_play'   )
qPath_v_ctrl    = qFunc.getValue('qPath_v_ctrl'   )
qPath_v_inp     = qFunc.getValue('qPath_v_inp'    )
qPath_v_jpg     = qFunc.getValue('qPath_v_jpg'    )
qPath_v_detect  = qFunc.getValue('qPath_v_detect' )
qPath_v_cv      = qFunc.getValue('qPath_v_cv'     )
qPath_v_photo   = qFunc.getValue('qPath_v_photo'  )
qPath_v_msg     = qFunc.getValue('qPath_v_msg'    )
qPath_d_ctrl    = qFunc.getValue('qPath_d_ctrl'   )
qPath_d_play    = qFunc.getValue('qPath_d_play'   )
qPath_d_prtscn  = qFunc.getValue('qPath_d_prtscn' )
qPath_d_movie   = qFunc.getValue('qPath_d_movie'  )
qPath_d_upload  = qFunc.getValue('qPath_d_upload' )

qBusy_dev_cpu   = qFunc.getValue('qBusy_dev_cpu'  )
qBusy_dev_com   = qFunc.getValue('qBusy_dev_com'  )
qBusy_dev_mic   = qFunc.getValue('qBusy_dev_mic'  )
qBusy_dev_spk   = qFunc.getValue('qBusy_dev_spk'  )
qBusy_dev_cam   = qFunc.getValue('qBusy_dev_cam'  )
qBusy_dev_dsp   = qFunc.getValue('qBusy_dev_dsp'  )
qBusy_dev_scn   = qFunc.getValue('qBusy_dev_scn'  )
qBusy_s_ctrl    = qFunc.getValue('qBusy_s_ctrl'   )
qBusy_s_inp     = qFunc.getValue('qBusy_s_inp'    )
qBusy_s_wav     = qFunc.getValue('qBusy_s_wav'    )
qBusy_s_STT     = qFunc.getValue('qBusy_s_STT'    )
qBusy_s_TTS     = qFunc.getValue('qBusy_s_TTS'    )
qBusy_s_TRA     = qFunc.getValue('qBusy_s_TRA'    )
qBusy_s_play    = qFunc.getValue('qBusy_s_play'   )
qBusy_v_ctrl    = qFunc.getValue('qBusy_v_ctrl'   )
qBusy_v_inp     = qFunc.getValue('qBusy_v_inp'    )
qBusy_v_QR      = qFunc.getValue('qBusy_v_QR'     )
qBusy_v_jpg     = qFunc.getValue('qBusy_v_jpg'    )
qBusy_v_CV      = qFunc.getValue('qBusy_v_CV'     )
qBusy_d_ctrl    = qFunc.getValue('qBusy_d_ctrl'   )
qBusy_d_inp     = qFunc.getValue('qBusy_d_inp'    )
qBusy_d_QR      = qFunc.getValue('qBusy_d_QR'     )
qBusy_d_rec     = qFunc.getValue('qBusy_d_rec'    )
qBusy_d_play    = qFunc.getValue('qBusy_d_play'   )
qBusy_d_browser = qFunc.getValue('qBusy_d_browser')
qBusy_d_upload  = qFunc.getValue('qBusy_d_upload' )
qRdy__s_force   = qFunc.getValue('qRdy__s_force'  )
qRdy__s_fproc   = qFunc.getValue('qRdy__s_fproc'  )
qRdy__s_sendkey = qFunc.getValue('qRdy__s_sendkey')
qRdy__v_reader  = qFunc.getValue('qRdy__v_reader' )
qRdy__v_sendkey = qFunc.getValue('qRdy__v_sendkey')
qRdy__d_reader  = qFunc.getValue('qRdy__d_reader' )
qRdy__d_sendkey = qFunc.getValue('qRdy__d_sendkey')



if getattr(sys, 'frozen', False):
    #print('exe')
    google = False
else:
    #print('python')
    google = True

# debug
runMode     = 'handsfree'

if (google == True):
    qApiInp     = 'free'
    qApiTrn     = 'free'
    qApiOut     = qApiTrn
    if (qOS == 'windows'):
        qApiOut = 'winos'
else:
    qApiInp     = 'azure'
    qApiTrn     = 'azure'
    qApiOut     = qApiTrn
if (qOS == 'darwin'):
    qApiOut = 'macos'
qLangInp    = 'ja'
#qLangTrn    = 'en,fr,'
qLangTrn    = 'en'
qLangTxt    = qLangInp
qLangOut    = qLangTrn[:2]



# シグナル処理
import signal
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

    #runMode  debug, hud, handsfree, translator, speech, number, camera, background,

    # パラメータ

    if (True):

        #runMode     = 'handsfree'
        micDev      = '0'
        micType     = 'bluetooth'
        micGuide    = 'on'
        micLevel    = '777'

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        if   (runMode == 'debug'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        elif (runMode == 'hud'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'handsfree'):
            micType   = 'bluetooth'
            micGuide  = 'off'
        elif (runMode == 'translator'):
            micType   = 'bluetooth'
            micGuide  = 'on'
        elif (runMode == 'speech'):
            micType   = 'usb'
            micGuide  = 'on'
        elif (runMode == 'number'):
            micType   = 'usb'
            micGuide  = 'on'
        elif (runMode == 'camera'):
            micType   = 'usb'
            micGuide  = 'off'
        elif (runMode == 'background'):
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

        qFunc.remove(qCtrl_control_kernel    )
        qFunc.remove(qCtrl_control_speech    )
        qFunc.remove(qCtrl_control_vision    )
        qFunc.remove(qCtrl_control_desktop   )
        qFunc.remove(qCtrl_control_bgm       )
        qFunc.remove(qCtrl_control_browser   )
        qFunc.remove(qCtrl_control_player    )
        qFunc.remove(qCtrl_control_chatting  )
        qFunc.remove(qCtrl_control_knowledge )

        qFunc.statusReset_speech(False)
        qFunc.statusReset_vision(False)
        qFunc.statusReset_desktop(False)

        # 起動条件

        main_speech_run      = None
        main_speech_switch   = 'on'
        main_vision_run      = None
        main_vision_switch   = 'off'
        main_desktop_run     = None
        main_desktop_switch  = 'off'
        bgm_run              = None
        bgm_switch           = 'off'
        browser_run          = None
        browser_switch       = 'off'
        player_run           = None
        player_switch        = 'off'
        chatting_run         = None
        chatting_switch      = 'off'
        knowledge_run        = None
        knowledge_switch     = 'off'

        if   (runMode == 'debug'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (runMode == 'hud'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (runMode == 'handsfree'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'on'
            browser_switch       = 'on'
            player_switch        = 'on'
        elif (runMode == 'translator'):
            main_vision_switch   = 'off'
            main_desktop_switch  = 'off'
            bgm_switch           = 'off'
            browser_switch       = 'off'
            player_switch        = 'off'
        elif (runMode == 'speech'):
            main_vision_switch   = 'off'
            main_desktop_switch  = 'off'
            bgm_switch           = 'off'
            browser_switch       = 'off'
            player_switch        = 'off'
        elif (runMode == 'number'):
            main_vision_switch   = 'off'
            main_desktop_switch  = 'off'
            bgm_switch           = 'off'
            browser_switch       = 'off'
            player_switch        = 'off'
        elif (runMode == 'camera'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'off'
            browser_switch       = 'off'
            player_switch        = 'off'
        elif (runMode == 'background'):
            main_vision_switch   = 'on'
            main_desktop_switch  = 'on'
            bgm_switch           = 'off'
            browser_switch       = 'off'
            player_switch        = 'off'

    # 起動

    if (True):

        qFunc.logOutput(main_id + ':start')

    # 待機ループ

    onece = True
    last_alive = time.time()

    while (True):

        # 終了確認

        control = ''
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            qFunc.logOutput(main_id + ':' + str(txt))
            if (txt == '_end_'):
                break
            else:
                qFunc.remove(qCtrl_control_self)
                control = txt

        # リブート

        if (control == '_reboot_'):
            reboot_hit = False

            speechs = []
            speechs.append({ 'text':u'再起動処理を、開始しました。', 'wait':0, })
            qFunc.speech(id=main_id, speechs=speechs, lang='', )

            if (not main_desktop_run is None):
                qFunc.txtsWrite(qCtrl_control_desktop   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                reboot_hit = True
            if (not main_vision_run is None):
                qFunc.txtsWrite(qCtrl_control_vision    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                reboot_hit = True
            if (not main_speech_run is None):
                time.sleep(10.00)
                qFunc.txtsWrite(qCtrl_control_speech    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
                reboot_hit = True

            if (reboot_hit == True):
                time.sleep(10.00)
                if (not main_speech_run is None):
                    main_speech_run.wait()
                    main_speech_run.terminate()
                    main_speech_run = None
                if (not main_vision_run is None):
                    main_vision_run.wait()
                    main_vision_run.terminate()
                    main_vision_run = None
                if (not main_desktop_run is None):
                    main_desktop_run.wait()
                    main_desktop_run.terminate()
                    main_desktop_run = None

        # コントロール

        if (control == '_vision_begin_'):
            main_vision_switch   = 'on'
        if (control == '_vision_end_'):
            main_vision_switch   = 'off'
        if (control == '_desktop_begin_'):
            main_desktop_switch  = 'on'
        if (control == '_desktop_end_'):
            main_desktop_switch  = 'off'
        if (control == '_bgm_begin_'):
            bgm_switch           = 'on'
        if (control == '_bgm_end_') or (control == '_reboot_'):
            bgm_switch           = 'off'
        if (control == '_browser_begin_'):
            browser_switch       = 'on'
        if (control == '_browser_end_') or (control == '_reboot_'):
            browser_switch       = 'off'
        if (control == '_player_begin_'):
            player_switch        = 'on'
        if (control == '_player_end_') or (control == '_reboot_'):
            player_switch        = 'off'
        if (control == '_chatting_begin_'):
            chatting_switch      = 'on'
        if (control == '_chatting_end_') or (control == '_reboot_'):
            chatting_switch      = 'off'
        if (control == '_knowledge_begin_'):
            knowledge_switch     = 'on'
        if (control == '_knowledge_end_') or (control == '_reboot_'):
            knowledge_switch     = 'off'

        # 活動メッセージ

        if  ((time.time() - last_alive) > 30):
            qFunc.logOutput(main_id + ':alive')
            last_alive = time.time()

        # プロセス設定

        running = 'python'
        if getattr(sys, 'frozen', False):
            running = 'exe'

        speechs = []

        if (main_speech_run is None) and (main_speech_switch == 'on'):
            if (running == 'python'):
                main_speech_run = subprocess.Popen(['python', qPython_main_speech, 
                                runMode, micDev, micType, micGuide, micLevel,
                                qApiInp, qApiTrn, qApiOut,
                                qLangInp, qLangTrn, qLangTxt, qLangOut, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                main_speech_run = subprocess.Popen([qPython_main_speech[:-3], 
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

        if (not main_speech_run is None) and (main_speech_switch != 'on'):
            time.sleep(10.00)
            #main_speech_run.wait()
            main_speech_run.terminate()
            main_speech_run = None

        if (main_vision_run is None) and (main_vision_switch == 'on'):
            if (running == 'python'):
                main_vision_run = subprocess.Popen(['python', qPython_main_vision, 
                                runMode, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                main_vision_run = subprocess.Popen([qPython_main_vision[:-3],
                                runMode, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'カメラ機能を、起動しました。', 'wait':0, })

        if (not main_vision_run is None) and (main_vision_switch != 'on'):
            time.sleep(10.00)
            #main_vision_run.wait()
            main_vision_run.terminate()
            main_vision_run = None

            speechs.append({ 'text':u'カメラ機能を、終了しました。', 'wait':0, })

        if (main_desktop_run is None) and (main_desktop_switch == 'on'):
            if (running == 'python'):
                main_desktop_run = subprocess.Popen(['python', qPython_main_desktop, 
                                #'debug', ], )
                                runMode, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                main_desktop_run = subprocess.Popen([qPython_main_desktop[:-3], 
                                #'debug', ], )
                                runMode, ], )
                                #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'デスクトップ制御機能を、起動しました。', 'wait':0, })

        if (not main_desktop_run is None) and (main_desktop_switch != 'on'):
            time.sleep(10.00)
            #main_desktop_run.wait()
            main_desktop_run.terminate()
            main_desktop_run = None

            speechs.append({ 'text':u'デスクトップ制御機能を、終了しました。', 'wait':0, })

        if (bgm_run is None) and (bgm_switch == 'on'):
            if (running == 'python'):
                bgm_run = subprocess.Popen(['python', qPython_bgm, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                bgm_run = subprocess.Popen([qPython_bgm[:-3], runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ＢＧＭ再生機能を、起動しました。', 'wait':0, })

        if (not bgm_run is None) and (bgm_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_bgm, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #bgm_run.wait()
            bgm_run.terminate()
            bgm_run = None

            speechs.append({ 'text':u'ＢＧＭ再生機能を、終了しました。', 'wait':0, })

        if (browser_run is None) and (browser_switch == 'on'):
            if (running == 'python'):
                browser_run = subprocess.Popen(['python', qPython_browser, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                browser_run = subprocess.Popen([qPython_browser[:-3], runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ブラウザー連携機能を、起動しました。', 'wait':0, })

        if (not browser_run is None) and (browser_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_browser, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #browser_run.wait()
            browser_run.terminate()
            browser_run = None

            speechs.append({ 'text':u'ブラウザー連携機能を、終了しました。', 'wait':0, })

        if (player_run is None) and (player_switch == 'on'):
            if (running == 'python'):
                player_run = subprocess.Popen(['python', qPython_player, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                player_run = subprocess.Popen([qPython_player[:-3], runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'動画連携機能を、起動しました。', 'wait':0, })

        if (not player_run is None) and (player_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_player, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #player_run.wait()
            player_run.terminate()
            player_run = None

            speechs.append({ 'text':u'動画連携機能を、終了しました。', 'wait':0, })

        if (chatting_run is None) and (chatting_switch == 'on'):
            if (running == 'python'):
                chatting_run = subprocess.Popen(['python', qPython_chatting, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                chatting_run = subprocess.Popen([qPython_chatting[:-3], runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ドコモ雑談連携機能を、起動しました。', 'wait':0, })

        if (not chatting_run is None) and (chatting_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_chatting, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
            time.sleep(10.00)
            #chatting_run.wait()
            chatting_run.terminate()
            chatting_run = None

            speechs.append({ 'text':u'ドコモ雑談連携機能を、終了しました。', 'wait':0, })

        if (knowledge_run is None) and (knowledge_switch == 'on'):
            if (running == 'python'):
                knowledge_run = subprocess.Popen(['python', qPython_knowledge, runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            else:
                knowledge_run = subprocess.Popen([qPython_knowledge[:-3], runMode, ], )
                            #stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            speechs.append({ 'text':u'ドコモ知識データベースを、起動しました。', 'wait':0, })

        if (not knowledge_run is None) and (knowledge_switch != 'on'):
            qFunc.txtsWrite(qCtrl_control_knowledge, txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
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
        slow = False
        if (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.25)

    # 終了

    if (True):

        qFunc.logOutput(main_id + ':terminate')

        # プロセス終了

        qFunc.txtsWrite(qCtrl_control_kernel    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_speech    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_vision    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_desktop   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_bgm       ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_browser   ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_player    ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_chatting  ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        qFunc.txtsWrite(qCtrl_control_knowledge ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )
        
        #time.sleep(60.00)

        time.sleep(0.50)
        if (not main_speech_run is None):
            main_speech_run.wait()
            main_speech_run.terminate()
            main_speech_run = None

        time.sleep(0.50)
        if (not main_vision_run is None):
            main_vision_run.wait()
            main_vision_run.terminate()
            main_vision_run = None

        time.sleep(0.50)
        if (not main_desktop_run is None):
            main_desktop_run.wait()
            main_desktop_run.terminate()
            main_desktop_run = None

        time.sleep(0.50)
        if (not bgm_run is None):
            bgm_run.wait()
            bgm_run.terminate()
            bgm_run = None

        time.sleep(0.50)
        if (not browser_run is None):
            #browser_run.wait()
            browser_run.terminate()
            browser_run = None

        time.sleep(0.50)
        if (not player_run is None):
            #player_run.wait()
            player_run.terminate()
            player_run = None

        time.sleep(0.50)
        if (not chatting_run is None):
            #chatting_run.wait()
            chatting_run.terminate()
            chatting_run = None

        time.sleep(0.50)
        if (not knowledge_run is None):
            #knowledge_run.wait()
            knowledge_run.terminate()
            knowledge_run = None

        qFunc.logOutput(main_id + ':bye!')

        sys.exit(0)


