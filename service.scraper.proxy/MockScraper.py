# -*- coding: utf-8 -*-
import copy
#import json
import simplejson as json
import logging
import os
import re
import sys
import time
import urllib2
#from collections import OrderedDict
from simplejson import OrderedDict
from datetime import datetime, timedelta
try:
    import xbmc
except:
    print "standalone-mode"
'''
Created on 2016. 3. 29.

@author: mashedon@gmail.com
'''


class MockScraper(object):
    '''
    classdocs
    '''
    logger = None
    cacheDir = './cache'
    kodiListJson = '{"results":[]}'
    kodiEntityJson = '{"entity":{"title":"","year":"","language":"","id":""}}'
    kodiDetailJson = '{"details":{"id":"","title":"","originaltitle":"","set":"","year":"","premiered":"","runtime":"","rating":"","votes":"","mpaa":"","tagline":"","outline":"","plot":"","thumb":[],"fanart":[],"genre":[],"country":[],"studio":[],"director":[],"credits":[],"actor":[]}}'
    kodiFanartJson = '{"thumb":""}'
    kodiActorJson = '{"name":"","role":"","thumb":""}'
    kodiEpListJson = '{"episodeguide":[]}'
    kodiEpJson = '{"episode":{"id":"","season":"","epnum":"","title":"","aired":"","url":"","thumb":[]}}'
    kodiEpDetailJson = '{"details":{"id":"","season":"","episode":"","title":"","aired":"","uniqueid":"","displayseason":"","displayepisode":"","displayafterseason":"","runtime":"","rating":"","votes":"","plot":"","thumb":[],"director":[],"credits":[],"actor":[]}}'
    
    
    def __init__(self, loggerName):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(loggerName)


    def __log_dbg__(self, txt):
        if ('__addonname__' in globals()):
            message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
            xbmc.log(msg=message, level=xbmc.LOGDEBUG)
        else:
            self.logger.debug(txt)
        

    def __log_inf__(self, txt):
        if ('__addonname__' in globals()):
            message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
            xbmc.log(msg=message, level=xbmc.LOGINFO)
        else:
            self.logger.info(txt)
        

    def __log_err__(self, txt):
        if ('__addonname__' in globals()):
            message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
            xbmc.log(msg=message, level=xbmc.LOGERROR)
        else:
            self.logger.error(txt)

        
    def __dict2json__(self, objDict):
        try:
            return json.dumps(objDict, ensure_ascii=False, separators=(',', ':'))
        except Exception as e: 
            self.__log_err__(str(e))
            return ''
    
    
    def __json2dict__(self, strJson):
        try:
            return json.loads(strJson, object_pairs_hook=OrderedDict) 
        except Exception as e: 
            self.__log_err__(str(e))
            return None
    
    
    def __html_escape__(self, text):
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }
        
        # Produce entities within text.
        return "".join(html_escape_table.get(c,c) for c in text)
    

    def __tag_strip__(self, html):
        TAG_RE = re.compile(r'<[^>]+>')
        text = TAG_RE.sub('', html)
        return text


    def __plot_escape__(self, plot):
        plot = re.sub('\\\"', '&quot;', plot)
        plot = re.sub('[\r\n]+', ' ', plot)
        plot = re.sub('<br>', ' ', plot)
        plot = re.sub('<[^<]+?>', '', plot)  # strip html tags
        plot = re.sub('  +', ' ', plot)
        return plot
        
        
    def __regex_find__(self, regexStr, text, option = None):
        try:
            if option:
                return re.search(regexStr, text, option).group(1)
            else:
                return re.search(regexStr, text).group(1)
        except Exception as e: 
            return ''
    
    
    def __regex_findall__(self, regexStr, text, option = None):
        try:
            if option:
                return re.findall(regexStr, text, option)
            else:
                return re.findall(regexStr, text)
        except Exception as e: 
            return []


    def __cache_write__(self, cache, msg):
        try:
            if (cache is None):
                return
            
            filename = '{0}/{1}'.format(self.cacheDir, cache)
            self.__log_dbg__(filename)
            f = open(filename,'wb')
            f.write(msg)
            f.close()
        except Exception as e: 
            self.__log_err__(str(e))

    
    def __cache_read__(self, cache):
        try:
            if (cache is None):
                return ''
            
            filename = '{0}/{1}'.format(self.cacheDir, cache)
            self.__log_dbg__(filename)
            
            # 캐시 파일이 15분 안에 생성되었다면 재사용
            if os.path.isfile(filename):
                modDate = datetime.fromtimestamp(os.path.getmtime(filename))
                limDate = datetime.now() - timedelta(minutes=15)
                if (modDate >= limDate):
                    with open(filename,'rb') as f:
                        return f.read()
                else:
                    # 오래된 캐시 파일 삭제
                    os.remove(filename)
            
            return ''
        except Exception as e: 
            self.__log_err__(str(e))
            return ''

    
    def __wget__(self, url, cache=None):
        try:
            self.__log_inf__('Open : {0}'.format(url))
            
            body = self.__cache_read__(cache)
            if (body is not None) and (len(body) > 0):
                self.__log_inf__('Cache hit! : {0}'.format(cache))
                return body
            
            resp = urllib2.urlopen(url)
            body = resp.read()
            self.__cache_write__(cache, body)
            return body
        
        except urllib2.HTTPError as e:
            # HTTP-specific error (e.g. 404:FileNotFound)
            self.__log_err__(str(e))
            
        except urllib2.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            self.__log_err__(str(e))
            
        except Exception as e: 
            self.self.__log_err__(str(e))
            

    # 영화 검색
    def findMovies4Kodi(self, query, year, lang):
        try:
            kodiListDict = json.loads(self.kodiListJson, object_pairs_hook=OrderedDict)
            entityDictTemplate = json.loads(self.kodiEntityJson, object_pairs_hook=OrderedDict)
            self.__log_dbg__(kodiListDict)
            
            entityDict = copy.deepcopy(entityDictTemplate)
            entityDict['entity']['title'] = '매트릭스'
            entityDict['entity']['year'] = '1999'
            entityDict['entity']['language'] = 'ko'
            entityDict['entity']['id'] = '603'
            kodiListDict['results'].append(entityDict)
            
            kodiListJson = json.dumps(kodiListDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 상세정보 조회
    def getMovieDetail4Kodi(self, movieId, lang):
        try:
            kodiDetailDict = json.loads(self.kodiDetailJson, object_pairs_hook=OrderedDict)
            fanartDictTemplate = json.loads(self.kodiFanartJson, object_pairs_hook=OrderedDict)
            actorDictTemplate = json.loads(self.kodiActorJson, object_pairs_hook=OrderedDict)
            self.__log_dbg__(kodiDetailDict)
            
            detailsDict = kodiDetailDict['details'] 
            detailsDict['id'] = '603'
            detailsDict['title'] = '매트릭스'
            detailsDict['originaltitle'] = 'The Matrix'
            detailsDict['set'] = 'The Matrix Collection'
            detailsDict['year'] = '1999'
            detailsDict['premiered'] = '1999-03-30'
            detailsDict['runtime'] = '136'
            detailsDict['rating'] = '7.7'
            detailsDict['votes'] = '5328'
            detailsDict['mpaa'] = 'RATED R'
            detailsDict['tagline'] = 'Welcome to the Real World.(tagline)'
            detailsDict['outline'] = 'Welcome to the Real World.(outline)'
            detailsDict['plot'] = 'Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a malevolent hacker known as Neo, who finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker, who reveals the shocking truth about our reality.'
            
            detailsDict['thumb'].append('http://image.tmdb.org/t/p/w396/lZpWprJqbIFpEV5uoHfoK0KCnTW.jpg')
            detailsDict['thumb'].append('http://image.tmdb.org/t/p/w396/gynBNzwyaHKtXqlEKKLioNkjKgN.jpg')
            
            fanartDict = copy.deepcopy(fanartDictTemplate)
            fanartDict['thumb'] = 'http://image.tmdb.org/t/p/w396/7u3pxc0K1wx32IleAkLv78MKgrw.jpg'
            detailsDict['fanart'].append(fanartDict)
            fanartDict = copy.deepcopy(fanartDictTemplate)
            fanartDict['thumb'] = 'http://image.tmdb.org/t/p/w396/xbm8IlWguCctQL7nqKpjpryFh5e.jpg'
            detailsDict['fanart'].append(fanartDict)
            
            detailsDict['genre'].append('Adventure')
            detailsDict['genre'].append('Action')
            detailsDict['genre'].append('Thriller')
            detailsDict['genre'].append('Science Fiction')
            
            detailsDict['country'].append('Australia')
            detailsDict['country'].append('United States of America')
            
            detailsDict['studio'].append('Village Roadshow Pictures')
            detailsDict['studio'].append('Groucho II Film Partnership')
            detailsDict['studio'].append('Silver Pictures')
            detailsDict['studio'].append('Warner Bros.')

            detailsDict['director'].append('Lilly Wachowski')
            detailsDict['director'].append('Lana Wachowski')
            
            detailsDict['credits'].append('Lilly Wachowski')
            detailsDict['credits'].append('Lana Wachowski')
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Keanu Reeves'
            actorDict['role'] = 'Neo'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/glCFGnKkX3QWxeLRYUMU1XTESHf.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Laurence Fishburne'
            actorDict['role'] = 'Morpheus'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/mh0lZ1XsT84FayMNiT6Erh91mVu.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Carrie-Anne Moss'
            actorDict['role'] = 'Trinity'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/6gk8GmlfjW8ONS19KMeISp8Cqxf.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Hugo Weaving'
            actorDict['role'] = 'Agent Smith'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/ysED1kp94bpnweNVaDoVQQ6iy8X.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Gloria Foster'
            actorDict['role'] = 'Oracle'
            actorDict['thumb'] = ''
            detailsDict['actor'].append(actorDict)
            
            kodiMovieDetailJson = json.dumps(kodiDetailDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiMovieDetailJson)
            return kodiMovieDetailJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 검색
    def findTvShows4Kodi(self, query, year, lang):
        try:
            kodiListDict = json.loads(self.kodiListJson, object_pairs_hook=OrderedDict)
            entityDictTemplate = json.loads(self.kodiEntityJson, object_pairs_hook=OrderedDict)
            self.__log_dbg__(kodiListDict)
            
            entityDict = copy.deepcopy(entityDictTemplate)
            entityDict['entity']['title'] = '왕좌의 게임'
            entityDict['entity']['year'] = ''
            entityDict['entity']['language'] = 'ko'
            entityDict['entity']['id'] = '58449'
            kodiListDict['results'].append(entityDict)
            
            kodiListJson = json.dumps(kodiListDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 상세정보 조회
    def getTvShowDetail4Kodi(self, showId, lang):
        try:
            kodiDetailDict = json.loads(self.kodiDetailJson, object_pairs_hook=OrderedDict)
            fanartDictTemplate = json.loads(self.kodiFanartJson, object_pairs_hook=OrderedDict)
            actorDictTemplate = json.loads(self.kodiActorJson, object_pairs_hook=OrderedDict)
            self.__log_dbg__(kodiDetailDict)
            
            detailsDict = kodiDetailDict['details'] 
            detailsDict['id'] = '58449'
            detailsDict['title'] = '왕좌의 게임'
            detailsDict['originaltitle'] = 'Game of Thrones'
            detailsDict['set'] = ''
            detailsDict['year'] = '2011'
            detailsDict['premiered'] = '2011-04-17'
            detailsDict['runtime'] = '60'
            detailsDict['rating'] = '8.37'
            detailsDict['votes'] = '551'
            detailsDict['mpaa'] = ''
            detailsDict['tagline'] = ''
            detailsDict['outline'] = ''
            detailsDict['plot'] = 'Seven noble families fight for control of the mythical land of Westeros. Friction between the houses leads to full-scale war. All while a very ancient evil awakens in the farthest north. Amidst the war, a neglected military order of misfits, the Night\'s Watch, is all that stands between the realms of men and icy horrors beyond.'
            
            detailsDict['thumb'].append('http://image.tmdb.org/t/p/w396/jIhL6mlT7AblhbHJgEoiBIOUVl1.jpg')
            #detailsDict['thumb'].append('http://image.tmdb.org/t/p/w396/gynBNzwyaHKtXqlEKKLioNkjKgN.jpg')
            
            fanartDict = copy.deepcopy(fanartDictTemplate)
            fanartDict['thumb'] = 'http://image.tmdb.org/t/p/w396/mUkuc2wyV9dHLG0D0Loaw5pO2s8.jpg'
            detailsDict['fanart'].append(fanartDict)
            #fanartDict = copy.deepcopy(fanartDictTemplate)
            #fanartDict['thumb'] = 'http://image.tmdb.org/t/p/w396/xbm8IlWguCctQL7nqKpjpryFh5e.jpg'
            #detailsDict['fanart'].append(fanartDict)
            
            detailsDict['genre'].append('Action & Adventur')
            detailsDict['genre'].append('Drama')
            detailsDict['genre'].append('Sci-Fi & Fantasy')
            
            detailsDict['country'].append('US')
            
            detailsDict['studio'].append('HBO')

            detailsDict['director'].append('Who')
            
            detailsDict['credits'].append('Who')
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Peter Dinklage'
            actorDict['role'] = 'Tyrion Lannister'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/xuB7b4GbARu4HN6gq5zMqjGbkwF.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Nikolaj Coster-Waldau'
            actorDict['role'] = 'Jaime Lannister'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/7FGmv5Hrknmsnpxbox2V4GG2xdx.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Lena Headey'
            actorDict['role'] = 'Cersei Baratheon'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/wcpy6J7KLzmVt0METboX3CZ0Jp.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Emilia Clarke'
            actorDict['role'] = 'Daenerys Targaryen'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/tB1nE2LJH81f5UMiGhKCSlaqsF1.jpg'
            detailsDict['actor'].append(actorDict)
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Kit Harington'
            actorDict['role'] = 'Jon Snow'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/dwRmvQUkddCx6Xi7vDrdnQL4SJ0.jpg'
            detailsDict['actor'].append(actorDict)
            
            kodiDetailJson = json.dumps(kodiDetailDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiDetailJson)
            return kodiDetailJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 에피소드 목록 조회
    def getTvShowEpList4Kodi(self, showId, lang):
        try:
            kodiEpListDict = json.loads(self.kodiEpListJson, object_pairs_hook=OrderedDict)
            epDictTemplate = json.loads(self.kodiEpJson, object_pairs_hook=OrderedDict)
            self.__log_dbg__(kodiEpListDict)
                        
            epDict = copy.deepcopy(epDictTemplate)
            epDict['episode']['id'] = str(showId)
            epDict['episode']['season'] = '1'
            epDict['episode']['epnum'] = '1'
            epDict['episode']['title'] = 'Winter Is Coming'
            epDict['episode']['aired'] = '2011-04-17'
            epDict['episode']['url'] = ''   # addon에서 생성
            kodiEpListDict['episodeguide'].append(epDict)
            
            epDict = copy.deepcopy(epDictTemplate)
            epDict['episode']['id'] = str(showId)
            epDict['episode']['season'] = '1'
            epDict['episode']['epnum'] = '2'
            epDict['episode']['title'] = 'The Kingsroad'
            epDict['episode']['aired'] = '2011-04-24'
            epDict['episode']['url'] = ''  # addon에서 생성
            kodiEpListDict['episodeguide'].append(epDict)
            
            epDict = copy.deepcopy(epDictTemplate)
            epDict['episode']['id'] = str(showId)
            epDict['episode']['season'] = '1'
            epDict['episode']['epnum'] = '3'
            epDict['episode']['title'] = 'Lord Snow'
            epDict['episode']['aired'] = '2011-05-01'
            epDict['episode']['url'] = ''  # addon에서 생성
            kodiEpListDict['episodeguide'].append(epDict)
            
            kodiEpListJson = json.dumps(kodiEpListDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiEpListJson)
            return kodiEpListJson
            
        except Exception as e: 
            self.__log_err__(str(e))


    # 에피소드 상세정보 조회
    def getTvShowEpisode4Kodi(self, showId, sno, eno, lang):
        try:
            kodiEpDetailDict = json.loads(self.kodiEpDetailJson, object_pairs_hook=OrderedDict)
            actorDictTemplate = json.loads(self.kodiActorJson, object_pairs_hook=OrderedDict)
            
            detailsDict = kodiEpDetailDict['details']
            detailsDict['id'] = str(showId)
            detailsDict['season'] = str(sno)
            detailsDict['epnum'] = str(eno)
            detailsDict['title'] = 'Lord Snow'
            detailsDict['aired'] = '2011-05-01'
            detailsDict['uniqueid'] = '{0}_{1}_{2}'.format(showId, sno, eno)
            detailsDict['displayseason'] = str(sno)
            detailsDict['displayepisode'] = str(eno)
            detailsDict['displayafterseason'] = ''
            detailsDict['runtime'] = '61'
            detailsDict['rating'] = '9.1'
            detailsDict['votes'] = '521'
            detailsDict['plot'] = 'We don\'t currently have an overview translated to 한국어/조선말 (Korean). Help expand our database by adding one!'
            detailsDict['thumb'].append('https://image.tmdb.org/t/p/w300/wrGWeW4WKxnaeA8sxJb2T9O6ryo.jpg')
            detailsDict['director'].append('Tim Van Patten')
            detailsDict['credits'].append('David Benioff')
            detailsDict['credits'].append('D. B. Weiss')
            
            actorDict = copy.deepcopy(actorDictTemplate)
            actorDict['name'] = 'Kit Harington'
            actorDict['role'] = 'Jon Snow'
            actorDict['thumb'] = 'http://image.tmdb.org/t/p/w396/dwRmvQUkddCx6Xi7vDrdnQL4SJ0.jpg'
            detailsDict['actor'].append(actorDict)
            
            kodiEpDetailJson = json.dumps(kodiEpDetailDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiEpDetailJson)
            return kodiEpDetailJson
        
        except Exception as e: 
            self.__log_err__(str(e))


if __name__ == '__main__':
    try:
        # 기본 인코딩을 UTF-8로 설정
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        SVC_NAME = 'MOCK'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #logging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        logger = logging.getLogger(SVC_NAME)
        logger.info('==[STARTED]======================================')
        
    #     # 영화 검색
    #     query = '배트맨 대 슈퍼맨'
    #     year = ''
    #     lang = 'ko'
    #     scraper = MockScraper(SVC_NAME)
    #     listJson = scraper.findMovies4Kodi(query, year, lang)
    #     logger.debug('')
    #      
    #     listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
    #     logger.debug(listDict)
    #     for resultDict in listDict['results']:
    #         # 검색결과에서 영화ID 추출
    #         movieId = resultDict['entity']['id']
    #         logger.debug('movieId={0}'.format(movieId))
    #         title = resultDict['entity']['title']
    #         logger.debug('title={0}'.format(title))
    #          
    #         # 상세정보 조회
    #         detailJson = scraper.getMovieDetail4Kodi(movieId, lang)
    #         logger.debug('')
    
        # TV쇼 검색
        query = '왕좌의 게임'
        year = ''
        lang = 'ko'
        scraper = MockScraper(SVC_NAME)
        listJson = scraper.findTvShows4Kodi(query, year, lang)
        logger.debug('')
         
        listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
        logger.debug(listDict)
        for resultDict in listDict['results']:
            # 검색결과에서 TV쇼ID 추출
            showId = resultDict['entity']['id']
            logger.debug('showId={0}'.format(showId))
            title = resultDict['entity']['title']
            logger.debug('title={0}'.format(title))
             
            # 상세정보 조회
            detailJson = scraper.getTvShowDetail4Kodi(showId, lang)
            logger.debug('')
    
            # 에피소드목록 조회
            detailJson = scraper.getTvShowEpList4Kodi(showId, lang)
            logger.debug('')
    
    except Exception as e:
        logger.error(str(e))
