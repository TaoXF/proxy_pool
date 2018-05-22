# proxy_pool

### 使用依赖
版本: python3\
包: aiohttp  requests redis

### 使用之前配置
需要配置settings 里的redis配置项\
scheduler.py 里102行的本机ip地址\
getter.py 的请求url\
url 需要购买 价钱很便宜, 数量无限制, 高匿名\
http://www.66ip.cn/zz.html

也有免费的但是不怎么好用

其他就改改自己的user-agent之类的就行了
可以根据自己的需求修改\
scheduler.py 里的 Scheduler类的 check_pool 方法 的测试值改变代理池的容量\
建议不要太大, 代理的存活时间并不长久, 需求量大的话1000也就足够了
