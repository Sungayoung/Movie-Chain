import requests
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
    
    # 영화 검색 함수
    def search_movie():
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
        return data

    data = search_movie()

    # 검색결과가 없다면 TMDB에서 검색 진행 및 DB 저장 후 재 검색
    if not (data.get('movies') or data.get('actors') or data.get('crews')):
        _movie = GetMovie()
        movie_list = _movie.save_search_result(query)
        save_movie(movie_list, 'search')
        data = search_movie()
    
    
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



# 아래는 TMDB 에서 영화를 불러오기 위한 함수
class GetMovie:

    def __init__(self):

        self.API_KEY = settings.TMDB_API_KEY
        self.BASE_URL = 'https://api.themoviedb.org/3'

    def save_movie_info(self, page_num):
        result = []
        url = f'{self.BASE_URL}/movie/popular'
        for i in range(1, page_num+1):
            params = {
                'api_key': self.API_KEY,
                'language': 'ko',
                'page': i
            }
            res = requests.get(url, params=params).json().get('results')
            result.extend(res)
        
        return result

    def save_search_result(self, query):
        url = f'{self.BASE_URL}/search/movie'
        params = {
            'api_key': self.API_KEY,
            'query': query,
            'language': 'ko',
        }
        res = requests.get(url, params=params).json().get('results')
        return res

    def save_credit_info(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/credits'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko'
        }
        res = requests.get(url, params=params)
        return res.json()


    def save_keyword_info(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/keywords'
        params = {
            'api_key': self.API_KEY,
        }
        res = requests.get(url, params=params)
        return res.json().get('keywords')

    def save_genre_info(self):
        url = f'{self.BASE_URL}/genre/movie/list'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko'
        }
        res = requests.get(url, params=params)
        return res.json().get('genres')

    def get_video(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/videos'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko',
        }
        res = requests.get(url, params=params).json()
        for video in res['results']:
            if video['site'] == 'YouTube':
                return video['key']

def save_movie(info_list, save_type):
    _movie = GetMovie()
    if save_type == 'search':
        movie_list = []
        for movie in info_list:
            if not Movie.objects.filter(id=movie['id']).exists():
                movie_list.append(movie)
                    
    else:
        # 장르 리스트 저장
        genres = _movie.save_genre_info()
        for genre in genres:
            g = Genre(id=genre['id'], name=genre['name'])
            g.save()
        movie_list = info_list

    # 전체 영화 리스트를 돌면서 세부사항 저장
    for movie in movie_list:
        movie_id = movie['id']
        print(movie_id)
        m = Movie(
            id = movie_id,
            title = movie['title'],
            overview = movie['overview'],
            release_date = movie['release_date'],
            vote_count = movie['vote_count'],
            vote_average = movie['vote_average'],
            poster_path = movie['poster_path'],
            video_id = _movie.get_video(movie_id)
        )
        m.save()
        # 장르 리스트에서 object를 찾아 추가
        for genre_id in movie['genre_ids']:
            m.genre.add(Genre.objects.get(id=genre_id))
        

        # cast, crew 정보 받아옴
        credit = _movie.save_credit_info(movie_id)

        for cast in credit.get('cast')[:10]:
            cast_id = cast['id']

            # 만약 Actor 테이블에 없다면 추가해줌
            if not Actor.objects.filter(id=cast_id).exists():
                a = Actor(
                    id = cast['id'],
                    name = cast['name'],
                    profile_path = cast['profile_path']
                )
                a.save()
            m.actors.add(Actor.objects.get(id=cast_id))

        for crew in credit.get('crew'):
            if crew['job'] == 'Director':

                crew_id = crew['id']

                # 만약 Crew 테이블에 없다면 추가해줌
                if not Crew.objects.filter(id=crew_id).exists():
                    c = Crew(
                        id = crew['id'],
                        name = crew['name'],
                        job = crew['job'],
                        profile_path = crew['profile_path'],
                    )
                    c.save()
                m.crews.add(Crew.objects.get(id=crew_id))
                break
        
        for keyword in _movie.save_keyword_info(movie_id):
            keyword_id = keyword['id']

            # 만약 Hashtag 테이블에 없다면 추가해줌
            if not Hashtag.objects.filter(id=keyword['id']).exists():
                h = Hashtag(
                    id = keyword_id,
                    name = keyword['name']
                )
                h.save()
            m.keyword.add(Hashtag.objects.get(id=keyword_id))

        m.save()
