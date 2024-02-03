import psutil
import subprocess
import mcrcon
import time
import threading

server_address = "127.0.0.1"     # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.read()  # パスワード
server_port = 25575              # ポート番号


pal_start = ("/home/deck/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 メモリ使用量が90%を超えたためサーバが30秒後に終了します。"


def start_server(proc):
    print("[INFO]Initial Pal server start")

    while True:
        line = proc.stdout.readline().decode('utf8', 'replace')
        if line:
            print(f"[Server_log]{line}", end='')

        if not line and proc.poll() is not None:
            break


proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
thread1 = threading.Thread(target=start_server, args=(proc,),)  # ytdlのスレッドを作成 ダウンロードに時間かかるときにBotが死ぬため
thread1.start()  # ytdlのスレッドを実行

counter = 0
print("[INFO]Start loop for check mem percent")
while True:
    mem = psutil.virtual_memory()

    if mem.percent > 90:
        print(f"[ERROR]Server mem allocation is too high! mem={mem.percent}%")

        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)
            # server_proc.terminate()
        time.sleep(10)
        print("[INFO]Reboot Pal server start")
        server_proc = subprocess.run(pal_start, shell=True)
    else:
        if counter >= 20:
            print(f"[CHECK]Server mem={mem.percent}%")
            counter = 0
    counter += 1
    time.sleep(3)

