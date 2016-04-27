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
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 정보 조회
    # http://api.tmdb.org/3/movie/8467?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getMovie(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 캐스팅정보 조회
    # http://api.tmdb.org/3/movie/8467/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getMovieCredits(self, movieId, lang):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/credits?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 릴리즈정보 조회
    # http://api.tmdb.org/3/movie/8467/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getMovieReleases(self, movieId, lang=''):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/releases?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 이미지정보 조회
    # http://api.tmdb.org/3/movie/8467/images?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getMovieImages(self, movieId, lang=''):
        try:
            url = 'http://api.tmdb.org/3/movie/{0}/images?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(movieId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 검색
    # http://api.tmdb.org/3/search/tv?api_key=f7f51775877e0bb6703520952b3c7840&query=태양의 후예&year=&language=ko
    def __findTvShows(self, query, year, lang):
        try:
            url = 'http://api.tmdb.org/3/search/tv?api_key=f7f51775877e0bb6703520952b3c7840&query={0}&year={1}&language={2}'.format(urllib2.quote(query), year, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 정보 조회
    # http://api.tmdb.org/3/tv/65143?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getTvShow(self, showId, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(showId, lang)
            cacheName = '{0}.{1}.json'.format(self.__convertEntityId(showId, False), lang)
            return self._wget(url, cacheName, 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 캐스팅정보 조회
    # http://api.tmdb.org/3/tv/65143/credits?api_key=f7f51775877e0bb6703520952b3c7840&language=ko
    def __getTvShowCredits(self, showId, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/credits?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(showId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 이미지정보 조회
    # http://api.tmdb.org/3/tv/65143/images?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowImages(self, showId, lang=''):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/images?api_key=f7f51775877e0bb6703520952b3c7840&language={1}'.format(showId, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 시즌별 이미지정보 조회
    # http://api.tmdb.org/3/tv/65143/season/1/images?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowSeasonImages(self, showId, sno, lang=''):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/season/{1}/images?api_key=f7f51775877e0bb6703520952b3c7840&language={2}'.format(showId, sno, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 회차정보 조회
    # http://api.tmdb.org/3/tv/65143/season/1?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowEpList(self, showId, sno, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/season/{1}?api_key=f7f51775877e0bb6703520952b3c7840&language={2}'.format(showId, sno, lang)
            cacheName = '{0}_season{1}.{2}.json'.format(self.__convertEntityId(showId), sno, lang)
            return self._wget(url, cacheName, 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 회차정보 상세 조회
    # http://api.tmdb.org/3/tv/65143/season/1/episode/1?api_key=f7f51775877e0bb6703520952b3c7840&language=en
    def __getTvShowEpisode(self, showId, sno, eno, lang):
        try:
            url = 'http://api.tmdb.org/3/tv/{0}/season/{1}/episode/{2}?api_key=f7f51775877e0bb6703520952b3c7840&language={3}'.format(showId, sno, eno, lang)
            return self._wget(url, '', 'dbg')
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화나 TV쇼 ID를 Kodi에 전달할 때, 메타정보 소스를 구분할 수 있도록 변환
    def __convertEntityId(self, entityId, movieYn = True):
        try:
            if (movieYn == False):
                return '{0}{1}'.format(self.showIdPrefix, entityId)
            else:
                return '{0}{1}'.format(self.movieIdPrefix, entityId)
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            
    
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
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
        

    def __convertGenres(self, tmdbGenresDict):
        try:
            kodiGenreDict = []
            for tmdbGenre in tmdbGenresDict:
                kodiGenreDict.append(tmdbGenre['name'])
            return kodiGenreDict

        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    def __convertList(self, kodiListDict, tmdbListJson, year, lang):
        try:
            kodiEntityDictTemplate = self._json2dict(self.kodiEntityJson)
            
            tmdbListDict = self._json2dict(tmdbListJson)
            if ('results' in tmdbListDict) and (tmdbListDict['results'] != None):
                for tmdbMovieDict in tmdbListDict['results']:
                    
                    movieYn = True
                    releaseDate = ''
                    title = ''
                    originalTitle = ''
                    if ('release_date' in tmdbMovieDict):
                        movieYn = True
                        releaseDate = tmdbMovieDict['release_date']
                        title = tmdbMovieDict['title']
                        originalTitle = tmdbMovieDict['original_title'] 
                    else:
                        movieYn = False
                        releaseDate = tmdbMovieDict['first_air_date']
                        title = tmdbMovieDict['name']
                        originalTitle = tmdbMovieDict['original_name'] 
                    
                    # 요청항목에 연도가 있다면, 같은 연도 영화만 검색
                    releaseYear = releaseDate[0:4]
                    if (len(year) == 4) and (year != releaseYear):
                        continue
                    
                    if (tmdbMovieDict['original_language'] == 'ko'):
                        title = originalTitle
                        lang = 'ko'
                    
                    kodiEntityDict = copy.deepcopy(kodiEntityDictTemplate)
                    kodiEntityDict['entity']['title'] = '[TMDB] {0}'.format(title)
                    kodiEntityDict['entity']['year'] = releaseYear
                    kodiEntityDict['entity']['language'] = lang
                    kodiEntityDict['entity']['id'] = self.__convertEntityId(tmdbMovieDict['id'], movieYn)
                    kodiListDict['results'].append(kodiEntityDict)
                    
                    if (lang == 'ko') and (originalTitle != title) and (originalTitle != ''):
                        kodiEntityDict = copy.deepcopy(kodiEntityDictTemplate)
                        kodiEntityDict['entity']['title'] = '[TMDB] {0}'.format(originalTitle)
                        kodiEntityDict['entity']['year'] = releaseYear
                        kodiEntityDict['entity']['language'] = lang
                        kodiEntityDict['entity']['id'] = self.__convertEntityId(tmdbMovieDict['id'], movieYn)
                        kodiListDict['results'].append(kodiEntityDict)
                    
            return kodiListDict
        
        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
    
            
    def __convertMovie(self, kodiMovieDict, tmdbMovieJson, lang):
        try:
            tmdbMovieDict = self._json2dict(tmdbMovieJson)
            
            mpaa = kodiMovieDict['mpaa']
            if (len(mpaa) == 0):
                if (tmdbMovieDict['adult'] == True):
                    mpaa = '청소년관람불가'
                else:
                    mpaa = '청소년관람가'
            
            if (tmdbMovieDict['original_language'] == 'ko'):
                # 국내 영화는 한글제목
                title = self._nvl(tmdbMovieDict['original_title'], tmdbMovieDict['title'])
                originalTitle = ''
            else:
                title = tmdbMovieDict['title']
                originalTitle = self._nvl(tmdbMovieDict['original_title'], '')
            
            # 제목과 원제가 동일하면 원제 삭제
            if (originalTitle == title):
                originalTitle = ''
            
            setName = kodiMovieDict['set']
            if (tmdbMovieDict['belongs_to_collection']):
                if ('name' in tmdbMovieDict['belongs_to_collection']) and (tmdbMovieDict['belongs_to_collection']['name'] != None):
                    setName = tmdbMovieDict['belongs_to_collection']['name']
            
            plot = kodiMovieDict['plot']
            if ('overview' in tmdbMovieDict) and (tmdbMovieDict['overview'] != None):
                plot = self._plot_escape(tmdbMovieDict['overview'])

            posterImage = ''
            if ('poster_path' in tmdbMovieDict) and (tmdbMovieDict['poster_path'] != None):
                posterImage = '{0}{1}'.format(self.baseImageURL, tmdbMovieDict['poster_path'])

            fanartImage = ''
            if ('backdrop_path' in tmdbMovieDict) and (tmdbMovieDict['backdrop_path'] != None):
                fanartImage = '{0}{1}'.format(self.baseImageURL, tmdbMovieDict['backdrop_path'])
            
            kodiMovieDict['id'] = self.__convertEntityId(tmdbMovieDict['id'])
            kodiMovieDict['title'] = title
            kodiMovieDict['originaltitle'] = originalTitle
            kodiMovieDict['set'] = setName
            kodiMovieDict['year'] = tmdbMovieDict['release_date'][0:4]
            kodiMovieDict['premiered'] = tmdbMovieDict['release_date']
            kodiMovieDict['runtime'] = str(tmdbMovieDict['runtime'])
            kodiMovieDict['rating'] = str(tmdbMovieDict['vote_average'])
            kodiMovieDict['votes'] = str(tmdbMovieDict['vote_count'])
            kodiMovieDict['mpaa'] = mpaa
            kodiMovieDict['tagline'] = tmdbMovieDict['tagline']
            #kodiMovieDict['outline'] = tmdbMovieDict['tagline']
            kodiMovieDict['plot'] = plot
            if len(posterImage) > 0:
                kodiMovieDict['thumb'].append(posterImage)
            if len(fanartImage) > 0:
                fanartDict = self._json2dict(self.kodiFanartJson)
                fanartDict['thumb'] = fanartImage
                kodiMovieDict['fanart'].append(fanartDict)
            kodiMovieDict['genre'] = self.__convertGenres(tmdbMovieDict['genres'])
            for countryDict in tmdbMovieDict['production_countries']:
                kodiMovieDict['country'].append(countryDict['name'])
            for productionDict in tmdbMovieDict['production_companies']:
                kodiMovieDict['studio'].append(productionDict['name'])
            
            return kodiMovieDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertCredits(self, kodiMovieDict, tmdbCreditsJson):
        try:
            tmdbCreditsDict = self._json2dict(tmdbCreditsJson)
            
            # 감독, 극본
            if 'crew' in tmdbCreditsDict:
                for crewDict in tmdbCreditsDict['crew']:
                    if crewDict['department'] == 'Directing':
                        kodiMovieDict['director'].append(crewDict['name'])
                    elif crewDict['department'] == 'Writing':
                        kodiMovieDict['credits'].append(crewDict['name'])
            
            # 배우
            if 'cast' in tmdbCreditsDict:
                actorDictTemplate = self._json2dict(self.kodiActorJson)
                for castDict in tmdbCreditsDict['cast']:
                    actorDict = copy.deepcopy(actorDictTemplate)
                    actorDict['name'] = castDict['name']
                    actorDict['role'] = castDict['character']
                    if castDict['profile_path']:
                        actorDict['thumb'] = '{0}{1}'.format(self.baseImageURL, castDict['profile_path'])
                    kodiMovieDict['actor'].append(actorDict)
            
            return kodiMovieDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertReleases(self, kodiMovieDict, tmdbReleasesJson):
        try:
            tmdbReleasesDict = self._json2dict(tmdbReleasesJson)
            
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
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertImages(self, kodiMovieDict, tmdbImagesJson):
        try:
            tmdbImagesDict = self._json2dict(tmdbImagesJson)
            
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
                fanartDictTemplate = self._json2dict(self.kodiFanartJson)
                #kodiMovieDict['fanart'].pop()
                j = 0
                for fanartDict in tmdbImagesDict['backdrops']:
                    fanartImage = '{0}{1}'.format(self.baseImageURL, fanartDict['file_path'])
                    fanartDict = copy.deepcopy(fanartDictTemplate)
                    fanartDict['thumb'] = fanartImage
                    kodiMovieDict['fanart'].append(fanartDict)
                    j = j + 1
                    if (j >= 10):
                        break
            
            return kodiMovieDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertTvShow(self, kodiMovieDict, tmdbTvShowJson):
        try:
            tmdbTvShowDict = self._json2dict(tmdbTvShowJson)
            
            if ('original_language' in tmdbTvShowDict) and (tmdbTvShowDict['original_language'] == 'ko'):
                title = self._nvl(tmdbTvShowDict['original_name'], tmdbTvShowDict['name']) 
                originalTitle = '' 
                lang = 'ko'
            else:
                title = tmdbTvShowDict['name']
                originalTitle = self._nvl(tmdbTvShowDict['original_name'], '')
                lang = 'en'
            
            # 제목과 원제가 동일하면 원제 삭제
            if (originalTitle == title):
                originalTitle = ''
            
            plot = kodiMovieDict['plot']
            if ('overview' in tmdbTvShowDict) and (tmdbTvShowDict['overview'] != None) and (len(tmdbTvShowDict['overview']) > 0):
                plot = self._plot_escape(tmdbTvShowDict['overview'])

            posterImage = ''
            if ('poster_path' in tmdbTvShowDict) and (len(tmdbTvShowDict['poster_path']) != None) and (len(tmdbTvShowDict['poster_path']) > 0):
                posterImage = '{0}{1}'.format(self.baseImageURL, tmdbTvShowDict['poster_path'])

            fanartImage = ''
            if ('backdrop_path' in tmdbTvShowDict) and (len(tmdbTvShowDict['backdrop_path']) != None) and (len(tmdbTvShowDict['backdrop_path']) > 0):
                fanartImage = '{0}{1}'.format(self.baseImageURL, tmdbTvShowDict['backdrop_path'])
            
            kodiMovieDict['id'] = self.__convertEntityId(tmdbTvShowDict['id'], False)
            kodiMovieDict['title'] = title
            kodiMovieDict['originaltitle'] = originalTitle
            #kodiMovieDict['set'] = ''
            kodiMovieDict['year'] = tmdbTvShowDict['first_air_date'][0:4]
            kodiMovieDict['premiered'] = tmdbTvShowDict['first_air_date']
            kodiMovieDict['language'] = lang
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
                fanartDict = self._json2dict(self.kodiFanartJson)
                fanartDict['thumb'] = fanartImage
                kodiMovieDict['fanart'].append(fanartDict)
            kodiMovieDict['genre'] = self.__convertGenres(tmdbTvShowDict['genres'])
            kodiMovieDict['country'].append(tmdbTvShowDict['origin_country'][0])
            for productionDict in tmdbTvShowDict['networks']:
                kodiMovieDict['studio'].append(productionDict['name'])
            
            return kodiMovieDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
    
            
    def __convertTvShowImageList(self, tmdbImageListJson, showId, sno = ''):
        try:
            tmdbImageListDict = self._json2dict(tmdbImageListJson)
            listXml = ''
            
            # 포스터 이미지(세로로 긴 이미지)
            if ('posters' in tmdbImageListDict):
                for imageDict in tmdbImageListDict['posters']:
                    if (sno == ''):
                        listXml += '<thumb aspect="poster">%s</thumb>' % (sno, '{0}{1}'.format(self.baseImageURL, imageDict['file_path']))
                    else:
                        listXml += '<thumb aspect="poster" type="season" season="%s">%s</thumb>' % (sno, '{0}{1}'.format(self.baseImageURL, imageDict['file_path']))
            
            # 팬아트 이미지(가로로 넓은 이미지)
            if ('backdrops' in tmdbImageListDict):
                listXml += '<fanart url="%s">' % (self.baseImageURL)
                for imageDict in tmdbImageListDict['backdrops']:
                    if (sno == ''):
                        listXml += '<thumb aspect="poster">%s</thumb>' % (sno, imageDict['file_path'])
                    else:
                        listXml += '<thumb aspect="poster" type="season" season="%s">%s</thumb>' % (sno, imageDict['file_path'])
                listXml += '</fanart>'
            
            return listXml
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
        

    def __convertTvShowEpList(self, kodiEpListDict, tmdbEpisodesJson, showId, lang):
        try:
            epDictTemplate = self._json2dict(self.kodiEpJson)
            
            tmdbEpisodesDict = self._json2dict(tmdbEpisodesJson)
            showId = self.__convertEntityId(showId, False)
            sno = str(tmdbEpisodesDict['season_number'])
            i = 0
            for tmdbEpDict in tmdbEpisodesDict['episodes']:
                title = tmdbEpDict['name']
                if (title is None) or (title == ''):
                    title = self._title_format(tmdbEpDict['episode_number'], lang)
    
                stillImage = ''
                if ('still_path' in tmdbEpDict) and (tmdbEpDict['still_path'] != None):
                    stillImage = '{0}{1}'.format(self.baseImageURL, tmdbEpDict['still_path'])
                    
                eno = str(tmdbEpDict['episode_number'])
    
                epDict = copy.deepcopy(epDictTemplate)
                detailsDict = epDict['episode'] 
                detailsDict['id'] = str(tmdbEpDict['id'])
                detailsDict['season'] = sno
                detailsDict['epnum'] = eno
                detailsDict['title'] = title
                detailsDict['aired'] = tmdbEpDict['air_date']
                detailsDict['url'] = ''   # addon에서 생성
                detailsDict['uniqueid'] = '{0}-{1}-{2}'.format(showId, sno, eno)
                detailsDict['displayseason'] = sno
                detailsDict['displayepisode'] = eno
                detailsDict['displayafterseason'] = ''
                #detailsDict['runtime'] = '60'
                #detailsDict['rating'] = '7.1'
                #detailsDict['votes'] = '52'
                detailsDict['plot'] = self._plot_escape(tmdbEpDict['overview'])
                if (stillImage != ''):
                    detailsDict['thumb'].append(stillImage)
                #detailsDict['director'].append('Tim Van Patten')
                #detailsDict['credits'].append('David Benioff')
                kodiEpListDict['episodeguide'].append(epDict)
                i = i + 1
            
            if (i == 0):
                # TV 회차 정보가 없으면, 가짜 회차 목록 생성하여 리턴
                for i in range(1, 100):
                    epDict = copy.deepcopy(epDictTemplate)
                    detailsDict = epDict['episode'] 
                    detailsDict['id'] = '{0}-{1}-{2}'.format(showId, sno, i)
                    detailsDict['season'] = sno
                    detailsDict['epnum'] = str(i)
                    detailsDict['title'] = self._title_format(i, lang)
                    detailsDict['aired'] = ''
                    detailsDict['url'] = ''   # addon에서 생성
                    detailsDict['uniqueid'] = detailsDict['id']
                    detailsDict['displayseason'] = detailsDict['season']
                    detailsDict['displayepisode'] = detailsDict['epnum']
                    detailsDict['displayafterseason'] = ''
                    #detailsDict['runtime'] = '60'
                    #detailsDict['rating'] = '7.1'
                    #detailsDict['votes'] = '52'
                    detailsDict['plot'] = '.'
                    #detailsDict['thumb'].append('https://image.tmdb.org/t/p/w300/wrGWeW4WKxnaeA8sxJb2T9O6ryo.jpg')
                    #detailsDict['director'].append('Tim Van Patten')
                    #detailsDict['credits'].append('David Benioff')
                    kodiEpListDict['episodeguide'].append(epDict)
                
            kodiEpListDict['language'] = lang
            return kodiEpListDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertTvShowEpisode(self, kodiEpDetailDict, tmdbEpisodesJson, showId, sno, eno, lang):
        try:
            # 회차 목록에서 요청한 회차정보 검색 
            showId = self.__convertEntityId(showId, False)
            sno = str(sno)
            eno = str(eno)
            tmdbEpisodesDict = self._json2dict(tmdbEpisodesJson)
            for tmdbEpDict in tmdbEpisodesDict['episodes']:
                if (str(tmdbEpDict['episode_number']) == eno):
                    
                    title = tmdbEpDict['name']
                    if (len(title) == 0):
                        title = self._title_format(tmdbEpDict['episode_number'], lang)
                    
                    stillImage = ''
                    if ('still_path' in tmdbEpDict) and (tmdbEpDict['still_path'] != None):
                        stillImage = '{0}{1}'.format(self.baseImageURL, tmdbEpDict['still_path'])
        
                    detailsDict = kodiEpDetailDict['details']
                    detailsDict['id'] = str(tmdbEpDict['id'])
                    detailsDict['season'] = sno
                    detailsDict['episode'] = eno
                    detailsDict['title'] = title
                    detailsDict['aired'] = tmdbEpDict['air_date']
                    detailsDict['uniqueid'] = '{0}-{1}-{2}'.format(showId, sno, eno)
                    detailsDict['displayseason'] = sno
                    detailsDict['displayepisode'] = eno
                    detailsDict['displayafterseason'] = ''
                    #detailsDict['runtime'] = '60'
                    #detailsDict['rating'] = '7.1'
                    #detailsDict['votes'] = '52'
                    detailsDict['plot'] = self._plot_escape(tmdbEpDict['overview'])
                    if (stillImage != ''):
                        detailsDict['thumb'].append(stillImage)
                    #detailsDict['director'].append('Tim Van Patten')
                    #detailsDict['credits'].append('David Benioff')
                    
                    return kodiEpDetailDict
            
            #  TMDB TV 회차정보가 없으면, 가짜 회차정보 생성하여 리턴  
            detailsDict = kodiEpDetailDict['details']
            detailsDict['id'] = '{0}-{1}-{2}'.format(showId, sno, eno)
            detailsDict['season'] = sno
            detailsDict['episode'] = eno
            detailsDict['title'] = '제 {0}화'.format(eno)
            detailsDict['aired'] = ''
            detailsDict['uniqueid'] = detailsDict['id'] 
            detailsDict['displayseason'] = detailsDict['season']
            detailsDict['displayepisode'] = detailsDict['episode']
            detailsDict['displayafterseason'] = ''
            #detailsDict['runtime'] = '60'
            #detailsDict['rating'] = '7.1'
            #detailsDict['votes'] = '52'
            detailsDict['plot'] = '.'
            #detailsDict['thumb'].append('https://image.tmdb.org/t/p/w300/wrGWeW4WKxnaeA8sxJb2T9O6ryo.jpg')
            #detailsDict['director'].append('Tim Van Patten')
            #detailsDict['credits'].append('David Benioff')
            return kodiEpDetailDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 검색
    def findMovies4Kodi(self, query, year, lang):
        try:
            kodiListDict = self._json2dict(self.kodiListJson)
            self._log_dbg('{0}.{1}: query={2}, year={3}, lang={4}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, query, year, lang))
            
            tmdbListJson = self.__findMovies(query, year, lang)
            kodiListDict = self.__convertList(kodiListDict, tmdbListJson, year, lang)
            kodiListJson = self._dict2json(kodiListDict)
            self._log_dbg(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 상세정보 조회
    def getMovieDetail4Kodi(self, movieId, lang, imageSrc):
        try:
            kodiMovieDict = self._json2dict(self.kodiDetailJson)
            self._log_dbg('{0}.{1}: movieId={2}, lang={3}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, movieId, lang))
            movieId = self.__revertEntityId(movieId)
            
            # 영화 정보 변환
            tmdbMovieJson = self.__getMovie(movieId, lang)
            if tmdbMovieJson:
                kodiMovieDict['details'] = self.__convertMovie(kodiMovieDict['details'], tmdbMovieJson, lang)
                self._log_dbg(kodiMovieDict)
            
            # Credit 정보 변환
            tmdbCreditsJson = self.__getMovieCredits(movieId, lang)
            if tmdbCreditsJson:
                kodiMovieDict['details'] = self.__convertCredits(kodiMovieDict['details'], tmdbCreditsJson)
                self._log_dbg(kodiMovieDict)
             
            # Release 정보 변환
            tmdbReleasesJson = self.__getMovieReleases(movieId)
            if tmdbReleasesJson:
                kodiMovieDict['details'] = self.__convertReleases(kodiMovieDict['details'], tmdbReleasesJson)
                self._log_dbg(kodiMovieDict)
            
            # 이미지 정보 변환
            tmdbImagesJson = self.__getMovieImages(movieId)
            if tmdbImagesJson:
                kodiMovieDict['details'] = self.__convertImages(kodiMovieDict['details'], tmdbImagesJson)
                self._log_dbg(kodiMovieDict)
            
            kodiMovieJson = self._dict2json(kodiMovieDict)
            self._log_dbg(kodiMovieJson)
            return kodiMovieJson
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 검색
    def findTvShows4Kodi(self, query, year, lang):
        try:
            kodiListDict = self._json2dict(self.kodiListJson)
            self._log_dbg('{0}.{1}: query={2}, year={3}, lang={4}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, query, year, lang))
            year = str(year)
            
            tmdbListJson = self.__findTvShows(query, year, lang)
            kodiListDict = self.__convertList(kodiListDict, tmdbListJson, year, lang)
            kodiListJson = self._dict2json(kodiListDict)
            self._log_dbg(kodiListJson)
            return kodiListJson
        
        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 상세정보 조회
    def getTvShowDetail4Kodi(self, showId, lang):
        try:
            kodiDetailDict = self._json2dict(self.kodiDetailJson)
            self._log_dbg('{0}.{1}: showId={2}, lang={3}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, showId, lang))
            showId = self.__revertEntityId(showId)
            
            # TV쇼 정보 변환
            tmdbTvShowJson = self.__getTvShow(showId, lang)
            kodiDetailDict['details'] = self.__convertTvShow(kodiDetailDict['details'], tmdbTvShowJson)
            self._log_dbg(kodiDetailDict)
            
            # Credit 정보 변환
            #tmdbCreditsJson = self.__getTvShowCredits(showId, lang)
            tmdbCreditsJson = self.__getTvShowCredits(showId, 'en')
            kodiDetailDict['details'] = self.__convertCredits(kodiDetailDict['details'], tmdbCreditsJson)
            self._log_dbg(kodiDetailDict)
            
            # 이미지 정보 변환
            #tmdbImagesJson = self.__getTvShowImages(showId, lang)
            tmdbImagesJson = self.__getTvShowImages(showId)
            kodiDetailDict['details'] = self.__convertImages(kodiDetailDict['details'], tmdbImagesJson)
            self._log_dbg(kodiDetailDict)
            
            kodiMovieJson = self._dict2json(kodiDetailDict)
            self._log_dbg(kodiMovieJson)
            return kodiMovieJson
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
        

    # 에피소드 목록 조회
    def getTvShowEpList4Kodi(self, showId, lang):
        try:
            kodiEpListDict = self._json2dict(self.kodiEpListJson)
            self._log_dbg('{0}.{1}: showId={2}, lang={3}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, showId, lang))
            showId = self.__revertEntityId(showId)

            # TV쇼 정보 변환
            tmdbTvShowJson = self.__getTvShow(showId, lang)
            tmdbTvShowDict = self._json2dict(tmdbTvShowJson)
            
            # 에피소드 상세내용은 한국 드라마는 한글로, 외화는 영문으로 조회
            if ('original_language' in tmdbTvShowDict) and (tmdbTvShowDict['original_language'] == 'ko'):
                lang = 'ko'
            else:
                lang = 'en'
            
            # 각 시즌별 에피소드 목록 조회
            seasonCount = tmdbTvShowDict['number_of_seasons']
            for season in range(1, (seasonCount+1)):
                tmdbEpisodesJson = self.__getTvShowEpList(showId, season, lang)
                self.__convertTvShowEpList(kodiEpListDict, tmdbEpisodesJson, showId, lang)

            kodiEpListJson = self._dict2json(kodiEpListDict)
            self._log_dbg(kodiEpListJson)
            return kodiEpListJson

        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))

            
    # 에피소드 상세정보 조회
    def getTvShowEpisode4Kodi(self, showId, sno, eno, lang):
        try:
#             kodiEpDetailDict = self._json2dict(self.kodiEpDetailJson)
#             self._log_dbg('{0}.{1}: showId={2}, sno={3}, eno={4}, lang={5}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, showId, sno, eno, lang))
#             showId = self.__revertEntityId(showId)
#             sno = str(sno)
#             eno = str(eno)
#             
#             # 요청 시즌과 일치하는 시즌의 에피소드 정보를 조회
#             tmdbEpisodesJson = self.__getTvShowEpList(showId, sno, lang)
#             kodiEpDetailDict = self.__convertTvShowEpisode(kodiEpDetailDict, tmdbEpisodesJson, showId, sno, eno, lang)
#             kodiEpDetailJson = self._dict2json(kodiEpDetailDict)
#             self._log_dbg(kodiEpDetailJson)
#             return kodiEpDetailJson
            return '{"error":"deprecated"}'
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    def getTvShowImages4Kodi(self, showId, lang):
        try:
            showId = self.__revertEntityId(showId)
            
            # TV쇼 정보 변환
            tmdbTvShowJson = self.__getTvShow(showId, lang)
            self._log_dbg(tmdbTvShowJson)
            tmdbTvShowDict = self._json2dict(tmdbTvShowJson)
            
            # 에피소드 상세내용은 한국 드라마는 한글로, 외화는 영문으로 조회
            if ('original_language' in tmdbTvShowDict) and (tmdbTvShowDict['original_language'] == 'ko'):
                lang = 'ko'
            else:
                lang = 'en'
            
            # 각 시즌별 이미지 목록 조회
            kodiImagesXml = '<details>'
            seasonCount = tmdbTvShowDict['number_of_seasons']
            for season in range(1, (seasonCount+1)):
                tmdbImagesJson = self.__getTvShowSeasonImages(showId, season)
                kodiImagesXml += self.__convertTvShowImageList(tmdbImagesJson, showId, season)
            kodiImagesXml += '</details>'
            
            self._log_dbg(kodiImagesXml)
            return kodiImagesXml

        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
        

if __name__ == '__main__':
    try:
        # 기본 인코딩을 UTF-8로 설정
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        SVC_NAME = 'TMDB'
        #LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #logging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        logger = logging.getLogger(SVC_NAME)
        logger.info('==[STARTED]======================================')
     
        # 영화 검색
        #query = '장화 홍련'
        query = '트랜스포머'
        year = ''
        lang = 'ko'
        scraper = TMDBScraper(SVC_NAME)
        listJson = scraper.findMovies4Kodi(query, year, lang)
        logger.debug(listJson)
        logger.debug('')
          
        listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
        logger.debug(listDict)
        for resultDict in listDict['results']:
            # 검색결과에서 영화ID 추출
            movieId = resultDict['entity']['id']
            logger.debug('movieId={0}'.format(movieId))
            title = resultDict['entity']['title']
            logger.debug('title={0}'.format(title))
            lang = resultDict['entity']['language']
            logger.debug('lang={0}'.format(lang))
                
            # 상세정보 조회
            detailJson = scraper.getMovieDetail4Kodi(movieId, lang, '')
            logger.debug(detailJson)
            logger.debug('')
               
            break;
        
        exit()
        
        # TV쇼 검색
        #query = '피리부는 사나이'
        query = 'Breaking Bad'
        #query = 'friends'
        year = ''
        lang = 'ko'
        tvscraper = TMDBScraper(SVC_NAME)
        listJson = tvscraper.findTvShows4Kodi(query, year, lang)
        logger.debug('')
         
        listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
        for resultDict in listDict['results']:
            # 검색결과에서 영화ID 추출
            showId = resultDict['entity']['id']
            logger.debug('showId={0}'.format(showId))
            title = resultDict['entity']['title']
            logger.debug('title={0}'.format(title))
            lang = resultDict['entity']['language']
            logger.debug('lang={0}'.format(lang))
               
            # 상세정보 조회
            detailJson = tvscraper.getTvShowDetail4Kodi(showId, lang)
            logger.debug('')
      
            # 에피소드 조회
            detailJson = tvscraper.getTvShowEpList4Kodi(showId, lang)
            logger.debug('')
           
#             # 에피소드 상세정보 조회
#             detailJson = tvscraper.getTvShowEpisode4Kodi(showId, '1', '5', lang)
#             logger.debug('')
     
            # 시즌별 이미지 조회
            detailJson = tvscraper.getTvShowImages4Kodi(showId, lang)
            logger.debug('')
           
            break
        
    except Exception as e:
        print str(e)
