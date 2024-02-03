import psutil
import subprocess
import mcrcon
import time
import threading

server_address = "127.0.0.1"  # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.read()  # パスワード
server_port="25575"           # ポート番号


pal_start = ("/home/deck/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 メモリ使用量が90%を超えたためサーバが30秒後に終了します。"
print("Initial Pal server start")
server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def get_lines(proc):
    while True:
        line = proc.stdout.readline()
        if line:
            print(f"[Server_log]{line}")

        if not line and proc.poll() is not None:
            break


thread1 = threading.Thread(target=get_lines,
                               args=(server_proc,))  # ytdlのスレッドを作成 ダウンロードに時間かかるときにBotが死ぬため
thread1.start()  # ytdlのスレッドを実行

counter = 0
print("Start loop for check mem percent")
while True:
    mem = psutil.virtual_memory()
    # get_lines(server_proc)

    if mem.percent > 90:
        counter += 1
        print(f"[ERROR]Server mem allocation is too high! mem={mem.percent}%")
        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)
            time.sleep(10)
            # server_proc.terminate()
        print("[INFO]Reboot Pal server start")
        server_proc = subprocess.run(pal_start, shell=True)
    else:
        if counter >= 20:
            print(f"[CHECK]Server mem={mem.percent}%")
            counter = 0
    time.sleep(3)

