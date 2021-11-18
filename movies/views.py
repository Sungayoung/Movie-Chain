from django.db.models.query_utils import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers.Actor import ActorSerializer
from .serializers.Comment import CommentSerializer
from .serializers.Crew import CrewSerializer
from .serializers.Movie import MovieListSerializer, MovieSerializer
from .serializers.Review import ReviewSerializer

# Create your views here.

# 영화 목록 요청
@api_view(['GET'])
def get_movie_list(request):

    # 정렬 기준 설정, 기본값 : id 큰 순서
    order = request.GET.get('order_by') if request.GET.get('order_by') else '-id'

    # 기준 별로 movies_list를 뽑음.
    filter_by = request.GET.get('filter_by')
    filter_id = request.GET.get('filter_id')


    # http://127.0.0.1:8000/movies/?filter_by='actor'&filter_id=9195&order_by=-title
    if not filter_by:
        return Response({'error' : 'filter_by가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)

    if filter_by == 'all':
        movies = get_list_or_404(Movie.objects.order_by(order))
    else:
        if not filter_id:
            return Response({'error': 'filter_id가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
        
        if filter_by == 'actor':
            actor = get_object_or_404(Actor, id=filter_id)
            movies = get_list_or_404(actor.actor_movies.all().order_by(order))
        
        elif filter_by == 'crew':
            crew = get_object_or_404(Actor, id=filter_id)
            movies = get_list_or_404(crew.crew_movies.all().order_by(order))
        
        elif filter_by == 'keyword':
            keyword = get_object_or_404(Hashtag, id=filter_id)
            movies = get_list_or_404(keyword.hashtag_movies.all().order_by(order))
        
        elif filter_by == 'genre':
            genre = get_object_or_404(Genre, id=filter_id)
            movies = get_list_or_404(genre.genre_movies.all().order_by(order))
        
        else:
            return Response({'error' : 'fiter_by 값이 올바르지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 영화 검색 기능
@api_view(['GET'])
def search(request):
    query = request.GET.get('query')
    if not query:
        return Response({'error' : 'query값이 올바르지 않습니다'})
    
    movies = Movie.objects.filter(title__icontains=query)
    actors = Actor.objects.filter(name__icontains=query)
    crews = Crew.objects.filter(name__icontains=query)
    for actor in actors:
        movies.union(actor.actor_movies.all())
    
    for crew in crews:
        movies.union(crew.crew_movies.all())

    data = {
        'movies': MovieListSerializer(movies, many=True).data,
        'actors': ActorSerializer(actors, many=True).data,
        'crews': CrewSerializer(crews, many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)


# 영화 상세페이지 요청
@api_view(['GET'])
def get_movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


# 배우 리스트 요청
@api_view(['GET'])
def get_actor_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)   # 영화 객체에서 배우 id추출 후
    actor = Actor.objects.filter(actor_movies=movie)   # 배우 목록에서 필터링
    serializer = ActorSerializer(actor, many=True)
    return Response(serializer.data)


# 제작진 리스트 요청
@api_view(['GET'])
def get_crew_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)   # 위와 동일
    crew = Crew.objects.filter(crew_movies=movie)
    serializer = CrewSerializer(crew, many=True)
    return Response(serializer.data)


# 해당 영화의 리뷰 조회와 새로운 리뷰 생성 요청
@api_view(['GET', 'POST'])
def get_or_create_review(request, movie_pk):
    if request.method == 'GET':  # 해당영화 리뷰 조회
        reviews = Review.objects.filter(movie=movie_pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':  # 새로운 리뷰 생성
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 리뷰 수정&삭제 / 댓글 조회&작성
@api_view(['PUT', 'DELETE', 'GET', 'POST'])
def update_or_delete_review_or_get_or_create_comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':   # 리뷰 수정
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':  # 리뷰 삭제
        review.delete()
        return Response(data=f'{review_pk}번 리뷰 삭제', status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':  # 댓글 조회
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':    # 새로운 댓글 작성
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 수정 및 삭제
@api_view(['PUT', 'DELETE'])
def update_or_delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(data=f'{comment_pk}번 댓글 삭제', status=status.HTTP_204_NO_CONTENT)
