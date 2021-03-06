#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import datetime
import codecs
import glob

import queue
import threading
import subprocess

#print(os.path.dirname(__file__))
#print(os.path.basename(__file__))
#print(sys.version_info)



# インターフェース
qCtrl_control_bgm        = 'temp/control_bgm.txt'
qCtrl_control_self       = qCtrl_control_bgm



# qLog,qFunc 共通ルーチン
import  _v5__qLog
qLog  = _v5__qLog.qLog_class()
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()

qPLATFORM       = qFunc.getValue('qPLATFORM'      )
qRUNATTR        = qFunc.getValue('qRUNATTR'       )
qHOSTNAME       = qFunc.getValue('qHOSTNAME'      )
qUSERNAME       = qFunc.getValue('qUSERNAME'      )
qPath_pictures  = qFunc.getValue('qPath_pictures' )
qPath_videos    = qFunc.getValue('qPath_videos'   )
qPath_cache     = qFunc.getValue('qPath_cache'    )
qPath_sounds    = qFunc.getValue('qPath_sounds'   )
qPath_icons     = qFunc.getValue('qPath_icons'    )
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



runMode = 'debug'



class main_bgm:

    def __init__(self, name='thread', id='0', runMode='debug', ):
        self.runMode   = runMode

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_' + str(id)
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qLog.log('info', self.proc_id, 'init', display=self.logDisp, )

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

        self.bgm_id    = None 
        self.bgm_start = time.time() 
        self.bgm_file  = ''
        self.bgm_parm  = ''
        self.bgm_name  = ''

    def __del__(self, ):
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        #qLog.log('info', self.proc_id, 'start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.statusSet(self.fileRun, False)
        qFunc.statusSet(self.fileRdy, False)
        qFunc.statusSet(self.fileBsy, False)

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ))
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0

        self.proc_main.setDaemon(True)
        self.proc_main.start()

    def abort(self, waitMax=5, ):
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (not self.proc_beat is None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)
        chktime = time.time()
        while (os.path.exists(self.fileRun)) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)

    def put(self, data, ):
        self.proc_s.put(data)
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and ((time.time() - chktime) < waitMax):
            time.sleep(0.10)
        data = self.get()
        return data

    def get(self, ):
        if (self.proc_r.qsize() == 0):
            return ['', '']
        data = self.proc_r.get()
        self.proc_r.task_done()
        return data

    def main_proc(self, cn_r, cn_s, ):
        # ログ
        qLog.log('info', self.proc_id, 'start', display=self.logDisp, )
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

        # 待機ループ
        self.proc_step = '5'

        onece = True
        last_alive = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 終了確認
            control = ''
            txts, txt = qFunc.txtsRead(qCtrl_control_self)
            if (txts != False):
                qLog.log('info', self.proc_id, '' + str(txt))
                if (txt == '_end_'):
                    break
                else:
                    qFunc.remove(qCtrl_control_self)
                    control = txt

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # 活動メッセージ
            if  ((time.time() - last_alive) > 30):
                qLog.log('debug', self.proc_id, 'alive', display=True, )
                last_alive = time.time()

            # キュー取得
            if (cn_r.qsize() > 0):
                cn_r_get  = cn_r.get()
                inp_name  = cn_r_get[0]
                inp_value = cn_r_get[1]
                cn_r.task_done()
            else:
                inp_name  = ''
                inp_value = ''

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 20):
                qLog.log('warning', self.proc_id, 'queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディー設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                out_value = '_ready_'
                cn_s.put([out_name, out_value])

            # ＢＧＭアナウンス
            if (self.bgm_id is None):
                if ((time.time() - self.bgm_start) > 120):
                    if (onece == True):
                        onece = False

                        if (self.runMode == 'debug') \
                        or (self.runMode == 'live'):
                            speechs = []
                            speechs.append({ 'text':u'プレイリストの再生はいかがですか？', 'wait':0, })
                            qFunc.speech(id='speech', speechs=speechs, lang='', )

            # 処理
            if (control != ''):
                self.sub_proc(control, )

            # アイドリング
            slow = False
            if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            elif (qFunc.statusCheck(qBusy_dev_mic) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                if (cn_r.qsize() == 0):
                    time.sleep(0.50)
                else:
                    time.sleep(0.25)

        # 終了処理
        if (True):

            # レディー解除
            qFunc.statusSet(self.fileRdy, False)

            # 停止
            if (not self.bgm_id is None):
                self.sub_proc('_stop_', )

            # ビジー解除
            qFunc.statusSet(self.fileBsy, False)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



    # 処理
    def sub_proc(self, proc_text, ):

        if (proc_text.find(u'リセット') >=0):

            # 停止
            if (not self.bgm_id is None):
                #self.sub_stop(proc_text, )
                self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_stop_') \
          or (proc_text.find(u'BGM') >=0)   and (proc_text.find(u'停止') >=0) \
          or (proc_text.find(u'BGM') >=0)   and (proc_text.find(u'終了') >=0) \
          or (proc_text.find(u'ＢＧＭ') >=0) and (proc_text.find(u'停止') >=0) \
          or (proc_text.find(u'ＢＧＭ') >=0) and (proc_text.find(u'終了') >=0):

            # 停止
            if (not self.bgm_id is None):
                #self.sub_stop(proc_text, )
                self.sub_stop('_stop_', )

        elif (proc_text.lower() == '_start_') \
          or (proc_text.find(u'BGM') >=0)   and (proc_text.find(u'開始') >=0) \
          or (proc_text.find(u'BGM') >=0)   and (proc_text.find(u'再生') >=0) \
          or (proc_text.find(u'ＢＧＭ') >=0) and (proc_text.find(u'開始') >=0) \
          or (proc_text.find(u'ＢＧＭ') >=0) and (proc_text.find(u'再生') >=0):

            # 停止
            if (not self.bgm_id is None):
                #self.sub_stop(proc_text, )
                self.sub_stop('_stop_', )

            # 開始
            self.sub_start('_start_', )

        else:

            txt = proc_text.lower()
            procBgm = ''

            if (txt == 'playlist 00'  ) or (txt == 'playlist 0') \
            or (txt == 'playlist zero') \
            or (txt == 'bgm') or (txt == 'garageband'):
                procBgm =  '_00_'

            if (txt == 'playlist 01' ) or (txt == 'playlist 1') \
            or (txt == 'playlist etc') or (txt == 'playlists etc'):
                procBgm =  '_01_'

            if (txt == 'playlist 02') or (txt == 'playlist 2') \
            or (txt == 'babymetal'):
                procBgm =  '_02_'

            if (txt == 'playlist 03') or (txt == 'playlist 3') \
            or (txt == 'perfume'):
                procBgm =  '_03_'

            if (txt == 'playlist 04') or (txt == 'playlist 4') \
            or (txt == 'kyary pamyu pamyu'):
                procBgm =  '_04_'

            if (txt == 'playlist 05') or (txt == 'playlist 5') \
            or (txt == 'one ok rock') or (txt == 'one ok'):
                procBgm =  '_05_'

            if (txt == 'playlist 06') or (txt == 'playlist 6') \
            or (txt == 'the end of the world') or (txt == 'end of the world'):
                procBgm =  '_06_'

            if (txt == 'playlist') or (txt == 'playlist list') \
            or (txt == 'list of playlists') or (txt == 'bgm list'):

                speechs = []
                speechs.append({ 'text':u'プレイリストゼロは、自作ＢＧＭです。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト１は、お気に入り音楽です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト２は、「BABYMETAL」です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト３は、「perfume」です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト４は、「きゃりーぱみゅぱみゅ」です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト５は、「ONE OK ROCK」です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリスト６は、「SEKAI NO OWARI」です。', 'wait':0, })
                speechs.append({ 'text':u'プレイリストを再生しますか？', 'wait':0, })
                qFunc.speech(id='speech', speechs=speechs, lang='', )

            if (procBgm != ''):

                # 停止
                if (not self.bgm_id is None):
                    #self.sub_stop(proc_text, )
                    self.sub_stop('_stop_', )

                # 開始
                self.sub_start(procBgm, )



    # 開始
    def sub_start(self, proc_text, ):

        # ファイル
        self.bgm_file = ''
        self.bgm_parm = ''
        self.bgm_name = ''

        if (proc_text.lower() == '_start_') \
        or (proc_text.lower() == 'bgm') \
        or (proc_text.lower() == '_00_'):
            self.bgm_file = u'_VLC_GB_プレイリスト.xspf'
            self.bgm_parm = '--qt-start-minimized'

        elif (proc_text.lower() == '_01_'):
            self.bgm_file = u'_VLC_etc_プレイリスト.xspf'

        elif (proc_text.lower() == '_02_'):
            self.bgm_file = u'_VLC_BABYMETAL_プレイリスト.xspf'

        elif (proc_text.lower() == '_03_'):
            self.bgm_file = u'_VLC_Perfume_プレイリスト.xspf'

        elif (proc_text.lower() == '_04_'):
            self.bgm_file = u'_VLC_きゃりーぱみゅぱみゅ_プレイリスト.xspf'

        elif (proc_text.lower() == '_05_'):
            self.bgm_file = u'_VLC_ワンオク_プレイリスト.xspf'

        elif (proc_text.lower() == '_06_'):
            self.bgm_file = u'_VLC_セカオワ_プレイリスト.xspf'

        if (self.bgm_file != ''):
            if (os.name == 'nt'):
                self.bgm_name = u'C:\\Users\\Public\\' + self.bgm_file
            else:
                self.bgm_name = u'/users/kondou/Documents/' + self.bgm_file

        # 開始
        if (self.bgm_file != ''):

            # ビジー設定
            if (qFunc.statusCheck(self.fileBsy) == False):
                qFunc.statusSet(self.fileBsy, True)

            try:
                if (os.name == 'nt'):
                    if (self.bgm_parm != ''):
                        self.bgm_id = subprocess.Popen(['VLC', self.bgm_parm, self.bgm_name, ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        self.bgm_start = time.time()
                    else:
                        self.bgm_id = subprocess.Popen(['VLC', self.bgm_name, ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        self.bgm_start = time.time()

                else:
                    if (self.bgm_parm != ''):
                        self.bgm_id = subprocess.Popen(['open', '-a', 'VLC', self.bgm_name, ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        self.bgm_start = time.time()
                    else:
                        self.bgm_id = subprocess.Popen(['open', '-a', 'VLC', self.bgm_name, ], \
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                        self.bgm_start = time.time()
            except Exception as e:
                pass

            # ログ
            qLog.log('info', self.proc_id, '' + u'play ' + self.bgm_file + ' start', display=True,)

    # 停止
    def sub_stop(self, proc_text, ):

        if (not self.bgm_id is None):

            # 停止
            self.bgm_id.terminate()
            self.bgm_id = None

            # ログ
            qLog.log('info', self.proc_id, '' + u'play ' + self.bgm_file + ' stop', display=True,)

        # リセット
        qFunc.kill('VLC', )

        # ビジー解除
        qFunc.statusSet(self.fileBsy, False)



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



if __name__ == '__main__':
    main_name = 'bgm'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # 共通クラス
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, ')

    # パラメータ

    if (True):

        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()

        qLog.log('info', main_id, 'runMode  =' + str(runMode  ))

    # 初期設定

    if (True):

        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                qFunc.remove(qCtrl_control_self)

    # 起動

    if (True):

        qLog.log('info', main_id, 'start')

        main_core = main_bgm(main_name, '0', runMode=runMode, )
        main_core.begin()

        main_start = time.time()
        onece      = True

    # 待機ループ

    while (True):

        # 終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if (txts != False):
            if (txt == '_end_'):
                break

        # デバッグ
        if (runMode == 'debug'):

            # テスト開始
            if  ((time.time() - main_start) > 1):
                if (onece == True):
                    onece = False
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_start_'], encoding='utf-8', exclusive=True, mode='w', )

            # テスト終了
            if  ((time.time() - main_start) > 30):
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_stop_'], encoding='utf-8', exclusive=True, mode='w', )
                    time.sleep(5.00)
                    qFunc.txtsWrite(qCtrl_control_self ,txts=['_end_'], encoding='utf-8', exclusive=True, mode='w', )

        # アイドリング
        slow = False
        if   (qFunc.statusCheck(qBusy_dev_cpu) == True):
            slow = True
        elif (qFunc.statusCheck(qBusy_dev_mic) == True):
            slow = True

        if (slow == True):
            time.sleep(1.00)
        else:
            time.sleep(0.50)

    # 終了

    if (True):

        qLog.log('info', main_id, 'terminate')

        main_core.abort()
        del main_core

        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


