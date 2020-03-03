import requests, re, hashlib, json

class KG(object):
    def __init__(self):
        self.url = 'https://www.kugou.com/share/zlist.html?listid=2&type=0&uid=1012067831&share_type=collect&from=pcCode&_t=636584374&sign=03102c5ccc9ffdf8bb5645af257bb91b#hash=287AB65E26E0948BD0DF8181980D5BAC&album_id=27984599'

    def rjson(self):
        req = requests.get(self.url).text
        js = re.findall('    var dataFromSmarty = (.*?),//当前页面歌曲信息',req,re.S)[0]
        self.js = json.loads(js)
        
    def mp3_url(self,x):
        #hash+kgcloudv2的加盐值就是key  得出mp3url
        hash = self.js[x]['hash']
        key = hashlib.md5((hash+'kgcloudv2').encode('utf-8')).hexdigest()
        self.mp3url = f'http://trackercdn.kugou.com/i/v2/?appid=1005&pid=2&cmd=25&behavior=play&hash={hash}&key={key}'
        #得出name
        self.name = self.js[x]['audio_name']
        






kg = KG()
kg.rjson()
kg.mp3_url(0)

