#!/usr/bin/python
# -*- coding: utf-8 -*-
#import json
import simplejson as json
import logging
import os
import re
import sys
import time
#from collections import OrderedDict
from simplejson import OrderedDict
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from DaumScraper import DaumScraper
from DummyScraper import DummyScraper
from MockScraper import MockScraper
from TMDBScraper import TMDBScraper
try:
    import xbmc
    __addonname__ = 'SCRPROXY_ADDON'
except:
    print "standalone-mode"
'''
Created on 2016. 3. 29.

@author: mashedon@gmail.com
'''


def log_dbg(txt):
    if ('__addonname__' in globals()):
        message = ('{0}: {1}'.format(__addonname__, txt)).encode('utf-8','ignore')
        xbmc.log(msg=message, level=xbmc.LOGDEBUG)
    else:
        __logger__.debug(txt)        


def log_inf(txt):
    if ('__addonname__' in globals()):
        message = ('{0}: {1}'.format(__addonname__, txt)).encode('utf-8','ignore')
        xbmc.log(msg=message, level=xbmc.LOGINFO)
    else:
        __logger__.info(txt)        


def log_err(txt):
    if ('__addonname__' in globals()):
        message = ('{0}: {1}'.format(__addonname__, txt)).encode('utf-8','ignore')
        xbmc.log(msg=message, level=xbmc.LOGERROR)
    else:
        __logger__.error(txt)        


#This class will handles any incoming request from
#the browser 
class ScraperProxyHandler(BaseHTTPRequestHandler):
    
    def refineQuery(self, query):
        try:
            query = re.sub('[`~!@#$%^\&\(\)\-_=+\[\{\]\}\;\'\,\.]', ' ', query)  # 특수문자 제거
            query = re.sub('\s\s*', ' ', query)                                  # 연속된 공백 하나로
            query = query.strip().rstrip()                                       # 앞,뒤 공백 trim
            return query
            
        except Exception as e:
            return ''
        
        
    def mergeList(self, listJson1, listJson2):
        try:
            # 두 개의 검색 결과를 merge
            listDict1= json.loads(listJson1, object_pairs_hook=OrderedDict)
            listDict2 =  json.loads(listJson2, object_pairs_hook=OrderedDict)
            for resultDict in listDict2['results']:
                listDict1['results'].append(resultDict)
            listJson = json.dumps(listDict1, ensure_ascii=False, separators=(',', ':'))
            return listJson
        except Exception as e:
            log_err(str(e))
        
        
    # 영화 검색
    def findMovies(self, query, year, lang, metaSrc):
        try:
            query = self.refineQuery(query)
            
            if (metaSrc == 'tmdb'):
                # TMDB에서 검색
                return TMDBScraper(SVC_NAME).findMovies4Kodi(query, year, lang) 
            elif (metaSrc == 'daum'):
                # Daum에서 검색
                return DaumScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
            elif (metaSrc == 'dummy'):
                # Dummy 검색결과 생성
                return DummyScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
            elif (metaSrc == 'mock'):
                # 테스트용
                return MockScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
            else:
                # TMDB에서 검색
                tmdbListJson = TMDBScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
                # Daum에서 검색
                daumListJson = DaumScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
            
                if (tmdbListJson is not None) and (daumListJson is not None):
                    # 두 개의 검색 결과를 merge
                    return self.mergeList(tmdbListJson, daumListJson)
                elif (tmdbListJson is not None):
                    return tmdbListJson
                elif (daumListJson is not None):
                    return daumListJson
                else:
                    # Dummy 리턴
                    return DummyScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
                    #return '{"error":"Nothing Found","query":"{0}"}'.format(query)
             
        except Exception as e:
            log_err(str(e))
    
    
    # 영화 상세정보 조회
    def getMovieDetail(self, movieId, lang, imageSrc):
        try:
            if movieId.startswith(TMDBScraper.movieIdPrefix) or movieId.startswith('tt') :
                # TMDB 영화정보 조회
                return TMDBScraper(SVC_NAME).getMovieDetail4Kodi(movieId, lang, imageSrc)
            elif movieId.startswith(DaumScraper.movieIdPrefix):
                # Daum 영화정보 조회
                return DaumScraper(SVC_NAME).getMovieDetail4Kodi(movieId, lang, imageSrc)
            elif movieId.startswith(DummyScraper.movieIdPrefix):
                # Dummy 영화정보 생성
                return DummyScraper(SVC_NAME).getMovieDetail4Kodi(movieId, lang, imageSrc)
            elif movieId.startswith(MockScraper.movieIdPrefix):
                # 테스트용
                return MockScraper(SVC_NAME).getMovieDetail4Kodi(movieId, lang, imageSrc)
            else:
                return '{"error":"Invalid Id","id":"{0}"}'.format(movieId)
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 검색
    def findTvShows(self, query, year, lang, metaSrc):
        try:
            query = re.sub('[\.\[\]\-=:]', ' ', query)  # 특수문자 제거
            query = re.sub(' [ ]+', ' ', query)         # 연속된 공백은 공백 하나로 변경 
            query = query.strip().rstrip()              # 앞,뒤 공백 trim
            
            if (metaSrc == 'tmdb'):
                # TMDB에서 검색
                return TMDBScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
            elif (metaSrc == 'daum'):
                # Daum에서 검색
                return DaumScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
            elif (metaSrc == 'dummy'):
                # Dummy 검색결과 생성
                return DummyScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
            elif (metaSrc == 'mock'):
                # 테스트용
                return MockScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
            else:
                # TMDB에서 검색
                tmdbListJson = TMDBScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
                # Daum에서 검색
                daumListJson = DaumScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
                
                if (tmdbListJson is not None) and (daumListJson is not None):
                    # 두 개의 검색 결과를 merge
                    return self.mergeList(tmdbListJson, daumListJson)
                elif (tmdbListJson is not None):
                    return tmdbListJson
                elif (daumListJson is not None):
                    return daumListJson
                else:
                    # Dummy 리턴
                    #return DummyScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
                    return '{"error":"Nothing Found","query":"{0}"}'.format(query)
            
        except Exception as e:
            log_err(str(e))
    
    
    # TV쇼 상세정보 조회
    def getTvShowDetail(self, showId, lang):
        try:
            if showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV정보 조회
                return DaumScraper(SVC_NAME).getTvShowDetail4Kodi(showId, lang)
            elif showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV정보 조회
                return TMDBScraper(SVC_NAME).getTvShowDetail4Kodi(showId, lang)
            elif showId.startswith(MockScraper.showIdPrefix):
                # 테스트용
                return MockScraper(SVC_NAME).getTvShowDetail4Kodi(showId, lang)
            else:
                return '{"error":"Invalid Id","id":"{0}"}'.format(showId)
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 에피소드목록 조회
    def getTvShowEpList(self, showId, lang):
        try:
            if showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV 에피소드 목록 조회
                return TMDBScraper(SVC_NAME).getTvShowEpList4Kodi(showId, lang)
            elif showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV 에피소드 목록 조회
                return DaumScraper(SVC_NAME).getTvShowEpList4Kodi(showId, lang)
            elif showId.startswith(MockScraper.showIdPrefix):
                # 테스트용
                return MockScraper(SVC_NAME).getTvShowEpList4Kodi(showId, lang)
            else:
                return '{"error":"Invalid Id","id":"{0}"}'.format(showId)
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 에피소드 목록 조회
    def getTvShowEpisode(self, showId, sno, eno, lang):
        try:
            if showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV 에피소드 조회
                return TMDBScraper(SVC_NAME).getTvShowEpisode4Kodi(showId, sno, eno, lang)
            elif showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV 에피소드 조회
                return DaumScraper(SVC_NAME).getTvShowEpisode4Kodi(showId, sno, eno, lang)
            elif showId.startswith(MockScraper.showIdPrefix):
                # 테스트용
                return MockScraper(SVC_NAME).getTvShowEpisode4Kodi(showId, sno, eno, lang)
            else:
                return '{"error":"Invalid Id","id":"{0}"}'.format(showId)
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 이미지 목록 조회
    def getTvShowImages(self, showId, lang):
        try:
            if showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV 에피소드 목록 조회
                return TMDBScraper(SVC_NAME).getTvShowImages4Kodi(showId, lang)
            elif showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV 에피소드 목록 조회
                return DaumScraper(SVC_NAME).getTvShowImages4Kodi(showId, lang)
            elif showId.startswith(MockScraper.showIdPrefix):
                # 테스트용
                return MockScraper(SVC_NAME).getTvShowImages4Kodi(showId, lang)
            else:
                return '{"error":"Invalid Id","id":"{0}"}'.format(showId)
    
        except Exception as e:
            log_err(str(e))

    
    def sendErrMsg(self, errno):
        try:
            log_inf('Send response(code:404)')
            self.send_error(errno)
            
        except Exception as e:
            log_err(str(e))


    def sendRespMsg(self, resp):
        try:
            if (resp is None) or (resp == ''):
                resp = '{}'
            log_inf('Send response(code:200)')
            log_inf(resp)
            self.send_response(200)
            self.send_header('content-type', 'application/json;charset=UTF-8')
            self.end_headers()
            self.wfile.write(resp.encode('utf-8'))
            
        except Exception as e:
            log_err(str(e))


    def sendRespImage(self, fileName):
        try:
            log_inf('fileName={0}'.format(fileName))
            fileSize = os.path.getsize(fileName)
            log_inf('fileSize={0}'.format(fileSize))
            if (fileSize > 0):
                f = open(fileName, 'rb')
                resp = f.read()
                f.close()
                
                log_inf('Send response(code:200)')
                self.send_response(200)
                self.send_header('content-type', 'image/jpeg')
                self.send_header('content-length', fileSize)
                self.wfile.write(resp)
                self.end_headers()
            else:
                self.sendErrMsg(404)
                    
        except Exception as e:
            log_err(str(e))


    #Handler for the GET requests
    def do_GET(self):
        try:
            log_inf("Recv request (self.path={0})".format(self.path))
            o = urlparse(self.path)
            
            # URL 파라메터 추출
            url_params = parse_qs(o.query)
            query = ''
            year = ''
            entityId = ''
            sno = ''
            eno = ''
            lang = 'ko'
            metaSrc = 'all'
            imageSrc  = ''
            if ('query' in url_params):
                query = url_params['query'][0]
                log_dbg('query={0}'.format(query))
            if ('year' in url_params):
                year = url_params['year'][0]
                log_dbg('year={0}'.format(year))
            if ('id' in url_params):
                entityId = url_params['id'][0]
                log_dbg('id={0}'.format(entityId))
            if ('sno' in url_params):
                sno = url_params['sno'][0]
                log_dbg('sno={0}'.format(sno))
            if ('eno' in url_params):
                eno = url_params['eno'][0]
                log_dbg('eno={0}'.format(eno))
            if ('language' in url_params):
                lang = url_params['language'][0]
                log_dbg('language={0}'.format(lang))
            if ('metasrc' in url_params):
                metaSrc = url_params['metasrc'][0]
                log_dbg('metasrc={0}'.format(metaSrc))
            if ('tmdbimg' in url_params):
                tmdbimg = url_params['tmdbimg'][0]
                log_dbg('tmdbimg={0}'.format(tmdbimg))
                if (tmdbimg == 'true'):
                    imageSrc = 'tmdb'
            
            # 파라메터 값 검사
            yearRegex = re.compile('[0-9]*')
            if (year != '') and (not yearRegex.match(year)):
                self.sendRespMsg('{"path":"%s"}' % format(self.path))
                return
            if (lang != 'ko') and (lang != 'en'):
                self.sendRespMsg('{"path":"%s"}' % format(self.path))
                return
            
            if (o.path == '/search/movie'):
                # 영화 검색
                if len(query) > 0:
                    resp = self.findMovies(query, year, lang, metaSrc)
                    self.sendRespMsg(resp)
                    return
                
            elif (o.path == '/movie'):
                # 영화 상세정보 조회
                if len(entityId) > 0:
                    resp = self.getMovieDetail(entityId, lang, imageSrc)
                    self.sendRespMsg(resp)
                    return
            
            elif (o.path == '/search/tv'):
                # TV쇼 검색
                if len(query) > 0:
                    resp = self.findTvShows(query, year, lang, metaSrc)
                    self.sendRespMsg(resp)
                    return
            
            elif (o.path == '/tv'):
                # TV시리즈 상세정보 조회
                if len(entityId) > 0:
                    resp = self.getTvShowDetail(entityId, lang)
                    self.sendRespMsg(resp)
                    return
            
            elif (o.path == '/tv/episode/all'):
                # 에피소드 목록+상세 조회
                if len(entityId) > 0:
                    resp = self.getTvShowEpList(entityId, lang)
                    self.sendRespMsg(resp)
                    return
            
#             elif (o.path == '/tv/episode'):
#                 # 에피소드 상세정보 조회
#                 if len(entityId) > 0:
#                     resp = self.getTvShowEpisode(entityId, sno, eno, lang)
#                     self.sendRespMsg(resp)
#                     return
            
            elif (o.path == '/tv/images'):
                # TV시리즈 이미지 조회
                if len(entityId) > 0:
                    resp = self.getTvShowImages(entityId, lang)
                    self.sendRespMsg(resp)
                    return
            
            elif o.path.startswith('/image/'):
                # 이미지 파일 전송
                fileName = self.path[len('/image/'):]
                log_dbg('fileName={0}'.format(fileName))
                if len(fileName) > 0:
                    self.sendRespImage(fileName)
                    return
            
            self.sendRespMsg('{"path":"%s"}' % format(self.path))
            return
        
        except Exception as e:
            log_err(str(e))


if __name__ == '__main__':
    try:
        SVC_NAME = 'SCRPROXY'
        PORT_NUMBER = 9990
        if ('__addonname__' in globals()):
            SVC_NAME = __addonname__
            PORT_NUMBER = 8880
        
        # 기본 인코딩을 UTF-8로 변경
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        #LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #logging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        __logger__ = logging.getLogger(SVC_NAME)
        
        log_inf('==[STARTED]======================================')
        
        # 오래된 캐시 파일 삭제
        MockScraper(SVC_NAME).cache_clear()
        
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), ScraperProxyHandler)
        log_inf("Started httpserver on port {0}".format(PORT_NUMBER))
        
        #Wait forever for incoming htto requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        log_inf("^C received, shutting down the web server")
        server.socket.close()
