from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from serializers.Actor import ActorSerializer
from serializers.Comment import CommentSerializer
from serializers.Crew import CrewSerializer
from serializers.Movie import MovieListSerializer, MovieSerializer
from serializers.Review import ReviewSerializer

# Create your views here.

# 영화 목록 요청
@api_view(['GET'])
def get_movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# 영화 상세페이지 요청
@api_view(['GET'])
def get_movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer)


# 배우 리스트 요청
@api_view(['GET'])
def get_actor_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)   # 영화 객체에서 배우 id추출 후
    actor = Actor.objects.filter(pk__in=movie.actors)   # 배우 목록에서 필터링
    serializer = ActorSerializer(actor, many=True)
    return Response(serializer)


# 제작진 리스트 요청
@api_view(['GET'])
def get_crew_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)   # 위와 동일
    crew = Actor.objects.filter(pk__in=movie.crews)
    serializer = ActorSerializer(crew, many=True)
    return Response(serializer)



