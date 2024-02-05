import psutil
import subprocess
import mcrcon
import time
import threading


server_address = "127.0.0.1"     # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.readline().rstrip('\r\n').rstrip('\n')  # パスワード
server_port = 25575              # ポート番号


pal_start = ("~/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 !!!MEMORY_LEAK_REBOOT_IS_SCHEDULED_IN_30_SECONDS!!!"
pal_say = "Broadcast !!!Server_is_shutdown_in_10_seconds!!!"

def log_output():
    while True:
        line = server_proc.stdout.readline().decode('utf8', 'replace')
        if line:
            print(f"[Server_log]{line}", end='')

print("[INFO]Initial Pal server start")
server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
thread1 = threading.Thread(target=log_output,)  # サーバーの標準出力を出すスレッドを作成
thread1.start()  # サーバーの標準出力を出すスレッドを実行

counter = 0
wait_time = 5   # サーバ再起時間　4以上を設定すること
print("[INFO]Start loop for check mem percent")
while True:
    virtual_mem_total = psutil.virtual_memory().total
    virtual_mem_free = psutil.virtual_memory().free
    swap_mem_total = psutil.swap_memory().total
    swap_mem_free = psutil.swap_memory().free

    mem_total = virtual_mem_total + swap_mem_total
    mem_free = virtual_mem_free + swap_mem_free
    mem_percent = ((mem_total - mem_free)/mem_total)*100
    # mem = psutil.virtual_memory()

    if mem_percent > 95:
        print(f"[ERROR]Server mem allocation is too high! mem={mem_percent}%")

        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)
            # server_proc.terminate()
        for i in range(wait_time):
            time.sleep(10)
            sec_wait = str((i+1)*10)
            if i <= wait_time-2:
                print(f"[INFO]sleep {sec_wait}s")
            else:
                print(f"[INFO]sleep {sec_wait}s end sleeping")
            if i == 1:
                with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
                    log = mcr.command("Save")
                    print(log)
                with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
                    log = mcr.command(pal_say)
                    print(log)
        print("[INFO]Reboot Pal server start")
        server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        counter = 0
    else:
        if counter >= 20:
            print(f"[CHECK]Server mem={mem_percent}%")
            counter = 0
    counter += 1
    time.sleep(3)

