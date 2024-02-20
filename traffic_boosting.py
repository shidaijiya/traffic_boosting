import requests
import threading
import time

class DownloadStats:
    def __init__(self):
        self.downloaded_bytes = 0
        self.start_time = time.time()
        self.last_print_time = self.start_time

    def update(self, chunk_size):
        # 更新已下载字节数
        self.downloaded_bytes += chunk_size
        current_time = time.time()
        # 如果距离上次打印下载速度已经过去了 1 秒，则打印当前下载速度
        if current_time - self.last_print_time >= 1:
            download_speed = self.downloaded_bytes / (current_time - self.last_print_time)
            download_speed_mbps = (download_speed * 8) / (1024 * 1024)  # 将下载速度转换为 Mbps
            print(f"下载速度 {download_speed_mbps:.2f} Mbps")
            self.last_print_time = current_time
            self.downloaded_bytes = 0

def download_file(url, stats):
    try:
        # 发送 GET 请求下载文件
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                # 更新下载统计信息
                stats.update(len(chunk))
    except Exception as e:
        # 如果下载失败，打印错误信息
        print(f"下载文件失败：{e}")

def worker(url, stats, semaphore):
    # 每个工作线程的执行函数，下载指定的文件并更新下载统计信息
    download_file(url, stats)
    semaphore.release()  # 释放信号量，表示线程执行完毕

def consume_bandwidth(urls, max_threads):
    stats = DownloadStats()

    # 创建一个信号量来限制并发线程数
    semaphore = threading.Semaphore(max_threads)

    def create_worker(url):
        # 创建一个工作线程，并使用信号量限制并发数
        with semaphore:
            t = threading.Thread(target=worker, args=(url, stats, semaphore))
            t.daemon = True
            t.start()
            return t

    # 创建并启动所有工作线程
    threads = [create_worker(url) for url in urls]

    # 等待所有工作线程结束
    for t in threads:
        t.join()

if __name__ == "__main__":
    # 要下载的文件链接列表
    urls = [
        "https://cn.download.nvidia.cn/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://us.download.nvidia.com/RTX/NVIDIA_ChatWithRTX_Demo.zip",
        "https://tw.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://jp.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
    ]
    max_threads = 16  # 最大并发线程数
    while True:
        consume_bandwidth(urls, max_threads)

