#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import math
import re
import time
from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse

class QingTingDownloader:

    def __init__(self, url, outputPath):
        self.apidata = {
            "url" : 'https://i.qingting.fm/wapi',
            'programs' : 'programs/',
            'page' : 'page/',
            'defaultPage': str(1),
            'pagesize' : '/pagesize/',
            'defaultPageSize': str(200),
            'dataUrl' : 'http://od.qingting.fm/'
        }
        self.data = []
        self.url = url
        self.outputPath = outputPath
        self.apiUrlDetector()
        self.apiGenerator()
        self.download()
    

    def creatDict(self):

        return

    def apiUrl (self, index = None):
        # https://i.qingting.fm/wapi/channels/62962/programs/page/1/pagesize/10
        # https://i.qingting.fm/wapi/channels/271526/programs/page/1/pagesize/10
        parseResult = urlparse(self.url)
        if index :
            return self.apidata['url'] + parseResult.path + \
                self.apidata['programs'] + \
                self.apidata['page'] + str(index) + \
                self.apidata['pagesize'] + self.apidata['defaultPageSize']
        else:
            return self.apidata['url'] + parseResult.path + \
                self.apidata['programs'] + \
                self.apidata['page'] + self.apidata['defaultPage'] + \
                self.apidata['pagesize'] + self.apidata['defaultPageSize']

    def apiUrlDetector(self):
        apiurl = self.apiUrl()
        req = Request(apiurl)        
        try:
            response = urlopen(req)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            self.total = 0
            self.pages = 0
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            self.total = 0
            self.pages = 0
        else:
            content = json.loads(response.read().decode('utf8'))
            self.total = int(content['total'])
            self.pages = math.ceil(self.total / int(self.apidata['defaultPageSize']))
        return 

    def apiGenerator(self):
        for pageIndex in range(self.pages):
            apiurl = self.apiUrl(pageIndex + 1)
            req = Request(apiurl) 
            try:
                response = urlopen(req)
            except HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            else:
                content = json.loads(response.read().decode('utf8'))
                datas = content['data']
                datadict = {}
                for value in datas:
                    r = u'[’!"#$%&\'*+,./:;<=>?@，。?★、…？“”•‘’！^`|【】《》『』（）()[\\]`{|}~；]+'
                    # r1 = u'[’!"#$%&\'*+,./:;<=>?@，。?★、…？“”•‘’！^`|~；]+'
                    # r2 = u'[’【】《》『』（）()[\\]`{|}~；]+'
                    extension = os.path.splitext(value['file_path'])[1]
                    filename = re.sub(r,'_',value['name'].replace(' ','_'))
                    filename = filename.replace('___','_').replace('__','_')
                    datadict[value['file_path']] = filename + extension
                self.data.append(datadict)
        return

    def download(self):
        for tempdata in self.data:
            for media in tempdata:
                tempUrl = self.apidata['dataUrl'] + media
                tempFile = self.outputPath + tempdata[media]

                result = None
                while result is None:
                    try:
                        urlretrieve(tempUrl, "{0}".format(tempFile))
                        print("{0} has been downloaded".format(tempdata[media]))
                        result = True
                    except:
                        time.sleep(5)
                        pass
        return 


if __name__ == "__main__":

    QingTingDownloader("https://www.qingting.fm/channels/154332/", "/Users/xnzhang/Downloads/test/")