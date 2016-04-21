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

class DaumScraper(MockScraper):
    '''
    classdocs
    '''
    movieIdPrefix = 'daum_'
    showIdPrefix = 'daumtv_'
    baseImageURL = 'http://movie.daum-img.net/movie'


    def __init__(self, loggerName):
        '''
        Constructor
        '''
        MockScraper.__init__(self, loggerName)


    # 영화 검색
    # http://m.movie.daum.net/data/movie/search/movie.json?start=1&size=20&searchText=배트맨 대 슈퍼맨
    def __findMovies(self, query):
        try:
            url = 'http://m.movie.daum.net/data/movie/search/movie.json?start=1&size=20&searchText={0}'.format(urllib2.quote(query))
            return self._wget(url)
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 상세정보 조회
    # http://m.movie.daum.net/data/movie/movie_info/detail.json?movieId=79940
    def __getMovie(self, movieId):
        try:
            url = 'http://m.movie.daum.net/data/movie/movie_info/detail.json?movieId={0}'.format(movieId)
            #return self._wget(url, '{0}{1}.json'.format(self.movieIdPrefix, movieId))
            return self._wget(url)
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 배우정보 조회
    # http://m.movie.daum.net/data/movie/movie_info/cast_crew.json?pageNo=1&pageSize=20&movieId=79940
    def __getMovieCredits(self, movieId):
        try:
            url = 'http://m.movie.daum.net/data/movie/movie_info/cast_crew.json?pageNo=1&pageSize=20&movieId={0}'.format(movieId)
            #return self._wget(url, '{0}{1}_credit.json'.format(self.movieIdPrefix, movieId))
            return self._wget(url)

        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 이미지정보 조회
    # http://m.movie.daum.net/data/movie/photo/movie/list.json?pageNo=1&pageSize=10&id=79940
    def __getMovieImages(self, movieId):
        try:
            url = 'http://m.movie.daum.net/data/movie/photo/movie/list.json?pageNo=1&pageSize=10&id={0}'.format(movieId)
            #return self._wget(url, '{0}{1}_image.json'.format(self.movieIdPrefix, movieId))
            return self._wget(url)
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 예고정보 조회
    # http://m.movie.daum.net/data/movie/vclip/movie/list.json?pageNo=1&pageSize=10&id=79940
    def __getMovieTrailer(self, movieId):
        try:
            url = 'http://m.movie.daum.net/data/movie/vclip/movie/list.json?pageNo=1&pageSize=10&id={0}'.format(movieId)
            #return self._wget(url, '{0}{1}_trailer.json'.format(self.movieIdPrefix, movieId))
            return self._wget(url)

        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 검색
    # http://m.movie.daum.net/data/movie/search/tv.json?start=1&size=10&searchText=태양의 후예
    def __findTvShows(self, query):
        try:
            url = 'http://m.movie.daum.net/data/movie/search/tv.json?start=1&size=10&searchText={0}'.format(urllib2.quote(query))
            return self._wget(url)
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


#     # TV쇼 상세정보 조회
#     # http://m.movie.daum.net/data/movie/tv/detail.json?tvProgramId=65440
#     def __getTvShow(self, showId):
#         try:
#             url = 'http://m.movie.daum.net/data/movie/tv/detail.json?tvProgramId={0}'.format(showId)
#             return self._wget(url, '{0}{1}.json'.format(self.showIdPrefix, showId))
#         
#         except Exception as e: 
#             self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 상세정보 조회
    # http://m.movie.daum.net/tv/main?tvProgramId=74551
    def __getTvShowHtml(self, showId):
        try:
            url = 'http://m.movie.daum.net/tv/main?tvProgramId={0}'.format(showId)
            return self._wget(url, '{0}{1}.html'.format(self.showIdPrefix, showId))
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 사진정보 조회
    # http://m.movie.daum.net/data/movie/photo/tv/list.json?pageNo=1&pageSize=10&id=65440
    def __getTvShowImages(self, showId):
        try:
            url = 'http://m.movie.daum.net/data/movie/photo/tv/list.json?pageNo=1&pageSize=10&id={0}'.format(showId)
            #return self._wget(url, '{0}{1}_image.json'.format(self.showIdPrefix, showId))
            return self._wget(url)
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


#     # TV쇼 배우정보 조회
#     # http://m.movie.daum.net/data/movie/tv/cast_crew.json?pageNo=1&pageSize=100&tvProgramId=65440
#     def __getTvShowCredits(self, showId):
#         try:
#             url = 'http://m.movie.daum.net/data/movie/tv/cast_crew.json?pageNo=1&pageSize=100&tvProgramId={0}'.format(showId)
#             #return self._wget(url, '{0}{1}_credit.json'.format(self.showIdPrefix, showId))
#             return self._wget(url)
#         
#         except Exception as e: 
#             self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 배우정보 조회
    # http://m.movie.daum.net/tv/crew?tvProgramId=74551
    def __getTvShowCreditsHtml(self, showId):
        try:
            url = 'http://m.movie.daum.net/tv/crew?tvProgramId={0}'.format(showId)
            #return self._wget(url, '{0}{1}_credit.html'.format(self.showIdPrefix, showId))
            return self._wget(url)
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 시즌 목록 조회
    # http://m.movie.daum.net/tv/series?tvProgramId=46165
    def __getTvShowSeasonsHtml(self, showId):
        try:
            url = 'http://m.movie.daum.net/tv/series?tvProgramId={0}'.format(showId)
            return self._wget(url, '{0}{1}_seasons.html'.format(self.showIdPrefix, showId))
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 시즌 목록 조회
    def __getTvShowSeasons(self, showId):
        try:
            body = self.__getTvShowSeasonsHtml(showId)
            m = re.search('MoreView.init\([0-9]+, (\[.*\])\);(.*)MoreView.setPageCount', body, re.S)
            seasonListJson = self._dict2json(self._json2dict(m.group(1)))
            return seasonListJson
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 회차정보 조회
    # http://m.movie.daum.net/m/tv/episode?tvProgramId=65440
    def __getTvShowEpisodesHtml(self, showId):
        try:
            url = 'http://m.movie.daum.net/m/tv/episode?tvProgramId={0}'.format(showId)
            return self._wget(url, '{0}{1}_episode.html'.format(self.showIdPrefix, showId))
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # TV쇼 회차정보 조회
    def __getTvShowEpisodes(self, showId):
        try:
            body = self.__getTvShowEpisodesHtml(showId)
            m = re.search('MoreView.init\([0-9]+, (\[.*\])\);(.*)MoreView.setPageCount', body, re.S)
            episodeListJson = self._dict2json(self._json2dict(m.group(1)))
            return episodeListJson
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화나 TV쇼 ID를 Kodi에 전달할 때, 메타정보 소스를 구분할 수 있도록 변환
    def __convertEntityId(self, daumEntityDict):
        try:
            entityId = ''
            if 'movieId' in daumEntityDict:
                entityId = '{0}{1}'.format(self.movieIdPrefix, daumEntityDict['movieId'])
            elif 'tvProgramId' in daumEntityDict:
                entityId = '{0}{1}'.format(self.showIdPrefix, daumEntityDict['tvProgramId'])
            elif 'programId' in daumEntityDict:
                entityId = '{0}{1}'.format(self.showIdPrefix, daumEntityDict['programId'])
            else:
                entityId = '{0}{1}'.format(self.showIdPrefix, daumEntityDict)
            return entityId
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
        

    # 날짜를 Kodi 형식으로 변환
    def __convertDate(self, daumDate):
        try:
            if len(daumDate) == 8:
                return '{0}-{1}-{2}'.format(daumDate[0:4], daumDate[4:6], daumDate[6:8])
            return '' 
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    # 장르 목록을 Kodi 형식으로 변환
    def __convertGenres(self, daumGenresDict):
        try:
            kodiGenreList = []
            if ('codeName' in daumGenresDict):
                kodiGenreList.append(daumGenresDict['codeName'])
            else:
                for daumGenre in daumGenresDict:
                    kodiGenreList.append(daumGenre['genreName'])
            return kodiGenreList

        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    def __convertList(self, kodiListDict, daumListJson, year, lang):
        try:
            kodiEntityDictTemplate = self._json2dict(self.kodiEntityJson)
            
            daumListDict =self._json2dict(daumListJson)
            for daumDataDict in daumListDict['data']:
                country = daumDataDict['countries'][0]['countryKo']
                if (country == '한국') or (country == '대한민국'):
                    # 국내 영화는 한글제목
                    title = self._tag_strip(daumDataDict['titleKo'])
                    lang = 'ko'
                elif (lang == 'en'):
                    # 영문 메타정보를 요청하였고 외국영화인 경우, 영문 제목
                    title = self._tag_strip(daumDataDict['titleEn'])
                else:
                    # 한글 메타정보를 요청한 경우, 한글 제목
                    title = self._tag_strip(daumDataDict['titleKo'])
                    
                releaseYear = str(daumDataDict['prodYear'])
                
                # 요청항목에 연도가 있다면, 같은 연도 영화만 검색
                if (len(year) == 4) and (year != releaseYear):
                    continue
                
                # 제목이 비어있으면 skip
                if (title is None or title == ''):
                    continue
                
                kodiEntityDict = copy.deepcopy(kodiEntityDictTemplate)
                kodiEntityDict['entity']['title'] = '[Daum] {0}'.format(title) 
                kodiEntityDict['entity']['year'] = releaseYear
                kodiEntityDict['entity']['language'] = lang
                kodiEntityDict['entity']['id'] = self.__convertEntityId(daumDataDict)
                kodiListDict['results'].append(kodiEntityDict)
            
            return kodiListDict
        
        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
    
            
    def __convertMovie(self, kodiDetailDict, daumMovieJson, lang):
        try:
            self._log_dbg(daumMovieJson)
            daumMovieDict = self._json2dict(daumMovieJson)
            daumDataDict = daumMovieDict['data']
            
            country = daumDataDict['countries'][0]['countryKo']
            originalTitle = kodiDetailDict['originaltitle']
            if (country == '한국') or (country == '대한민국'):
                # 국내 영화는 한글제목
                title = daumDataDict['titleKo']
                originalTitle = daumDataDict['titleKo']
            elif (lang == 'en'):
                # 영문 메타정보를 요청하였고 외국영화인 경우, 영문 제목
                title = daumDataDict['titleEn']
                originalTitle = daumDataDict['titleEn']
            else:
                # 한글 메타정보를 요청한 경우, 한글 제목
                title = daumDataDict['titleKo']
                originalTitle = daumDataDict['titleEn']
            
            releaseDate = kodiDetailDict['premiered']
            if ('releaseDate' in daumDataDict) and len(str(daumDataDict['releaseDate']))==8:
                releaseDate = self.__convertDate(daumDataDict['releaseDate'])
            elif ('startDate' in daumDataDict) and len(str(daumDataDict['startDate']))==8:
                releaseDate = self.__convertDate(daumDataDict['startDate'])
            
            runtime = kodiDetailDict['runtime']
            if ('showtime' in daumDataDict):
                runtime = str(daumDataDict['showtime'])
                
            rating = kodiDetailDict['rating']
            votes = kodiDetailDict['votes']
            mpaa = kodiDetailDict['mpaa']
            if ('moviePoint' in daumDataDict) and (daumDataDict['moviePoint'] is not None):
                rating = str(daumDataDict['moviePoint']['inspectPointAvg'])
                votes = str(daumDataDict['moviePoint']['inspectPointCnt'])
                mpaa = daumDataDict['admissionDesc']
            elif ('tvProgramPoint' in daumDataDict) and (daumDataDict['tvProgramPoint'] is not None):
                rating = str(daumDataDict['tvProgramPoint']['pointAvg'])
                votes = str(daumDataDict['tvProgramPoint']['pointCnt'])
                mpaa = '{0}세 이상'.format(daumDataDict['admissionCode'])

            plot = kodiDetailDict['plot']
            if ('plot' in daumDataDict) and (len(daumDataDict['plot']) > 0):
                plot = self._plot_escape(daumDataDict['plot'])
                #plot = self.__html_escape(plot)
            elif ('introduce' in daumDataDict) and (len(daumDataDict['introduce']) > 0):
                plot = self._plot_escape(daumDataDict['introduce'])
            
            posterImage = ''
            if ('photo' in daumDataDict) and (daumDataDict['photo'] is not None):
                posterImage = daumDataDict['photo']['fullname']
            
            genres = []
            if ('genres' in daumDataDict) and (daumDataDict['genres'] is not None):
                genres = self.__convertGenres(daumDataDict['genres'])
            elif ('categoryHigh' in daumDataDict) and (daumDataDict['categoryHigh'] is not None):
                genres = self.__convertGenres(daumDataDict['categoryHigh'])

            studio = ''
            if ('channel' in daumDataDict) and (daumDataDict['channel'] is not None):
                studio = daumDataDict['channel']['titleKo']

            kodiDetailDict['id'] = self.__convertEntityId(daumDataDict)
            kodiDetailDict['title'] = title
            kodiDetailDict['originaltitle'] = originalTitle
            kodiDetailDict['year'] = str(daumDataDict['prodYear'])
            kodiDetailDict['premiered'] = releaseDate
            kodiDetailDict['runtime'] = runtime
            kodiDetailDict['rating'] = rating
            kodiDetailDict['votes'] = votes
            kodiDetailDict['mpaa'] = mpaa
            kodiDetailDict['tagline'] = ''
            kodiDetailDict['outline'] = ''
            kodiDetailDict['plot'] = plot
            if len(posterImage) > 0:
                kodiDetailDict['thumb'].append(posterImage)
            kodiDetailDict['genre'] = genres
            kodiDetailDict['country'].append(country)
            kodiDetailDict['studio'].append(studio)
            
            return kodiDetailDict
        
        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            
            
    def __convertCredits(self, kodiDetailDict, daumCreditsJson):
        try:
            daumCreditsDict = self._json2dict(daumCreditsJson)
            if 'data' in daumCreditsDict:
                actorDictTemplate = self._json2dict(self.kodiActorJson)
                for crewDict in daumCreditsDict['data']:
                    castName = crewDict['castcrew']['castcrewCastName']
                    
                    if (castName == '감독') or (castName == '연출'):
                        kodiDetailDict['director'].append(crewDict['nameKo'])
                        
                    elif (castName == '극본') or (castName == '각본'):
                        kodiDetailDict['credits'].append(crewDict['nameKo'])
                        
                    elif (castName == '주연') or (castName == '출연'):
                        actorImage = crewDict['photo']['fullname']
                        if actorImage is None:
                            actorImage = ''
                        elif actorImage.startswith('/'):
                            actorImage = '{0}{1}'.format(self.baseImageURL, actorImage)
                        
                        actorDict = copy.deepcopy(actorDictTemplate)
                        actorDict['name'] = crewDict['nameKo']
                        actorDict['role'] = crewDict['castcrew']['castcrewTitleKo']
                        actorDict['thumb'] = actorImage
                        kodiDetailDict['actor'].append(actorDict)
                
            return kodiDetailDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
            

    def __convertImages(self, kodiDetailDict, daumImagesJson):
        try:
            fanartDictTemplate = self._json2dict(self.kodiFanartJson)
            daumImagesDict = self._json2dict(daumImagesJson)
            
            i = 0
            j = 0
            for imageDict in daumImagesDict['data']:
                if imageDict['photoCategory'] == '1':
                    # 포스터
                    if (i > 10):
                        continue
                    kodiDetailDict['thumb'].append(imageDict['fullname'])
                    i = i + 1 
                    
                elif imageDict['photoCategory'] == '2':
                    # 팬아트 
                    if (j > 10):
                        continue
                    fanartDict = copy.deepcopy(fanartDictTemplate)
                    fanartDict['thumb'] = imageDict['fullname']
                    kodiDetailDict['fanart'].append(fanartDict)
                    j = j + 1
                
            return kodiDetailDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))

            
    def __convertTvShow(self, kodiDetailDict, daumTvShowHtml, showId):
        try:
            daumTitle = self._regex_find('<strong class="tit_movie">(.*?)</strong>', daumTvShowHtml)
            title = re.sub(' 시즌 [0-9]*', '', daumTitle)
            self._log_dbg('title={0}'.format(title))
            rating = self._regex_find('<em class="emph_grade">(.*?)</em>', daumTvShowHtml)
            self._log_dbg('rating={0}'.format(rating))
            thumb = self._regex_find('<img src="(.*?)" class="img_summary"', daumTvShowHtml)
            self._log_dbg('thumb={0}'.format(thumb))
            studio = self._regex_find('<em class="emph_g">(.*?)</em>', daumTvShowHtml)
            self._log_dbg('studio={0}'.format(studio))
            genre = self._regex_find('>장르</dt><dd class="f_l">(.*?)</dd>', daumTvShowHtml)
            self._log_dbg('genre={0}'.format(genre))
            country = self._regex_find('>국가</dt>\s*?<dd>\s*?<span[^>]*></span>(.*?)\s*</dd>', daumTvShowHtml, re.S)
            self._log_dbg('country={0}'.format(country))
            premiered = re.sub('\.', '-', self._regex_find('>현재</dt>\s*?<dd>\s*([^~]*)~.*?<em class="emph_g">', daumTvShowHtml, re.S))
            self._log_dbg('premiered={0}'.format(premiered))
            year = ''
            if len(premiered) == 10:
                year = premiered[0:4]
            self._log_dbg('year={0}'.format(year))
            director = self._regex_find('>([^<]*?)</a> \(연출\)', daumTvShowHtml)
            self._log_dbg('director={0}'.format(director))
            credits = self._regex_find('>([^<]*?)</a> \(극본\)', daumTvShowHtml)
            self._log_dbg('credits={0}'.format(credits))
            plot = self._plot_escape(self._regex_find('<p class="desc_movie">(.*?)</p>', daumTvShowHtml))
            plot = self._tag_strip(plot)
            self._log_dbg('plot={0}'.format(plot))
            votes = re.sub(',', '', self._regex_find('평점 준 사람 수</span>([0-9,]*)\)</span>', daumTvShowHtml))
            self._log_dbg('votes={0}'.format(votes))
            
            if (country == '한국') or (country == '대한민국'):
                lang = 'ko'
            else:
                lang = 'en'
            
            kodiDetailDict['id'] = self.__convertEntityId(showId)
            kodiDetailDict['title'] = title
            kodiDetailDict['year'] = year
            kodiDetailDict['premiered'] = premiered
            kodiDetailDict['language'] = lang
            kodiDetailDict['rating'] = rating
            kodiDetailDict['votes'] = votes
            kodiDetailDict['plot'] = plot
            kodiDetailDict['thumb'].append(thumb)
            kodiDetailDict['genre'].append(genre)
            kodiDetailDict['country'].append(country)
            kodiDetailDict['studio'].append(studio)
            kodiDetailDict['director'].append(director)
            kodiDetailDict['credits'].append(credits)
            kodiDetailDict['daumTitle'] = daumTitle
            
            return kodiDetailDict

        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
    
        
    def __convertTvShowCredits(self, kodiDetailDict, daumCreditsHtml, showId):
        try:
            kodiActorDictTemplate = self._json2dict(self.kodiActorJson)
            
            actorMatches = self._regex_findall('<div class="area_character" (.*?)</div>', daumCreditsHtml, re.S)
            i = 0
            for actorHtml in actorMatches:
                actorName = self._regex_find('alt="(.*?)"', actorHtml)
                self._log_dbg('actorName={0}'.format(actorName))
                actorRole = self._regex_find('txt_join">(.*?)<', actorHtml)
                self._log_dbg('actorRole={0}'.format(actorRole))
                actorThumb = self._regex_find('"(http://.*?)"', actorHtml)
                self._log_dbg('actorThumb={0}'.format(actorThumb))
                
                actorDict = copy.deepcopy(kodiActorDictTemplate)
                actorDict['name'] = actorName
                actorDict['role'] = actorRole
                actorDict['thumb'] = actorThumb
                kodiDetailDict['actor'].append(actorDict)
                
                i = i + 1
                if (i >= 10):
                    break 
            
            return kodiDetailDict

        except Exception as e:
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))
    
        
    def __convertTvShowEpList(self, kodiEpListDict, daumEpisodesJson, showId, sno, lang):
        try:
            epDictTemplate = self._json2dict(self.kodiEpJson)
            
            daumEpisodesDict = self._json2dict(daumEpisodesJson)
            i = 0
            for daumEpDict in daumEpisodesDict:
                title = daumEpDict['title']
                if (len(title) == 0):
                    title = self._title_format(daumEpDict['name'], lang)
                    
                epDict = copy.deepcopy(epDictTemplate)
                epDict['episode']['id'] = self.__convertEntityId(daumEpDict['programId'])
                epDict['episode']['season'] = str(sno)
                epDict['episode']['epnum'] = str(daumEpDict['sequence'])
                epDict['episode']['title'] = title
                epDict['episode']['aired'] = self.__convertDate(daumEpDict['channels'][0]['broadcastDate'])
                epDict['episode']['url'] = ''   # addon에서 생성
                kodiEpListDict['episodeguide'].append(epDict)
                i = i + 1
            
            if (i > 0):
                return kodiEpListDict
            
            # TV 회차 정보가 없으면, 가짜 회차 목록 생성하여 리턴
            for i in range(1, 100):
                epDict = copy.deepcopy(epDictTemplate)
                epDict['episode']['id'] = self.__convertEntityId(showId)
                epDict['episode']['season'] = str(sno)
                epDict['episode']['epnum'] = str(i)
                epDict['episode']['title'] = self._title_format(i, lang)
                epDict['episode']['aired'] = ''
                epDict['episode']['url'] = ''   # addon에서 생성
                kodiEpListDict['episodeguide'].append(epDict)
                
            return kodiEpListDict
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))

    
    def __convertTvShowEpisode(self, kodiEpDetailDict, daumEpisodesJson, showId, sno, eno):
        try:
            # Daum TV 회차 목록에서 요청한 회차정보 검색 
            daumEpisodesDict = self._json2dict(daumEpisodesJson)
            for daumEpDict in daumEpisodesDict:
                if (str(daumEpDict['sequence']) == eno):
                    showId = self.__convertEntityId(daumEpDict)
                    
                    title = daumEpDict['title']
                    if (len(title) == 0):
                        title = '제 {0}화'.format(daumEpDict['name'])
                    
                    detailsDict = kodiEpDetailDict['details']
                    detailsDict['id'] = showId
                    detailsDict['season'] = str(sno)
                    detailsDict['episode'] = str(eno)
                    detailsDict['title'] = title
                    detailsDict['aired'] = self.__convertDate(daumEpDict['channels'][0]['broadcastDate'])
                    detailsDict['uniqueid'] = '{0}_{1}_{2}'.format(showId, sno, eno)
                    detailsDict['displayseason'] = str(sno)
                    detailsDict['displayepisode'] = str(eno)
                    detailsDict['displayafterseason'] = ''
                    #detailsDict['runtime'] = '60'
                    #detailsDict['rating'] = '7.1'
                    #detailsDict['votes'] = '52'
                    detailsDict['plot'] = self._plot_escape(daumEpDict['introduceDescription'])
                    #detailsDict['thumb'].append('https://image.tmdb.org/t/p/w300/wrGWeW4WKxnaeA8sxJb2T9O6ryo.jpg')
                    #detailsDict['director'].append('Tim Van Patten')
                    #detailsDict['credits'].append('David Benioff')
                    
                    return kodiEpDetailDict
            
            #  Daum TV 회차정보가 없으면, 가짜 회차정보 생성하여 리턴  
            detailsDict = kodiEpDetailDict['details']
            detailsDict['id'] = self.__convertEntityId(showId)
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
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))

    
    # 영화 검색
    def findMovies4Kodi(self, query, year, lang):
        try:
            kodiListDict = self._json2dict(self.kodiListJson)
            self._log_dbg('{0}.{1}: query={2}, year={3}, lang={4}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, query, year, lang))
            if re.search('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', query):
                # 한글은 공백을 제거하면 더 잘 찾음
                query = re.sub('[ ]*','', query)
            year = str(year)
            
            daumListJson = self.__findMovies(query)
            self._log_dbg(daumListJson)
            kodiListDict = self.__convertList(kodiListDict, daumListJson, year, lang)
            kodiListJson = self._dict2json(kodiListDict)
            self._log_dbg(kodiListJson)
            return kodiListJson
        
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


    # 영화 상세정보 조회
    def getMovieDetail4Kodi(self, movieId, lang):
        try:
            kodiMovieDict = self._json2dict(self.kodiDetailJson)
            self._log_dbg('{0}.{1}: movieId={2}, lang={3}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, movieId, lang))
            movieId = self.__revertEntityId(movieId)
            
            # 영화 정보 변환
            daumMovieJson = self.__getMovie(movieId)
            self._log_dbg(daumMovieJson)
            if daumMovieJson:
                kodiMovieDict['details'] = self.__convertMovie(kodiMovieDict['details'], daumMovieJson, lang)
                self._log_dbg(kodiMovieDict)
            
            # Credit 정보 변환
            daumCreditsJson = self.__getMovieCredits(movieId)
            self._log_dbg(daumCreditsJson)
            if daumCreditsJson:
                kodiMovieDict['details'] = self.__convertCredits(kodiMovieDict['details'], daumCreditsJson)
                self._log_dbg(kodiMovieDict)
             
            # 이미지 정보 변환 
            daumImagesJson = self.__getMovieImages(movieId)
            self._log_dbg(daumImagesJson)
            if daumImagesJson:
                kodiMovieDict['details'] = self.__convertImages(kodiMovieDict['details'], daumImagesJson)
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
            if re.search('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', query):
                # 한글은 공백을 제거하면 더 잘 찾음
                query = re.sub('[ ]*','', query)
            year = str(year)
            
            daumListJson = self.__findTvShows(query)
            self._log_dbg(daumListJson)
            kodiListDict = self.__convertList(kodiListDict, daumListJson, year, lang)
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
            
            # 영화 정보 변환
            daumTvShowHtml = self.__getTvShowHtml(showId)
            #self._log_dbg('len(daumTvShowHtml)={0}', len(daumTvShowHtml))
            kodiDetailDict['details'] = self.__convertTvShow(kodiDetailDict['details'], daumTvShowHtml, showId)
            self._log_dbg(kodiDetailDict)

            # 영문으로 검색했다면, 제목만 영문으로 변환
            if (lang == 'en') and (kodiDetailDict['details']['country'][0] != '대한민국'):
                daumTitle = kodiDetailDict['details']['daumTitle']
                daumListJson = self.__findTvShows(daumTitle)
                daumListDict = self._json2dict(daumListJson)
                for daumDataDict in daumListDict['data']:
                    if (daumDataDict['titleKo'] == daumTitle):
                        kodiDetailDict['details']['title'] = daumDataDict['titleEn'] 
                        break
            
            # Credit 정보 변환
            daumCreditsHtml = self.__getTvShowCreditsHtml(showId)
            #self._log_dbg('len(daumCreditsHtml)={0}', len(daumCreditsHtml))
            kodiDetailDict['details'] = self.__convertTvShowCredits(kodiDetailDict['details'], daumCreditsHtml, showId)
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

            daumEpisodesHtml = self.__getTvShowEpisodesHtml(showId)
            title = self._regex_find('class="link_rel #title">(.*?)</a>', daumEpisodesHtml)
            self._log_dbg(title)
            season = self._regex_find(' 시즌 (\d+)', title)
            self._log_dbg(season)
            if len(season) == 0:
                # 시즌이 없는 드라마는 현재 시즌 에피소드 목록만 조회
                season = '1'
                daumEpisodesJson = self.__getTvShowEpisodes(showId)
                kodiEpListDict = self.__convertTvShowEpList(kodiEpListDict, daumEpisodesJson, showId, season, lang)
            else:
                # Daum TV의 전체 시즌 에피소드 목록을 조회
                daumSeasonsJson = self.__getTvShowSeasons(showId)
                self._log_dbg(daumSeasonsJson)
                daumSeasonsDict = self._json2dict(daumSeasonsJson)
                for seasonDict in daumSeasonsDict:
                    # 시즌별로 에피소드 목록을 조회
                    self._log_dbg('seasonDict={0}'.format(seasonDict))
                    season = self._regex_find(u' 시즌 (\d+)', seasonDict['name'])
                    self._log_dbg('season={0}'.format(season))
                    daumEpisodesJson = self.__getTvShowEpisodes(seasonDict['programId'])
                    kodiEpListDict = self.__convertTvShowEpList(kodiEpListDict, daumEpisodesJson, showId, season, lang)
             
            kodiEpListJson = self._dict2json(kodiEpListDict)
            self._log_dbg(kodiEpListJson)
            return kodiEpListJson

        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))

            
    # 에피소드 상세정보 조회
    def getTvShowEpisode4Kodi(self, showId, sno, eno, lang):
        try:
            kodiEpDetailDict = self._json2dict(self.kodiEpDetailJson)
            self._log_dbg('{0}.{1}: showId={2}, sno={3}, eno={4}, lang={5}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, showId, sno, eno, lang))
            showId = self.__revertEntityId(showId)
            sno = str(sno)
            eno = str(eno)
            
            # 요청 시즌과 일치하는 시즌의 에피소드 정보를 조회
            daumEpisodesJson = self.__getTvShowEpisodes(showId)
            self._log_dbg(daumEpisodesJson)
            kodiEpDetailDict = self.__convertTvShowEpisode(kodiEpDetailDict, daumEpisodesJson, showId, sno, eno)
            kodiEpDetailJson = self._dict2json(kodiEpDetailDict)
            self._log_dbg(kodiEpDetailJson)
            return kodiEpDetailJson
            
        except Exception as e: 
            self._log_err('{0}.{1}: {2}'.format(self.__class__.__name__, sys._getframe().f_code.co_name, str(e)))


if __name__ == '__main__':
    try:
        # 기본 인코딩을 UTF-8로 설정
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # Logger 초기화
        SVC_NAME = 'DAUM'
        #LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(module)s:%(funcName)s][%(levelname)s] %(message)s'
        LOG_FORMAT = '[%(asctime)-15s][%(name)s][%(levelname)s] %(message)s'
        #logFile = '{0}_{1}.log'.format(SVC_NAME, time.strftime('%Y%m%d')) 
        #logging.basicConfig(filename=logFile, format=LOG_FORMAT, level=logging.DEBUG)
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
        logger = logging.getLogger(SVC_NAME)
        logger.info('==[STARTED]======================================')
    
#         # 영화 검색
#         query = '매트릭스 리로디드'
#         year = ''
#         lang = 'en'
#         scraper = DaumScraper(SVC_NAME)
#         listJson = scraper.findMovies4Kodi(query, year, lang)
#         logger.debug('')
#           
#         listDict = json.loads(listJson, object_pairs_hook=OrderedDict)
#         logger.debug(listDict)
#         for resultDict in listDict['results']:
#             # 검색결과에서 영화ID 추출
#             movieId = resultDict['entity']['id']
#             logger.debug('movieId={0}'.format(movieId))
#             title = resultDict['entity']['title']
#             logger.debug('title={0}'.format(title))
#                
#             # 상세정보 조회
#             detailJson = scraper.getMovieDetail4Kodi(movieId, lang)
#             logger.debug('')
            
        # TV쇼 검색
        #query = '태양의 후예'
        #query = '피리부는 사나이'
        #query = '프렌즈 시즌 8'
        query = 'Breaking Bad'
        year = ''
        lang = 'en'
        tvscraper = DaumScraper(SVC_NAME)
        listJson = tvscraper.findTvShows4Kodi(query, year, lang)
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
            detailJson = tvscraper.getTvShowDetail4Kodi(showId, lang)
            logger.debug('')
         
#             # 에피소드 조회
#             detailJson = tvscraper.getTvShowEpList4Kodi(showId, lang)
#             logger.debug('')
#             
#             # 에피소드 상세정보 조회
#             detailJson = tvscraper.getTvShowEpisode4Kodi(showId, '1', '2', lang)
#             logger.debug('')
        
            break
    
    except Exception as e:
        logger.error(str(e))
