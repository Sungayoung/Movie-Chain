from django.shortcuts import render
import requests
from django.conf import settings
from .models import Actor, Genre, Crew, Hashtag, Movie
# Create your views here.




class GetMovie:

    def __init__(self, page_num):
        self.page_num = page_num
        self.API_KEY = "0d315ea0ddddb2ff36619e88cd6f335b"
        self.BASE_URL = 'https://api.themoviedb.org/3'

    def save_movie_info(self):
        url = f'{self.BASE_URL}/movie/popular'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko',
            'page': self.page_num
        }
        res = requests.get(url, params=params).json()
        return res

    def save_credit_info(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/credits'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko'
        }
        pass

    def save_keyword_info(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/keywords'
        params = {
            'api_key': self.API_KEY,
        }

    def save_genre_info(self, movie_id):
        url = f'{self.BASE_URL}/genre/movie/list'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko'
        }

    def get_video(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/videos'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko',
        }