# traffic_boosting（带宽消耗器）
因为我宽带钱了，所以我要在闲暇之余跑满所有的带宽，让运营商亏的血本无归！！！
## 如何修改参数

更改列表内的链接网速越快建议添加越多，我这里就用nvidia的中国，美国，中国台湾，日本官网的下载链接，平均每个单跑可以50Mb/s 我这里4个相信可以跑满大部分

``` python
urls = [
        "https://cn.download.nvidia.cn/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://us.download.nvidia.com/RTX/NVIDIA_ChatWithRTX_Demo.zip",
        "https://tw.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
        "https://jp.download.nvidia.com/Windows/551.52/551.52-desktop-win10-win11-64bit-international-dch-whql.exe",
    ]
```
此处调整线程数

```python
    max_threads = 32
```

