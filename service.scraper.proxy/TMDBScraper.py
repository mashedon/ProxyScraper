# -*- coding: utf-8 -*-
import copy
#import json
import simplejson as json
import logging
import re
import sys
import time
import urllib2
#from collections import OrderedDict
from simplejson import OrderedDict
from MockScraper import MockScraper
'''
Created on 2016. 3. 29.

@author: mashedon@gmail.com
'''

'''
[참고URL]
    - https://www.themoviedb.org/talk/526963d5760ee3490201c360

GET '/3/search/tv'
GET '/3/discover/tv'
GET '/3/tv/:id'
GET '/3/tv/:id/credits'
GET '/3/tv/:id/external_ids'
GET '/3/tv/:id/images'
GET '/3/tv/:id/translations'
GET '/3/tv/:id/season/:season_number'
GET '/3/tv/:id/season/:season_number/credits'
GET '/3/tv/:id/season/:season_number/external_ids'
GET '/3/tv/:id/season/:season_number/images'
GET '/3/tv/:id/season/:season_number/episode/:episode_number'
GET '/3/tv/:id/season/:season_number/episode/:episode_number/credits'
GET '/3/tv/:id/season/:season_number/episode/:episode_number/external_ids'
GET '/3/tv/:id/season/:season_number/episode/:episode_number/images'
GET '/3/tv/on_the_air'
GET '/3/tv/top_rated'
GET '/3/tv/popular'

'''
class TMDBScraper(MockScraper):
    '''
    classdocs
    '''
    movieIdPrefix = 'tmdb_'
    showIdPrefix = 'tmdbtv_'
    baseImageURL = 'http://image.tmdb.org/t/p/w396'
    

    def __init__(self, loggerName):
        '''
        Constructor
        '''
        MockScraper.__init__(self, loggerName)


    # 영화 검색
    # http://api.tmdb.org/3/search/movie?api_key=f7f51775877e0bb6703520952b3c7840&query=검은 사제들&year=&language=en
    def __findMovies(self, query, year, lang):
        try:
            url = 'http://api.tmdb.org/3/search/movie?api_key=f7f51775877e0bb6703520952b3c7840&query={0}&year={1}&language={2}'.format(urllib2.quote(query), year, lang)
            return self.__wget__(url)
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 정보 조회
    # http://api.tmdb.org/3/movie/8467?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getMovie(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self.__wget__(url, '{0}.{1}.json'.format(self.__convertEntityId(movieId), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 캐스팅정보 조회
    # http://api.tmdb.org/3/movie/8467/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getMovieCredits(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/credits?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self.__wget__(url, '{0}_credit.{1}.json'.format(self.__convertEntityId(movieId), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 릴리즈정보 조회
    # http://api.tmdb.org/3/movie/8467/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getMovieReleases(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/releases?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self.__wget__(url, '{0}_release.{1}.json'.format(self.__convertEntityId(movieId), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 이미지정보 조회
    # http://api.tmdb.org/3/movie/8467/images?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getMovieImages(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/images?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self.__wget__(url, '{0}_image.{1}.json'.format(self.__convertEntityId(movieId), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 검색
    # http://api.tmdb.org/3/search/tv?api_key=f7f51775877e0bb6703520952b3c7840&query=태양의 후예&year=&language=ko
    def __findTvShows(self, query, year, lang):
        try:
            url = 'http://api.tmdb.org/3/search/tv?api_key=f7f51775877e0bb6703520952b3c7840&query={0}&year={1}&language={2}'.format(urllib2.quote(query), year, lang)
            return self.__wget__(url)
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 정보 조회
    # http://api.tmdb.org/3/tv/65143?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getTvShow(self, showId, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(showId, lang)
            return self.__wget__(url, '{0}.{1}.json'.format(self.__convertEntityId(showId, False), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 캐스팅정보 조회
    # http://api.tmdb.org/3/tv/65143/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getTvShowCredits(self, showId, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/credits?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(showId, lang)
            return self.__wget__(url, '{0}_credit.{1}.json'.format(self.__convertEntityId(showId, False), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 이미지정보 조회
    # http://api.tmdb.org/3/tv/65143/images?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowImages(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/images?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self.__wget__(url, '{0}_image.{1}.json'.format(self.__convertEntityId(movieId), lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 회차정보 조회
    # http://api.tmdb.org/3/tv/65143/season/1?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowEpList(self, movieId, sno, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/season/{1}?api_key=f7f51775877e0bb6703520952b3c7840&language={2}'.format(movieId, sno, lang)
            return self.__wget__(url, '{0}_season{1}.{2}.json'.format(self.__convertEntityId(movieId), sno, lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 회차정보 상세 조회
    # http://api.tmdb.org/3/tv/65143/season/1/episode/1?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowEpisode(self, movieId, sno, eno, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=f7f51775877e0bb6703520952b3c7840&language={3}'.format(movieId, sno, eno, lang)
            return self.__wget__(url, '{0}_season{1}_episode{2}.{3}.json'.format(self.__convertEntityId(movieId), sno, eno, lang))
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화나 TV쇼 ID를 Kodi에 전달할 때, 메타정보 소스를 구분할 수 있도록 변환
    def __convertEntityId(self, entityId, movieYn = True):
        try:
            if (movieYn == False):
                return '{0}{1}'.format(self.showIdPrefix, entityId)
            else:
                return '{0}{1}'.format(self.movieIdPrefix, entityId)
        except Exception as e: 
            self.__log_err__(str(e))
            
    
    # 영화나 TV쇼 ID를 원래 메타정보 ID 형식으로 복구
    def __revertEntityId(self, entityId):
        try:
            entityId = str(entityId)
            if entityId.startswith(self.showIdPrefix):
                entityId = entityId[len(self.showIdPrefix):]
            elif entityId.startswith(self.movieIdPrefix):
                entityId = entityId[len(self.movieIdPrefix):]
            return entityId
        except Exception as e: 
            self.__log_err__(str(e))
        

    def __convertGenres(self, tmdbGenresDict):
        try:
            self.__log_inf__(tmdbGenresDict)
            kodiGenreDict = []
            for tmdbGenre in tmdbGenresDict:
                self.__log_dbg__('name={0}'.format(tmdbGenre['name']))
                kodiGenreDict.append(tmdbGenre['name'])
                
            self.__log_inf__(kodiGenreDict)
            return kodiGenreDict

        except Exception as e:
            self.__log_err__(str(e))


    def __convertList(self, tmdbListJson, kodiListDict):
        try:
            kodiEntityDictTemplate = self.__json2dict__(self.kodiEntityJson)
            
            self.__log_inf__('tmdbListJson={0}'.format(tmdbListJson))
            tmdbListDict = self.__json2dict__(tmdbListJson)
            for tmdbMovieDict in tmdbListDict['results']:
                self.__log_dbg__('tmdbMovieDict={0}'.format(tmdbMovieDict))
                kodiEntityDict = copy.deepcopy(kodiEntityDictTemplate)
                
                movieYn = True
                title = ''
                if 'name' in tmdbMovieDict:
                    title = tmdbMovieDict['name']
                    movieYn = False
                else:
                    title = tmdbMovieDict['title']
                
                year = ''
                if 'first_air_date' in tmdbMovieDict:
                    year = tmdbMovieDict['first_air_date'][0:4]
                else:
                    year = tmdbMovieDict['release_date'][0:4]
                
                kodiEntityDict['entity']['title'] = '[TMDB] {0}'.format(title)
                kodiEntityDict['entity']['year'] = year
                kodiEntityDict['entity']['language'] = tmdbMovieDict['original_language']
                kodiEntityDict['entity']['id'] = self.__convertEntityId(tmdbMovieDict['id'], movieYn)
                self.__log_dbg__('kodiEntityDict={0}'.format(kodiEntityDict))
                kodiListDict['results'].append(kodiEntityDict)
            
            return kodiListDict
        
        except Exception as e:
            self.__log_err__(str(e))
    
            
    def __convertMovie(self, tmdbMovieJson, kodiMovieDict):
        try:
            tmdbMovieDict = self.__json2dict__(tmdbMovieJson)
            
            mpaa = kodiMovieDict['mpaa']
            if (len(mpaa) == 0):
                if (tmdbMovieDict['adult'] == True):
                    mpaa = '청소년관람불가'
                else:
                    mpaa = '청소년관람가'
            
            setName = kodiMovieDict['set']
            if (tmdbMovieDict['belongs_to_collection']):
                if ('name' in tmdbMovieDict['belongs_to_collection']) and (tmdbMovieDict['belongs_to_collection']['name'] != None):
                    setName = tmdbMovieDict['belongs_to_collection']['name']
            
            plot = kodiMovieDict['plot']
            if ('overview' in tmdbMovieDict) and (tmdbMovieDict['overview'] != None):
                plot = self.__plot_escape__(tmdbMovieDict['overview'])

            posterImage = ''
            if ('poster_path' in tmdbMovieDict) and (tmdbMovieDict['poster_path'] != None):
                posterImage = '{0}{1}'.format(self.baseImageURL, tmdbMovieDict['poster_path'])

            fanartImage = ''
            if ('backdrop_path' in tmdbMovieDict) and (tmdbMovieDict['backdrop_path'] != None):
                fanartImage = '{0}{1}'.format(self.baseImageURL, tmdbMovieDict['backdrop_path'])
            
            kodiMovieDict['id'] = self.__convertEntityId(tmdbMovieDict['id'])
            kodiMovieDict['title'] = tmdbMovieDict['title']
            kodiMovieDict['originaltitle'] = tmdbMovieDict['original_title']
            kodiMovieDict['set'] = setName
            kodiMovieDict['year'] = tmdbMovieDict['release_date'][0:4]
            kodiMovieDict['premiered'] = tmdbMovieDict['release_date']
            kodiMovieDict['runtime'] = str(tmdbMovieDict['runtime'])
            kodiMovieDict['rating'] = str(tmdbMovieDict['vote_average'])
            kodiMovieDict['votes'] = str(tmdbMovieDict['vote_count'])
            kodiMovieDict['mpaa'] = mpaa
            kodiMovieDict['tagline'] = tmdbMovieDict['tagline']
            kodiMovieDict['outline'] = tmdbMovieDict['tagline']
            kodiMovieDict['plot'] = plot
            if len(posterImage) > 0:
                kodiMovieDict['thumb'].append(posterImage)
            if len(fanartImage) > 0:
                fanartDict = self.__json2dict__(self.kodiFanartJson)
                fanartDict['thumb'] = fanartImage
                kodiMovieDict['fanart'].append(fanartDict)
            kodiMovieDict['genre'] = self.__convertGenres(tmdbMovieDict['genres'])
            for countryDict in tmdbMovieDict['production_countries']:
                kodiMovieDict['country'].append(countryDict['name'])
            for productionDict in tmdbMovieDict['production_companies']:
                kodiMovieDict['studio'].append(productionDict['name'])
            
            return kodiMovieDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertCredits(self, tmdbCreditsJson, kodiMovieDict):
        try:
            tmdbCreditsDict = self.__json2dict__(tmdbCreditsJson)
            
            # 감독, 극본
            if 'crew' in tmdbCreditsDict:
                for crewDict in tmdbCreditsDict['crew']:
                    if crewDict['department'] == 'Directing':
                        kodiMovieDict['director'].append(crewDict['name'])
                    elif crewDict['department'] == 'Writing':
                        kodiMovieDict['credits'].append(crewDict['name'])
            
            # 배우
            if 'cast' in tmdbCreditsDict:
                actorDictTemplate = self.__json2dict__(self.kodiActorJson)
                for castDict in tmdbCreditsDict['cast']:
                    actorDict = copy.deepcopy(actorDictTemplate)
                    actorDict['name'] = castDict['name']
                    actorDict['role'] = castDict['character']
                    if castDict['profile_path']:
                        actorDict['thumb'] = '{0}{1}'.format(self.baseImageURL, castDict['profile_path'])
                    kodiMovieDict['actor'].append(actorDict)
            
            return kodiMovieDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertReleases(self, tmdbReleasesJson, kodiMovieDict):
        try:
            tmdbReleasesDict = self.__json2dict__(tmdbReleasesJson)
            
            # 한국 등급
            for releaseDict in tmdbReleasesDict['countries']:
                if releaseDict['iso_3166_1'] == 'KR':
                    if len(releaseDict['certification']) > 0:
                        kodiMovieDict['mpaa'] = releaseDict['certification']
                        return kodiMovieDict

            # 미국 등급
            for releaseDict in tmdbReleasesDict['countries']:
                if releaseDict['iso_3166_1'] == 'US':
                    if len(releaseDict['certification']) > 0:
                        kodiMovieDict['mpaa'] = 'RATED {0}'.format(releaseDict['certification'])
                        return kodiMovieDict
            
            return kodiMovieDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertImages(self, tmdbImagesJson, kodiMovieDict):
        try:
            tmdbImagesDict = self.__json2dict__(tmdbImagesJson)
            
            # 포스터
            if len(tmdbImagesDict['posters']) > 0:
                #kodiMovieDict['thumb'].pop()
                i = 0
                for posterDict in tmdbImagesDict['posters']:
                    posterImage = '{0}{1}'.format(self.baseImageURL, posterDict['file_path'])
                    kodiMovieDict['thumb'].append(posterImage)
                    i = i + 1
                    if (i >= 10):
                        break
            
            # 팬아트 
            if len(tmdbImagesDict['backdrops']) > 0:
                fanartDictTemplate = self.__json2dict__(self.kodiFanartJson)
                #kodiMovieDict['fanart'].pop()
                i = 0
                for fanartDict in tmdbImagesDict['backdrops']:
                    fanartImage = '{0}{1}'.format(self.baseImageURL, fanartDict['file_path'])
                    fanartDict = copy.deepcopy(fanartDictTemplate)
                    fanartDict['thumb'] = fanartImage
                    kodiMovieDict['fanart'].append(fanartDict)
                    i = i + 1
                    if (i >= 10):
                        break
            
            return kodiMovieDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertTvShow(self, tmdbTvShowJson, kodiMovieDict):
        try:
            tmdbTvShowDict = self.__json2dict__(tmdbTvShowJson)
            
            plot = kodiMovieDict['plot']
            if ('overview' in tmdbTvShowDict) and (len(tmdbTvShowDict['overview']) > 0):
                plot = self.__plot_escape__(tmdbTvShowDict['overview'])

            posterImage = ''
            if ('poster_path' in tmdbTvShowDict) and (len(tmdbTvShowDict['poster_path']) > 0):
                posterImage = '{0}{1}'.format(self.baseImageURL, tmdbTvShowDict['poster_path'])

            fanartImage = ''
            if ('backdrop_path' in tmdbTvShowDict) and (len(tmdbTvShowDict['backdrop_path']) > 0):
                fanartImage = '{0}{1}'.format(self.baseImageURL, tmdbTvShowDict['backdrop_path'])
            
            kodiMovieDict['id'] = self.__convertEntityId(tmdbTvShowDict['id'], False)
            kodiMovieDict['title'] = tmdbTvShowDict['name']
            kodiMovieDict['originaltitle'] = tmdbTvShowDict['original_name']
            #kodiMovieDict['set'] = ''
            kodiMovieDict['year'] = tmdbTvShowDict['first_air_date'][0:4]
            kodiMovieDict['premiered'] = tmdbTvShowDict['first_air_date']
            kodiMovieDict['runtime'] = str(tmdbTvShowDict['episode_run_time'][0])
            kodiMovieDict['rating'] = str(tmdbTvShowDict['vote_average'])
            kodiMovieDict['votes'] = str(tmdbTvShowDict['vote_count'])
            #kodiMovieDict['mpaa'] = ''
            #kodiMovieDict['tagline'] = ''
            #kodiMovieDict['outline'] = ''
            kodiMovieDict['plot'] = plot
            if len(posterImage) > 0:
                kodiMovieDict['thumb'].append(posterImage)
            if len(fanartImage) > 0:
                fanartDict = self.__json2dict__(self.kodiFanartJson)
                fanartDict['thumb'] = fanartImage
                kodiMovieDict['fanart'].append(fanartDict)
            kodiMovieDict['genre'] = self.__convertGenres(tmdbTvShowDict['genres'])
            kodiMovieDict['country'].append(tmdbTvShowDict['origin_country'][0])
            for productionDict in tmdbTvShowDict['networks']:
                kodiMovieDict['studio'].append(productionDict['name'])
            
            return kodiMovieDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertTvShowEpList(self, showId, tmdbEpisodesJson, kodiEpListDict):
        try:
            epDictTemplate = self.__json2dict__(self.kodiEpJson)
            
            self.__log_inf__(tmdbEpisodesJson)
            tmdbEpisodesDict = self.__json2dict__(tmdbEpisodesJson)
            showId = self.__convertEntityId(showId, False)
            sno = tmdbEpisodesDict['season_number']
            i = 0
            for tmdbEpDict in tmdbEpisodesDict['episodes']:
                title = tmdbEpDict['name']
                if (len(title) == 0):
                    title = '제 {0}화'.format(tmdbEpDict['episode_number'])
    
                stillImage = ''
                if ('still_path' in tmdbEpDict) and (tmdbEpDict['still_path'] != None):
                    stillImage = '{0}{1}'.format(self.baseImageURL, tmdbEpDict['still_path'])
    
                epDict = copy.deepcopy(epDictTemplate)
                epDict['episode']['id'] = showId
                epDict['episode']['season'] = str(sno)
                epDict['episode']['epnum'] = str(tmdbEpDict['episode_number'])
                epDict['episode']['title'] = title
                epDict['episode']['aired'] = tmdbEpDict['air_date']
                epDict['episode']['url'] = ''   # addon에서 생성
                if (stillImage != ''):
                    epDict['episode']['thumb'].append(stillImage)
                kodiEpListDict['episodeguide'].append(epDict)
                i = i + 1
            
            if (i > 0):
                return kodiEpListDict
            
            # Daum TV 회차 정보가 없으면, 가짜 회차 목록 생성하여 리턴
            for i in range(1, 100):
                epDict = copy.deepcopy(epDictTemplate)
                epDict['episode']['id'] = self.__convertEntityId(showId)
                epDict['episode']['season'] = str(sno)
                epDict['episode']['epnum'] = str(i)
                epDict['episode']['title'] = '제 {0}화'.format(i)
                epDict['episode']['aired'] = ''
                epDict['episode']['url'] = ''   # addon에서 생성
                kodiEpListDict['episodeguide'].append(epDict)
                
            return kodiEpListDict
        
        except Exception as e: 
            self.__log_err__(str(e))
            

    def __convertTvShowEpisode(self, showId, sno, eno, tmdbEpisodesJson, kodiEpDetailDict):
        try:
            # 회차 목록에서 요청한 회차정보 검색 
            self.__log_inf__(tmdbEpisodesJson)
            showId = self.__convertEntityId(showId, False)
            tmdbEpisodesDict = self.__json2dict__(tmdbEpisodesJson)
            for tmdbEpDict in tmdbEpisodesDict['episodes']:
                if (str(tmdbEpDict['episode_number']) == eno):
                    
                    title = tmdbEpDict['name']
                    if (len(title) == 0):
                        title = '제 {0}화'.format(tmdbEpDict['episode_number'])
                    
                    stillImage = ''
                    if ('still_path' in tmdbEpDict) and (tmdbEpDict['still_path'] != None):
                        stillImage = '{0}{1}'.format(self.baseImageURL, tmdbEpDict['still_path'])
        
                    detailsDict = kodiEpDetailDict['details']
                    detailsDict['id'] = showId
                    detailsDict['season'] = str(sno)
                    detailsDict['episode'] = str(eno)
                    detailsDict['title'] = title
                    detailsDict['aired'] = tmdbEpDict['air_date']
                    detailsDict['uniqueid'] = '{0}_{1}_{2}'.format(showId, sno, eno)
                    detailsDict['displayseason'] = str(sno)
                    detailsDict['displayepisode'] = str(eno)
                    detailsDict['displayafterseason'] = ''
                    #detailsDict['runtime'] = '60'
                    #detailsDict['rating'] = '7.1'
                    #detailsDict['votes'] = '52'
                    detailsDict['plot'] = self.__plot_escape__(tmdbEpDict['overview'])
                    if (stillImage != ''):
                        detailsDict['thumb'].append(stillImage)
                    #detailsDict['director'].append('Tim Van Patten')
                    #detailsDict['credits'].append('David Benioff')
                    
                    return kodiEpDetailDict
            
            #  TMDB TV 회차정보가 없으면, 가짜 회차정보 생성하여 리턴  
            detailsDict = kodiEpDetailDict['details']
            detailsDict['id'] = showId
            detailsDict['season'] = str(sno)
            detailsDict['episode'] = str(eno)
            detailsDict['title'] = '제 {0}화'.format(eno)
            detailsDict['aired'] = ''
            detailsDict['uniqueid'] = '{0}_{1}_{2}'.format(showId, sno, eno)
            detailsDict['displayseason'] = str(sno)
            detailsDict['displayepisode'] = str(eno)
            detailsDict['displayafterseason'] = ''
            #detailsDict['runtime'] = '60'
            #detailsDict['rating'] = '7.1'
            #detailsDict['votes'] = '52'
            detailsDict['plot'] = ''
            #detailsDict['thumb'].append('https://image.tmdb.org/t/p/w300/wrGWeW4WKxnaeA8sxJb2T9O6ryo.jpg')
            #detailsDict['director'].append('Tim Van Patten')
            #detailsDict['credits'].append('David Benioff')
            return kodiEpDetailDict
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 검색
    def findMovies4Kodi(self, query, year, lang):
        try:
            kodiListDict = self.__json2dict__(self.kodiListJson)
            self.__log_inf__('query={0}'.format(query))
            self.__log_inf__('year={0}'.format(year))
            self.__log_inf__('lang={0}'.format(lang))
            
            tmdbListJson = self.__findMovies(query, year, lang)
            self.__log_inf__(tmdbListJson)
            kodiListDict = self.__convertList(tmdbListJson, kodiListDict)
            kodiListJson = self.__dict2json__(kodiListDict)
            self.__log_inf__(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # 영화 상세정보 조회
    def getMovieDetail4Kodi(self, movieId, lang):
        try:
            kodiMovieDict = self.__json2dict__(self.kodiDetailJson)
            self.__log_inf__('movieId={0}'.format(movieId))
            self.__log_inf__('lang={0}'.format(lang))
            movieId = self.__revertEntityId(movieId)
            
            # 영화 정보 변환
            tmdbMovieJson = self.__getMovie(movieId, lang)
            self.__log_inf__(tmdbMovieJson)
            if tmdbMovieJson:
                kodiMovieDict['details'] = self.__convertMovie(tmdbMovieJson, kodiMovieDict['details'])
                self.__log_dbg__(kodiMovieDict)
            
            # Credit 정보 변환
            tmdbCreditsJson = self.__getMovieCredits(movieId, lang)
            self.__log_inf__(tmdbCreditsJson)
            if tmdbCreditsJson:
                kodiMovieDict['details'] = self.__convertCredits(tmdbCreditsJson, kodiMovieDict['details'])
                self.__log_dbg__(kodiMovieDict)
             
            # Release 정보 변환
            tmdbReleasesJson = self.__getMovieReleases(movieId, lang)
            self.__log_inf__(tmdbReleasesJson)
            if tmdbReleasesJson:
                kodiMovieDict['details'] = self.__convertReleases(tmdbReleasesJson, kodiMovieDict['details'])
                self.__log_dbg__(kodiMovieDict)
            
            # 이미지 정보 변환
            tmdbImagesJson = self.__getMovieImages(movieId, lang)
            self.__log_inf__(tmdbImagesJson)
            if tmdbImagesJson:
                kodiMovieDict['details'] = self.__convertImages(tmdbImagesJson, kodiMovieDict['details'])
                self.__log_dbg__(kodiMovieDict)
            
            kodiMovieJson = self.__dict2json__(kodiMovieDict)
            self.__log_inf__(kodiMovieJson)
            return kodiMovieJson
            
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 검색
    def findTvShows4Kodi(self, query, year, lang):
        try:
            kodiListDict = self.__json2dict__(self.kodiListJson)
            self.__log_inf__('query={0}'.format(query))
            self.__log_inf__('year={0}'.format(year))
            self.__log_inf__('lang={0}'.format(lang))
            year = str(year)
            
            tmdbListJson = self.__findTvShows(query, year, lang)
            self.__log_inf__(tmdbListJson)
            kodiListDict = self.__convertList(tmdbListJson, kodiListDict)
            kodiListJson = self.__dict2json__(kodiListDict)
            self.__log_inf__(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self.__log_err__(str(e))


    # TV쇼 상세정보 조회
    def getTvShowDetail4Kodi(self, showId, lang):
        try:
            kodiDetailDict = self.__json2dict__(self.kodiDetailJson)
            self.__log_inf__('showId={0}'.format(showId))
            showId = self.__revertEntityId(showId)
            
            # TV쇼 정보 변환
            tmdbTvShowJson = self.__getTvShow(showId, lang)
            self.__log_inf__(tmdbTvShowJson)
            kodiDetailDict['details'] = self.__convertTvShow(tmdbTvShowJson, kodiDetailDict['details'])
            self.__log_dbg__(kodiDetailDict)
            
            # Credit 정보 변환
            tmdbCreditsJson = self.__getTvShowCredits(showId, lang)
            self.__log_inf__(tmdbCreditsJson)
            kodiDetailDict['details'] = self.__convertCredits(tmdbCreditsJson, kodiDetailDict['details'])
            self.__log_dbg__(kodiDetailDict)
            
            # 이미지 정보 변환
            tmdbImagesJson = self.__getTvShowImages(showId, lang)
            self.__log_inf__(tmdbImagesJson)
            kodiDetailDict['details'] = self.__convertImages(tmdbImagesJson, kodiDetailDict['details'])
            self.__log_dbg__(kodiDetailDict)
            
            kodiMovieJson = self.__dict2json__(kodiDetailDict)
            self.__log_inf__(kodiMovieJson)
            return kodiMovieJson
            
        except Exception as e: 
            self.__log_err__(str(e))
        

    # 에피소드 목록 조회
    def getTvShowEpList4Kodi(self, showId, lang):
        try:
            kodiEpListDict = self.__json2dict__(self.kodiEpListJson)
            self.__log_inf__('showId={0}'.format(showId))
            showId = self.__revertEntityId(showId)

            # TV쇼 정보 변환
            tmdbTvShowJson = self.__getTvShow(showId, lang)
            self.__log_inf__(tmdbTvShowJson)
            tmdbTvShowDict = self.__json2dict__(tmdbTvShowJson)
            
            seasonCount = tmdbTvShowDict['number_of_seasons']
            for season in range(1, (seasonCount+1)):
                tmdbEpisodesJson = self.__getTvShowEpList(showId, season, lang)
                self.__log_inf__(tmdbEpisodesJson)
                self.__convertTvShowEpList(showId, tmdbEpisodesJson, kodiEpListDict)

            kodiEpListJson = self.__dict2json__(kodiEpListDict)
            self.__log_inf__(kodiEpListJson)
            return kodiEpListJson

        except Exception as e: 
            self.__log_err__(str(e))

            
    # 에피소드 상세정보 조회
    def getTvShowEpisode4Kodi(self, showId, sno, eno, lang):
        try:
            kodiEpDetailDict = self.__json2dict__(self.kodiEpDetailJson)
            self.__log_inf__('showId={0}'.format(showId))
            self.__log_inf__('sno={0}'.format(sno))
            self.__log_inf__('eno={0}'.format(eno))
            showId = self.__revertEntityId(showId)
            sno = str(sno)
            eno = str(eno)
            
            # 요청 시즌과 일치하는 시즌의 에피소드 정보를 조회
            tmdbEpisodesJson = self.__getTvShowEpList(showId, sno, lang)
            self.__log_inf__(tmdbEpisodesJson)
            kodiEpDetailDict = self.__convertTvShowEpisode(showId, sno, eno, tmdbEpisodesJson, kodiEpDetailDict)
            
            kodiEpDetailJson = self.__dict2json__(kodiEpDetailDict)
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
        SVC_NAME = 'TMDB'
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
    #     scraper = TMDBScraper(SVC_NAME)
    #     listJson = scraper.findMovies4Kodi(query, year, lang)
    #     logger.debug(listJson)
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
    #         logger.debug(detailJson)
    #         logger.debug('')
    #          
    #         break;
        
        # TV쇼 검색
        query = '태양의 후예'
        year = ''
        lang = 'ko'
        tvscraper = TMDBScraper(SVC_NAME)
        listJson = tvscraper.findTvShows4Kodi(query, year, lang)
        logger.debug('')
        
        listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
        logger.debug(listDict)
        for resultDict in listDict['results']:
            # 검색결과에서 영화ID 추출
            showId = resultDict['entity']['id']
            logger.debug('showId={0}'.format(showId))
            title = resultDict['entity']['title']
            logger.debug('title={0}'.format(title))
              
            # 상세정보 조회
            detailJson = tvscraper.getTvShowDetail4Kodi(showId, lang)
            logger.debug('')
     
            # 에피소드 조회
            detailJson = tvscraper.getTvShowEpList4Kodi(showId, lang)
            logger.debug('')
         
            # 에피소드 상세정보 조회
            detailJson = tvscraper.getTvShowEpisode4Kodi(showId, '1', '5', lang)
            logger.debug('')
    
            break
        
    except Exception as e:
        logger.error(str(e))
