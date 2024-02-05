import psutil
import subprocess
import mcrcon
import time
import threading
import io

server_address = "127.0.0.1"     # マルチプレイするときに入れるアドレス
with open('./pass.txt', 'r') as passwd:  # apss.txtからパスワードを読み取る
    server_pass = passwd.readline().rstrip('\r\n').rstrip('\n')  # パスワード
server_port = 25575              # ポート番号


pal_start = ("~/Desktop/steamcmd/palworld/PalServer.sh "
              "-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS")
pal_stop = "Shutdown 30 !!!MEMORY_LEAK_REBOOT_IS_SCHEDULED_IN_30_SECONDS!!!"
pal_before_10_sec = "Broadcast !!!Server_will_shutdown_in_10_seconds!!!"


def log_output():
    with io.open(server_proc.stdout.fileno(), closefd=False) as stream:
        [print('[Server_log]'+line.rstrip('\n')) for line in stream]


print("[INFO]Initial Pal server start")
server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
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

    if mem_percent > 95:
        print(f"[ERROR]Server mem allocation is too high! mem={mem_percent}%")

        with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
            log = mcr.command(pal_stop)
            print(log)

        for waiting_time in range(wait_time):
            time.sleep(10)
            sec_wait = str((waiting_time+1)*10)
            if waiting_time <= wait_time-2:
                print(f"[INFO]sleep {sec_wait}s")
            else:
                print(f"[INFO]sleep {sec_wait}s end sleeping")
            if waiting_time == 1:
                with mcrcon.MCRcon(server_address, server_pass, server_port) as mcr:
                    log_save = mcr.command("Save")
                    print(log_save)
                    for i_say10 in range(3):
                        log_10say = mcr.command(pal_before_10_sec)
                        print(log_10say)
        print("[INFO]Reboot Pal server start")
        server_proc = subprocess.Popen(pal_start, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       bufsize=-1)
        counter = 0
    else:
        if counter >= 20:
            print(f"[CHECK]Server mem={mem_percent}%")
            counter = 0
    counter += 1
    time.sleep(3)

