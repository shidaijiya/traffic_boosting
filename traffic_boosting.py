import requests
import threading
import time

class DownloadStats:
    def __init__(self):
        self.downloaded_bytes = 0
        self.start_time = time.time()
        self.last_print_time = self.start_time

    def update(self, chunk_size):
        self.downloaded_bytes += chunk_size
        current_time = time.time()
        if current_time - self.last_print_time >= 1:
            download_speed = self.downloaded_bytes / (current_time - self.last_print_time)
            download_speed_mbps = (download_speed * 8) / (1024 * 1024)  # 将下载速度转换为 Mbps
            print(f"下载速度 {download_speed_mbps:.2f} Mbps")
            self.last_print_time = current_time
            self.downloaded_bytes = 0

def download_file(url, stats):
    try:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                stats.update(len(chunk))
    except Exception as e:
        print(f"下载文件失败：{e}")

def consume_bandwidth(urls, max_threads):
    stats = DownloadStats()

    def worker(url):
        download_file(url, stats)

    threads = []
    for url in urls:
        for _ in range(max_threads):
            t = threading.Thread(target=worker, args=(url,))
            t.daemon = True
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    urls = [
        "https://cn.download.nvidia.cn/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://us.download.nvidia.com/RTX/NVIDIA_ChatWithRTX_Demo.zip",
        "https://tw.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://jp.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
    ]
    max_threads = 32
    consume_bandwidth(urls, max_threads)
