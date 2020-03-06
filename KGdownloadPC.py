import requests, re, hashlib, json, os

#https://www.kugou.com/share/zlist.html?listid=2&type=0&uid=1012067831&share_type=collect&from=pcCode&_t=636584374&sign=03102c5ccc9ffdf8bb5645af257bb91b#hash=287AB65E26E0948BD0DF8181980D5BAC&album_id=27984599

class KG(object):
    def __init__(self):
        try:
            os.mkdir('download')
        except FileExistsError:
            pass
        self.url = input('输入歌单链接>')
         
    #只执行一次
    def rjson(self):
        req = requests.get(self.url).text
        js = re.findall('    var dataFromSmarty = (.*?),//当前页面歌曲信息',req,re.S)[0]
        self.js = json.loads(js)
    
    #循环len(kg.js) x为歌曲
    def mp3_url(self,x):
        #hash+kgcloudv2的加盐值就是key  得出mp3url
        hash = self.js[x]['hash']
        key = hashlib.md5((hash+'kgcloudv2').encode('utf-8')).hexdigest()
        self.mp3url = f'http://trackercdn.kugou.com/i/v2/?appid=1005&pid=2&cmd=25&behavior=play&hash={hash}&key={key}'
        #得出name
        self.name = self.js[x]['audio_name']
    
    #与mp3_url并行
    def download(self):
        js = json.loads(requests.get(self.mp3url).text)
        try:
            url = js['url'][0].replace('\\','')
            mp3 = requests.get(url)
            with open(f'download/{self.name}.mp3','wb') as f:
                f.write(mp3.content)
        except KeyError:
            print('VIP 歌曲无法下载')
            pass

def run():
    print('init...')
    kg = KG()
    print('done\nrequest song list...')
    kg.rjson()
    print('done\nstart download...')
    for i in range(len(kg.js)):
        kg.mp3_url(i)
        print(f'downloading{kg.name}')
        kg.download()
    print('Download Done \nThank you for useing...')
    input('Enter to exit')

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Download stop...')
        input('Enter to exit')
