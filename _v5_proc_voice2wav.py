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



class proc_voice2wav:

    def __init__(self, name='thread', id='0', runMode='debug', 
        micDev='0', micType='bluetooth', micGuide='on', micLevel='777', ):

        self.path      = qPath_a_inp

        self.runMode   = runMode
        self.micDev    = micDev
        self.micType   = micType
        self.micGuide  = micGuide
        self.micLevel  = micLevel

        self.minSize   =  10000
        self.maxSize   = 384000

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_{:01}'.format(int(id))
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qFunc.logOutput(self.proc_id + ':init', display=self.logDisp, )

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

    def __del__(self, ):
        qFunc.logOutput(self.proc_id + ':bye!', display=self.logDisp, )

    def start(self, ):
        #qFunc.logOutput(self.proc_id + ':start')

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ))
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0

        self.proc_main.setDaemon(True)
        self.proc_main.start()

    def stop(self, waitMax=5, ):
        qFunc.logOutput(self.proc_id + ':stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (not self.proc_beat is None) or (int(time.time() - chktime) < waitMax):
            time.sleep(0.10)

    def put(self, data, ):
        self.proc_s.put(data)        
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and (int(time.time() - chktime) < waitMax):
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
        qFunc.logOutput(self.proc_id + ':start', display=self.logDisp, )
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        fileRdy = qPath_work + self.proc_id + '.rdy'
        fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.remove(fileRdy)
        qFunc.remove(fileBsy)

        # 待機ループ
        self.proc_step = '5'

        check_file = ''
        check_size = 0
        check_time = time.time()

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

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
                qFunc.logOutput(self.proc_id + ':queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディ設定
            if (not os.path.exists(fileRdy)):
                qFunc.txtsWrite(fileRdy, txts=['ready'], encoding='utf-8', exclusive=False, mode='a', )

            # ステータス応答
            if (inp_name.lower() == 'status'):
                out_name  = inp_name
                out_value = 'ready'
                cn_s.put([out_name, out_value])



            # 処理
            path = self.path
            path_files = glob.glob(path + '*')
            if (len(path_files) > 0):

                #try:
                if (True):

                    base_byte  = 0
                    file_count = 0
                    for f in path_files:
                        file_count += 1

                        # 停止要求確認
                        if (self.breakFlag.is_set()):
                            self.breakFlag.clear()
                            self.proc_step = '9'
                            break

                        proc_file = f.replace('\\', '/')

                        # 書込み途中チェック
                        if (os.name != 'nt'):
                            if (len(path_files) == file_count):

                                # ファイルサイズ
                                proc_size = 0
                                try:
                                    rb = open(proc_file, 'rb')
                                    proc_size = sys.getsizeof(rb.read())
                                    rb.close
                                    rb = None
                                except:
                                    rb = None

                                # 変化？
                                if (proc_file != check_file) \
                                or (proc_size != check_size):
                                    check_file = proc_file
                                    check_size = proc_size
                                    check_time = time.time()
                                    break
                                else:
                                    # 変化なしでn秒経過？
                                    if ((time.time() - check_time)<0.50):
                                        break

                        if (proc_file[-4:].lower() == '.wav' and proc_file[-8:].lower() != '.wrk.wav'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.wav'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass
                        if (proc_file[-4:].lower() == '.mp3' and proc_file[-8:].lower() != '.wrk.mp3'):
                            f1 = proc_file
                            f2 = proc_file[:-4] + '.wrk.mp3'
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass

                        if (proc_file[-8:].lower() == '.wrk.wav' or proc_file[-8:].lower() == '.wrk.mp3'):
                            f1 = proc_file
                            f2 = proc_file[:-8] + proc_file[-4:]
                            try:
                                os.rename(f1, f2)
                                proc_file = f2
                            except:
                                pass

                            # 実行カウンタ
                            self.proc_last = time.time()
                            self.proc_seq += 1
                            if (self.proc_seq > 9999):
                                self.proc_seq = 1
                            seq4 = '{:04}'.format(self.proc_seq)
                            seq2 = '{:02}'.format(self.proc_seq)

                            proc_name = proc_file.replace(path, '')
                            proc_name = proc_name[:-4]

                            work_name = self.proc_id + '.' + seq2
                            work_file = qPath_work + work_name + '.wav'
                            if (os.path.exists(work_file)):
                                os.remove(work_file)

                            sox = subprocess.Popen(['sox', '-q', proc_file, '-r', '16000', '-b', '16', '-c', '1', work_file, ], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None

                            if (os.path.exists(work_file)):

                                if (self.micDev.isdigit()):
                                    os.remove(proc_file)

                                # ログ
                                if (self.runMode == 'debug') or (not self.micDev.isdigit()):
                                    qFunc.logOutput(self.proc_id + ':' + proc_name + u' → ' + work_name, display=self.logDisp,)

                                # ビジー設定
                                if (not os.path.exists(fileBsy)):
                                    qFunc.txtsWrite(fileBsy, txts=['busy'], encoding='utf-8', exclusive=False, mode='a', )
                                    if (str(self.id) == '0'):
                                        qFunc.busySet(qBusy_a_wav, True)

                                # ファイルサイズ
                                work_size = 0
                                try:
                                    rb = open(work_file, 'rb')
                                    work_size = sys.getsizeof(rb.read())
                                    rb.close
                                    rb = None
                                except:
                                    rb = None

                                # ファイル分割処理
                                self.proc_last = time.time()
                                self.sub_proc(seq4, proc_file, work_file, proc_name, work_size, base_byte, cn_s, )

                                if (not self.micDev.isdigit()):
                                    base_byte += work_size - 44

                                time.sleep(1.00)
                    
                #except:
                #    pass



            # ビジー解除
            qFunc.remove(fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_a_wav, False)

            # バッチ実行時は終了
            if (not self.micDev.isdigit()):
                break

            # アイドリング
            if (qFunc.busyCheck(qBusy_dev_cpu, 0) == 'busy') \
            or (qFunc.busyCheck(qBusy_dev_mic, 0) == 'busy'):
                time.sleep(1.00)
            if (cn_r.qsize() == 0):
                time.sleep(0.25)
            else:
                time.sleep(0.05)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.remove(fileRdy)

            # ビジー解除
            qFunc.remove(fileBsy)
            if (str(self.id) == '0'):
                qFunc.busySet(qBusy_a_wav, False)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qFunc.logOutput(self.proc_id + ':end', display=self.logDisp, )
            self.proc_beat = None



    def sub_proc(self, seq4, proc_file, work_file, proc_name, work_size, base_byte, cn_s, ):

        path = qPath_a_wav
        nowTime = datetime.datetime.now()
        stamp   = nowTime.strftime('%Y%m%d.%H%M%S')

        if (work_size >= int(self.minSize) and work_size <= int(self.maxSize+2000)):

                    if (self.micDev.isdigit()):
                        sec=int((work_size-44)/2/16000)
                    else:
                        sec=int(base_byte/2/16000)

                    hh = int(sec/3600)
                    mm = int((sec-hh*3600)/60)
                    ss = int(sec-hh*3600-mm*60)
                    tm = '{:02}{:02}{:02}'.format(hh,mm,ss)

                    fwork = path        + stamp + '.' + proc_name + '(000).' + tm + '.wav'
                    fjuli = qPath_a_jul + stamp + '.' + proc_name + '(000).' + tm + '.wav'
                    frec  = qPath_rec   + stamp + '.' + proc_name + '(000).' + tm + '.mp3'

                    try:
                        shutil.copy2(work_file, fwork)
                        shutil.copy2(work_file, fjuli)
                        if (self.micDev.isdigit()):
                            sox  = subprocess.Popen(['sox', '-q', work_file, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None

                        # 結果出力
                        if (cn_s.qsize() < 99):
                            out_name  = 'filename'
                            out_value = fjuli
                            cn_s.put([out_name, out_value])

                    except:
                        pass

        if (work_size > int(self.maxSize+2000)):

            sep_sec = int(self.maxSize/2/16000 - 1)

            nn = 1
            while (nn != 0):

                ftrim = work_file[:-4] + '.trim.wav'
                sox = subprocess.Popen(['sox', '-q', work_file, '-r', '16000', '-b', '16', '-c', '1', ftrim, 'trim', str((nn-1)*sep_sec), str(sep_sec+1), ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                sox.wait()
                sox.terminate()
                sox = None

                ftrim_size = 0
                try:
                    rb = open(ftrim, 'rb')
                    ftrim_size = sys.getsizeof(rb.read())
                    rb.close
                    rb = None
                except:
                    rb = None

                if (ftrim_size < int(self.minSize)):
                    os.remove(ftrim)
                    nn = 0
                else:

                    if (self.micDev.isdigit()):
                        sec = int((ftrim_size-44)/2/16000)
                    else:
                        sec = int(base_byte/2/16000) + (nn-1)*sep_sec

                    hh = int(sec/3600)
                    mm = int((sec-hh*3600)/60)
                    ss = int(sec-hh*3600-mm*60)
                    tm = '{:02}{:02}{:02}'.format(hh,mm,ss)

                    fwork = path        + stamp + '.' + proc_name + '(' + '{:03}'.format(nn) + ').' + tm + '.wav'
                    fjuli = qPath_a_jul + stamp + '.' + proc_name + '(' + '{:03}'.format(nn) + ').' + tm + '.wav'
                    frec  = qPath_rec   + stamp + '.' + proc_name + '(' + '{:03}'.format(nn) + ').' + tm + '.mp3'

                    try:
                        shutil.copy2(ftrim, fwork)
                        shutil.copy2(ftrim, fjuli)
                        if (self.micDev.isdigit()):
                            sox  = subprocess.Popen(['sox', '-q', ftrim, '-r', '16000', '-b', '16', '-c', '1', frec, ], \
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                            sox.wait()
                            sox.terminate()
                            sox = None

                        # 結果出力
                        if (cn_s.qsize() < 99):
                            out_name  = 'filename'
                            out_value = fjuli
                            cn_s.put([out_name, out_value])

                    except:
                        pass

                    nn += 1



if __name__ == '__main__':
    # 共通クラス
    qFunc.init()

    # ログ設定
    qNowTime = datetime.datetime.now()
    qLogFile = qPath_log + qNowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qFunc.logFileSet(file=qLogFile, display=True, outfile=True, )
    qFunc.logOutput(qLogFile, )



    voice2wav_thread = proc_voice2wav('voice2wav', '0', )
    voice2wav_thread.start()

    chktime = time.time()
    while (int(time.time() - chktime) < 15):

        res_data  = voice2wav_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            print(res_name, res_value, )

        if (voice2wav_thread.proc_s.qsize() == 0):
            voice2wav_thread.put(['status', ''])

        time.sleep(0.05)

    time.sleep(1.00)
    voice2wav_thread.stop()
    del voice2wav_thread


