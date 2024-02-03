import psutil
import subprocess
import mcrcon
import time
import threading

server_address = "127.0.0.1"     # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.readline().rstrip('\r\n').rstrip('\n')  # パスワード
server_port = 25575              # ポート番号


pal_start = ("/home/deck/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 !!!MEMORY_LEAK_REBOOT_IS_SCHEDULED_IN_30_SECONDS!!!"


def start_server():
    print("[INFO]Initial Pal server start")

    while True:
        line = server_proc.stdout.readline().decode('utf8', 'replace')
        if line:
            print(f"[Server_log]{line}", end='')


server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
thread1 = threading.Thread(target=start_server,)  # サーバーの標準出力を出すスレッドを作成
thread1.start()  # サーバーの標準出力を出すスレッドを実行

counter = 0
print("[INFO]Start loop for check mem percent")
while True:
    mem = psutil.virtual_memory()

    if mem.percent > 95:
        print(f"[ERROR]Server mem allocation is too high! mem={mem.percent}%")

        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)
            # server_proc.terminate()
        time.sleep(10)
        print("[INFO]sleep 10s")
        time.sleep(10)
        print("[INFO]sleep 20s")
        time.sleep(10)
        print("[INFO]sleep 30s")
        time.sleep(10)
        print("[INFO]sleep 40s")
        time.sleep(10)
        print("[INFO]sleep 50s")
        time.sleep(10)
        print("[INFO]sleep 60s end sleep")
        print("[INFO]Reboot Pal server start")
        server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        counter = 0
    else:
        if counter >= 20:
            print(f"[CHECK]Server mem={mem.percent}%")
            counter = 0
    counter += 1
    time.sleep(3)

