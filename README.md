# Bt_Spider
补天漏洞平台公益厂商域名爬虫

环境要求：
      python3及其需要的库,库名我会在requirements.txt给出.

使用说明：
    python3 --help
    python3 -c "你的cookie" -t 线程数量  -s 从第几页开始(默认从第一页开始) -e 到第几页结束(默认爬到第10页)

例子：
    python3 Bt_Spider -c "cookie" -t 8 -s 10 -e 20
    设置8个线程,从第10页爬取到第20页.

    
