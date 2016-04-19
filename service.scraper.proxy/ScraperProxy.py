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
except:
    print "standalone-mode"
'''
Created on 2016. 3. 29.

@author: mashedon@gmail.com
'''


def log_dbg(txt):
    if ('__addonname__' in globals()):
        message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
        xbmc.log(msg=message, level=xbmc.LOGDEBUG)
    else:
        __logger__.debug(txt)        


def log_inf(txt):
    if ('__addonname__' in globals()):
        message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
        xbmc.log(msg=message, level=xbmc.LOGINFO)
    else:
        __logger__.info(txt)        


def log_err(txt):
    if ('__addonname__' in globals()):
        message = '%s: %s' % (__addonname__, txt.encode('utf-8', 'ignore'))
        xbmc.log(msg=message, level=xbmc.LOGERROR)
    else:
        __logger__.error(txt)        


#This class will handles any incoming request from
#the browser 
class ScraperProxyHandler(BaseHTTPRequestHandler):
    
    def mergeList(self, listJson1, listJson2):
        try:
            # 두 개의 검색 결과를 merge
            listDict1= json.loads(listJson1, object_pairs_hook=OrderedDict)
            listDict2 =  json.loads(listJson2, object_pairs_hook=OrderedDict)
            for resultDict in listDict2['results']:
                listDict1['results'].append(resultDict)
            listJson = json.dumps(listDict1, ensure_ascii=False, separators=(',', ':'))
            log_inf(listJson)
            return listJson
        except Exception as e:
            log_err(str(e))
        
        
    # 영화 검색
    def findMovies(self, query, year, lang):
        try:
            query = re.sub('[\.\[\]\-=:]', ' ', query)  # 특수문자 제거
            query = re.sub(' [ ]+', ' ', query)         # 연속된 공백은 공백 하나로 변경 
            query = query.strip().rstrip()              # 앞,뒤 공백 trim
            
#             # 테스트
#             return MockScraper(SVC_NAME).findMovies4Kodi(query, year, lang)
            
            # TMDB에서 검색
            tmdbScraper = TMDBScraper(SVC_NAME)
            tmdbListJson = tmdbScraper.findMovies4Kodi(query, year, lang)
 
            # Daum에서 검색
            daumScraper = DaumScraper(SVC_NAME)
            daumListJson = daumScraper.findMovies4Kodi(query, year, lang)
             
            if (tmdbListJson is not None) and (daumListJson is not None):
                # 두 개의 검색 결과를 merge
                return self.mergeList(tmdbListJson, daumListJson)
            elif (tmdbListJson is not None):
                return tmdbListJson
            elif (daumListJson is not None):
                return daumListJson
            else:
                # Dummy 리턴
                dummyScraper = DummyScraper(SVC_NAME)
                return dummyScraper.findMovies4Kodi(query, year, lang)
             
        except Exception as e:
            log_err(str(e))
    
    
    # 영화 상세정보 조회
    def getMovieDetail(self, movieId, lang):
        try:
#             # 테스트
#             return MockScraper(SVC_NAME).getMovieDetail4Kodi(movieId, lang)

            if movieId.startswith(DummyScraper.movieIdPrefix):
                # Dummy 영화정보 생성
                dummyScraper = DummyScraper(SVC_NAME)
                movieJson = dummyScraper.getMovieDetail4Kodi(movieId, lang)
                return movieJson
            elif movieId.startswith(DaumScraper.movieIdPrefix):
                # Daum 영화정보 조회
                daumScraper = DaumScraper(SVC_NAME)
                movieJson = daumScraper.getMovieDetail4Kodi(movieId, lang)
                return movieJson
            elif movieId.startswith('tt') or movieId.startswith(TMDBScraper.movieIdPrefix):
                # TMDB 영화정보 조회
                tmdbScraper = TMDBScraper(SVC_NAME)
                movieJson = tmdbScraper.getMovieDetail4Kodi(movieId, lang)
                return movieJson
            else:
                return ''
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 검색
    def findTvShows(self, query, year, lang):
        try:
            query = re.sub('[\.\[\]\-=:]', ' ', query)  # 특수문자 제거
            query = re.sub(' [ ]+', ' ', query)         # 연속된 공백은 공백 하나로 변경 
            query = query.strip().rstrip()              # 앞,뒤 공백 trim
            
#             # 테스트
#             return MockScraper(SVC_NAME).findTvShows4Kodi(query, year, lang)
            
            # TMDB에서 검색
            tmdbScraper = TMDBScraper(SVC_NAME)
            tmdbListJson = tmdbScraper.findTvShows4Kodi(query, year, lang)
            
            # Daum에서 검색
            daumScraper = DaumScraper(SVC_NAME)
            daumListJson = daumScraper.findTvShows4Kodi(query, year, lang)
            
            if (tmdbListJson is not None) and (daumListJson is not None):
                # 두 개의 검색 결과를 merge
                return self.mergeList(tmdbListJson, daumListJson)
            elif (tmdbListJson is not None):
                return tmdbListJson
            elif (daumListJson is not None):
                return daumListJson
            else:
                # Dummy 리턴
                dummyScraper = DummyScraper(SVC_NAME)
                return dummyScraper.findMovies4Kodi(query, year, lang)
            
        except Exception as e:
            log_err(str(e))
    
    
    # TV쇼 상세정보 조회
    def getTvShowDetail(self, showId, lang):
        try:
#             # 테스트
#             return MockScraper(SVC_NAME).getTvShowDetail4Kodi(showId, lang)

            if showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV정보 조회
                daumScraper = DaumScraper(SVC_NAME)
                showJson = daumScraper.getTvShowDetail4Kodi(showId, lang)
                return showJson
            elif showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV정보 조회
                tmdbMovieScraper = TMDBScraper(SVC_NAME)
                showJson = tmdbMovieScraper.getTvShowDetail4Kodi(showId, lang)
                return showJson
            else:
                return ''
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 에피소드목록 조회
    def getTvShowEpList(self, showId, lang):
        try:
#             # 테스트
#             return MockScraper(SVC_NAME).getTvShowEpList4Kodi(showId, lang)

            if showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV 에피소드 목록 조회
                daumScraper = DaumScraper(SVC_NAME)
                showJson = daumScraper.getTvShowEpList4Kodi(showId, lang)
                return showJson
            elif showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV 에피소드 목록 조회
                tmdbScraper = TMDBScraper(SVC_NAME)
                showJson = tmdbScraper.getTvShowEpList4Kodi(showId, lang)
                return showJson
            else:
                return ''
    
        except Exception as e:
            log_err(str(e))

    
    # TV쇼 에피소드목록 조회
    def getTvShowEpisode(self, showId, sno, eno, lang):
        try:
#             # 테스트
#             return MockScraper(SVC_NAME).getTvShowEpisode4Kodi(showId, sno, eno, lang)

            if showId.startswith(DaumScraper.showIdPrefix):
                # Daum TV 에피소드 조회
                daumScraper = DaumScraper(SVC_NAME)
                showJson = daumScraper.getTvShowEpisode4Kodi(showId, sno, eno, lang)
                return showJson
            elif showId.startswith(TMDBScraper.showIdPrefix):
                # TMDB TV 에피소드 조회
                tmdbScraper = TMDBScraper(SVC_NAME)
                showJson = tmdbScraper.getTvShowEpisode4Kodi(showId, sno, eno, lang)
                return showJson
            else:
                return ''
    
        except Exception as e:
            log_err(str(e))

    
    def sendRespMsg(self, resp):
        try:
            if (resp is None) or (resp == ''):
                resp = '{"return":"none1"}'
            log_inf('Send response(code:200)')
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
                log_inf('Send response(code:404)')
                self.send_error(404)
                    
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
            lang = 'ko'
            entityId = ''
            sno = ''
            eno = ''
            if 'query' in url_params:
                query = url_params['query'][0]
                log_dbg('query={0}'.format(query))
            if 'year' in url_params:
                year = url_params['year'][0]
                log_dbg('year={0}'.format(year))
            if 'language' in url_params:
                lang = url_params['language'][0]
                log_dbg('lang={0}'.format(lang))
            if 'id' in url_params:
                entityId = url_params['id'][0]
                log_dbg('id={0}'.format(entityId))
            if 'sno' in url_params:
                sno = url_params['sno'][0]
                log_dbg('sno={0}'.format(sno))
            if 'eno' in url_params:
                eno = url_params['eno'][0]
                log_dbg('eno={0}'.format(eno))

            if (o.path == '/search/movie'):
                # 영화 검색
                if len(query) > 0:
                    resp = self.findMovies(query, year, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
                
            elif (o.path == '/movie'):
                # 영화 상세정보 조회
                if len(entityId) > 0:
                    resp = self.getMovieDetail(entityId, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
            
            elif (o.path == '/search/tv'):
                # TV쇼 검색
                if len(query) > 0:
                    resp = self.findTvShows(query, year, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
                
            elif (o.path == '/tv'):
                # TV시리즈 상세정보 조회
                if len(entityId) > 0:
                    resp = self.getTvShowDetail(entityId, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
            
            elif (o.path == '/tv/episode/all'):
                # 에피소드 목록 조회
                if len(entityId) > 0:
                    resp = self.getTvShowEpList(entityId, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
            
            elif (o.path == '/tv/episode'):
                # 에피소드 상세정보 조회
                if len(entityId) > 0:
                    resp = self.getTvShowEpisode(entityId, sno, eno, lang)
                    self.sendRespMsg(resp)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
            
            elif o.path.startswith('/image/'):
                # 이미지 파일 전송
                fileName = self.path[len('/image/'):]
                log_dbg('fileName={0}'.format(fileName))
                if len(fileName) > 0:
                    self.sendRespImage(fileName)
                else:
                    log_inf('Send response(code:404)')
                    self.send_error(404)
                return
                    
            else:
                log_inf('Send response(code:404)')
                self.send_error(404)
                return
        
        except Exception as e:
            log_err(str(e))


if __name__ == '__main__':
    try:
        __addonname__ = "ScraperProxy"
        
        # 기본 인코딩을 UTF-8로 변경
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        SVC_NAME = 'SCRAPER_PROXY'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #ogging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        __logger__ = logging.getLogger(SVC_NAME)
        
        log_inf('==[STARTED]======================================')
        
        #Create a web server and define the handler to manage the
        #incoming request
        PORT_NUMBER = 8880
        server = HTTPServer(('', PORT_NUMBER), ScraperProxyHandler)
        log_inf("Started httpserver on port {0}".format(PORT_NUMBER))
        
        #Wait forever for incoming htto requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        log_inf("^C received, shutting down the web server")
        server.socket.close()
