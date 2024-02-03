import psutil
import subprocess
import mcrcon                 # mcrconのインポート
import time

server_address = "127.0.0.1"  # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.read()  # youtube playerの音量
server_port="25575"           # ポート番号
counter = 0

pal_start = ("screen -S pal /home/deck/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 メモリ使用量が90%を超えたためサーバが30秒後に終了します。"
print("Initial Pal server start")
server_proc = subprocess.run(pal_start, shell=True)

print("Start loop for check mem percent")
while True:
    mem = psutil.virtual_memory()
    if mem > 90:
        counter += 1
        print(f"Server mem allocation is too high! mem={mem}%")
        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)
            time.sleep(10)
            # server_proc.terminate()
        print("Reboot Pal server start")
        server_proc = subprocess.run(pal_start, shell=True)
    else:
        if counter >= 20:
            print(f"Server mem={mem}%")
            counter = 0
    time.sleep(3)

