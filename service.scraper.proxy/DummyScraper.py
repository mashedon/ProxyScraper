# -*- coding: utf-8 -*-
#import json
import simplejson as json
import logging
import re
import sqlite3
import sys
import time
#from collections import OrderedDict
from simplejson import OrderedDict
from random import random
from MockScraper import MockScraper
'''
Created on 2016. 3. 29.

@author: mashedon@gmail.com
'''

class DummyScraper(MockScraper):
    '''
    classdocs
    '''
    movieIdPrefix = 'dummy_'
    con = None

    
    def __init__(self, loggerName):
        '''
        Constructor
        '''
        MockScraper.__init__(self, loggerName)
        self.__initDB()


    def __initDB(self):
        try:
            self.con = sqlite3.connect(':memory:')
            cur = self.con.cursor()
            
            try:
                cur.execute('CREATE TABLE TB_MOVIE (ID text, TITLE text, YEAR text)')
            except Exception as e: 
                self.__log_err__(str(e))
            
        except Exception as e: 
            self.__log_err__(str(e))
        
    
    def __insertMovie(self, movieId, title, year):
        try:
            cur = self.con.cursor()
            #cur.execute(u'INSERT INTO TB_MOVIE (ID, TITLE, YEAR) VALUES (?, ?, ?)', (movieId, title, year,))
            sql = "INSERT INTO TB_MOVIE (ID, TITLE, YEAR) VALUES ('{0}','{1}','{2}')".format(movieId, title, year)
            cur.execute(sql)
            self.con.commit()
            self.__log_dbg__('INSERT')
            return True
            
        except Exception as e: 
            self.__log_err__(str(e))
            return False
    
        
    def __updateMovie(self, movieId, title, year):
        try:
            cur = self.con.cursor()
            #cur.execute(u'UPDATE TB_MOVIE SET TITLE=?, YEAR=? WHERE ID=?', (movieId, title, year,))
            sql = "UPDATE TB_MOVIE SET TITLE='{0}', YEAR='{1}' WHERE ID='{2}'".format(title, year, movieId)
            cur.execute(sql)
            self.con.commit()
            return True
            
        except Exception as e: 
            self.__log_err__(str(e))
            return False
    
        
    def __selectMovie(self, movieId):
        try:
            cur = self.con.cursor()
            #cur.execute(u'SELECT ID, TITLE, YEAR FROM TB_MOVIE WHERE ID=?', (movieId, ))
            sql = "SELECT ID, TITLE, YEAR FROM TB_MOVIE WHERE ID='{0}'".format(movieId)
            cur.execute(sql)
            movieVO = cur.fetchone()
            self.__log_dbg__(movieVO)
            return movieVO
            
        except Exception as e: 
            self.__log_err__(str(e))
    

    def __selectMovieByTitle(self, title):
        try:
            cur = self.con.cursor()
            #cur.execute(u'SELECT ID, TITLE, YEAR FROM TB_MOVIE WHERE TITLE=?', (title, ))
            sql = "SELECT ID, TITLE, YEAR FROM TB_MOVIE WHERE TITLE='{0}'".format(title)
            cur.execute(sql)
            movieVO = cur.fetchone()
            self.__log_dbg__(movieVO)
            return movieVO
            
        except Exception as e: 
            self.__log_err__(str(e))
    
        
    # 영화 검색
    def findMovies4Kodi(self, query, year, lang):
        try:
            query = str(query)
            year = str(year)
            lang = str(lang)
            self.__log_inf__('query={0}'.format(query))
            self.__log_inf__('year={0}'.format(year))
            self.__log_inf__('lang={0}'.format(lang))
            
            movieVO = self.__selectMovieByTitle(query)
            if (movieVO is None):
                movieId = '{0}{1}'.format(self.movieIdPrefix, str(random())[2:7])
                if len(year) != 4:
                    year = '1999'
                self.__insertMovie(movieId, query, year)
            else:
                movieId = movieVO[0]
                if len(year) != 4:
                    year = movieVO[2]
                self.__updateMovie(movieId, query, year)
            
            kodiListDict = json.loads(self.kodiListJson, object_pairs_hook=OrderedDict)
            kodiEntityDict = json.loads(self.kodiEntityJson, object_pairs_hook=OrderedDict)
            kodiEntityDict['entity']['title'] = query
            kodiEntityDict['entity']['year'] = year
            kodiEntityDict['entity']['language'] = 'ko'
            kodiEntityDict['entity']['id'] = movieId
            kodiListDict['results'].append(kodiEntityDict)
            kodiListJson = json.dumps(kodiListDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 상세정보 조회
    def getMovieDetail4Kodi(self, movieId, lang):
        try:
            movieId = str(movieId)
            lang = str(lang)
            self.__log_inf__('movieId={0}'.format(movieId))
            self.__log_inf__('lang={0}'.format(lang))
            
            kodiMovieDict = json.loads(self.kodiDetailJson, object_pairs_hook=OrderedDict)
            movieVO = self.__selectMovie(movieId)
            if movieVO:
                movieId = movieVO[0]
                title = movieVO[1]
                year = movieVO[2]
                kodiMovieDict['details']['id'] = movieId
                kodiMovieDict['details']['title'] = title
                kodiMovieDict['details']['year'] = year
                kodiMovieDict['details']['plot'] = title
                kodiMovieDict['details']['thumb'] = 'http://127.0.0.1/image/poster.jpg'
                self.__log_dbg__(kodiMovieDict)
            
            kodiMovieJson = json.dumps(kodiMovieDict, ensure_ascii=False, separators=(',', ':'))
            self.__log_inf__(kodiMovieJson)
            return kodiMovieJson
        
        except Exception as e: 
            self.__log_err__(str(e))


if __name__ == '__main__':
    try:
        # 기본 인코딩을 UTF-8로 설정
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        SVC_NAME = 'DUMMY'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #logging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        logger = logging.getLogger(SVC_NAME)
        logger.info('==[STARTED]======================================')
        
        # 영화 검색
        query = '배트맨 대 슈퍼맨'
        year = ''
        lang = 'ko'
        scraper = DummyScraper(SVC_NAME)
        listJson = scraper.findMovies4Kodi(query, year, lang)
        logger.debug('')
        
        listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
        logger.debug(listDict)
        for resultDict in listDict['results']:
            # 검색결과에서 영화ID 추출
            movieId = resultDict['entity']['id']
            logger.debug('movieId={0}'.format(movieId))
            title = resultDict['entity']['title']
            logger.debug('title={0}'.format(title))
            
            # 상세정보 조회
            detailJson = scraper.getMovieDetail4Kodi(movieId, lang)
            logger.debug('')
        
    except Exception as e:
        logger.error(str(e))
