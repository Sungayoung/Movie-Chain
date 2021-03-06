import requests
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
from .serializers.Actor import ActorSerializer, ActorProfileSerializer
from .serializers.Comment import CommentSerializer
from .serializers.Crew import CrewSerializer, CrewProfileSerializer
from .serializers.Movie import MovieListSerializer, MovieSerializer
from .serializers.Review import ReviewSerializer
from .serializers.Genre import GenreSerializer
from .serializers.Hashtag import HashtagSerializer
import random

# Create your views here.
# 페이지별 영화목록
@api_view(['GET'])
def get_movie_list_page(request):

    # 정렬 기준 설정, 기본값 : id 큰 순서
    order = request.GET.get('order_by') if request.GET.get('order_by') else 'order'

    # 기준 별로 movies_list를 뽑음.
    filter_by = request.GET.get('filter_by')
    filter_id = request.GET.get('filter_id')
   

    # page 가져옴
    page = request.GET.get('page')

    # page별 영화 개수 지정, 기본값: 36개
    movie_cnt = request.GET.get('movie_cnt') if request.GET.get('movie_cnt') else 36

    # http://127.0.0.1:8000/movies/?filter_by='actor'&filter_id=9195&order_by=-title
    if not filter_by:
        return Response({'error' : 'filter_by가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)

    if filter_by == 'all':
        movies = get_list_or_404(Movie.objects.order_by(order))
    else:
        if not filter_id:
            return Response({'error': 'filter_id가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
        filter_id_list = filter_id.split(',')
        if filter_by == 'actor':
            movies = get_list_or_404(Movie.objects.filter(actors__in=filter_id_list).order_by(order).distinct())

        elif filter_by == 'crew':
            movies = get_list_or_404(Movie.objects.filter(crews__in=filter_id_list).order_by(order).distinct())
        
        elif filter_by == 'keyword':
            movies = get_list_or_404(Movie.objects.filter(keyword__in=filter_id_list).order_by(order).distinct())
        
        elif filter_by == 'genre':
            movies = get_list_or_404(Movie.objects.filter(genre__in=filter_id_list).order_by(order).distinct())
        
        else:
            return Response({'error' : 'filter_by 값이 올바르지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)

    paginator = Paginator(movies, movie_cnt)
    movie_list = paginator.get_page(page)  
    total_page_cnt = paginator.num_pages + 1
    if request.user.is_authenticated:
        serializer = MovieListSerializer(movie_list, many=True, context={'user': request.user})
    else:
        serializer = MovieListSerializer(movie_list, many=True)
    res = {'serialized_data':serializer.data, 'total_page_cnt':total_page_cnt}
    return Response(res, status=status.HTTP_200_OK)

# 영화 목록 요청
@api_view(['GET'])
@permission_classes([AllowAny])
def get_movie_list(request):

    # 정렬 기준 설정, 기본값 : id 큰 순서
    order = request.GET.get('order_by') if request.GET.get('order_by') else 'order'

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
            crew = get_object_or_404(Crew, id=filter_id)
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


# 영화 추천 알고리즘
@api_view(['GET'])
def get_recommend_movie(request):
    me = request.user
    personal_movies = me.personal_movies.all()
    genres = {}
    keywords = {}
    user_movie_list = Movie.objects.none()
    for genre in me.like_genres.all():
        if genres.get(genre.id):
            genres[genre.id] += 1
        else:
            genres[genre.id] = 2
    
    for movie in personal_movies:
        users = movie.personal_movie_users.exclude(id=me.id)
        # 나를 상징하는 영화에서 genre, keyword 저장
        for genre in movie.genre.all():
            if genres.get(genre.id):
                genres[genre.id] += 1
            else:
                genres[genre.id] = 2
        
        for keyword in movie.keyword.all():
            if keywords.get(keyword.id):
                keywords[keyword.id] += 1
            else:
                keywords[keyword.id] = 2
        
        for user in users:
            user_movie_list |= user.favorite_movies.all()
    
    idx = 0
    movie_list = Movie.objects.none()
    # 추천하는 영화는 최대 36개
    while len(movie_list) < 36:
        criteria = 0.9
        movie = Movie.objects.filter(order=idx)
        weight = 0
        
        for keyword in movie[0].keyword.all():
            if keyword in keywords.keys():
                weight = max(weight, keywords[keyword])
        
        for genre in movie[0].genre.all():
            if genre in genres.keys():
                weight = max(weight, genres[genre])
        
        if weight > 0:
            criteria //= weight
        num = random.random()
        if num > criteria:
            movie_list |= movie
        
        idx += 1
    movie_list |= user_movie_list
    serializer = MovieListSerializer(movie_list, many=True)
    data = serializer.data
    data = random.sample(data, 36)
    random.shuffle(data)


    return Response(data, status=status.HTTP_200_OK)


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
        genres = Genre.objects.filter(name__icontains=query)
        keywords = Hashtag.objects.filter(name__icontains=query)
        for actor in actors:
            movies.union(actor.actor_movies.all())
        
        for crew in crews:
            movies.union(crew.crew_movies.all())
        data = {
            'movies': MovieListSerializer(movies, many=True).data,
            'actors': ActorSerializer(actors, many=True).data,
            'crews': CrewSerializer(crews, many=True).data,
            'genres': GenreSerializer(genres, many=True).data,
            'keywords': HashtagSerializer(keywords, many=True).data,
        }
        return data

    data = search_movie()
    
    return Response(data, status=status.HTTP_200_OK)


# 영화 상세페이지 요청
@api_view(['GET'])
def get_movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie, context={'user': request.user})
    return Response(serializer.data)

# 배우, 감독 상세페이지 요청
@api_view(['GET'])
def get_people_detail(request, people_pk):
    actor = Actor.objects.filter(id=people_pk)
    if len(actor):
        serializer = ActorProfileSerializer(actor[0], context={'user': request.user})
    else:
        crew = Crew.objects.filter(id=people_pk)
        serializer = CrewProfileSerializer(crew[0], context={'user': request.user})

    return Response(serializer.data, status=status.HTTP_200_OK)

# 출연 배우 리스트 요청
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

# 모든배우 리스트 요청
@api_view(['GET'])
def get_actor_list_all(request):
    actors = Actor.objects.all()
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)


# 모든제작진 리스트 요청
@api_view(['GET'])
def get_crew_list_all(request):
    crews = Crew.objects.all()
    serializer = CrewSerializer(crews, many=True)
    return Response(serializer.data)


# 모든장르 리스트 요청
@api_view(['GET'])    
def get_genre_list_all(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

# 모든키워드 리스트 요청
@api_view(['GET'])
def get_hashtag_list_all(request):
    hashtags = Hashtag.objects.all()
    serializer = HashtagSerializer(hashtags, many=True)
    return Response(serializer.data)



# 해당 영화의 리뷰 조회와 새로운 리뷰 생성 요청
@api_view(['GET', 'POST'])
def get_or_create_review(request, movie_pk):
    if request.method == 'GET':  # 해당영화 리뷰 조회
        my_review = Review.objects.filter(movie=movie_pk, user=request.user, content__isnull=False)
        my_rank = Review.objects.filter(movie=movie_pk, user=request.user, rank__isnull=False)
        reviews = Review.objects.filter(movie=movie_pk, content__isnull=False).exclude(user=request.user)
        serializer_my_rank = ReviewSerializer(my_rank, many=True, context={'user': request.user})
        serializer_my_review = ReviewSerializer(my_review, many=True, context={'user': request.user})
        serializer_review = ReviewSerializer(reviews, many=True, context={'user': request.user})
        data = {
            'myRank': serializer_my_rank.data,
            'reviewCnt': len(serializer_my_review.data) + len(serializer_review.data),
            'myReview': serializer_my_review.data,
            'reviews': serializer_review.data,
        }
        return Response(data)

    elif request.method == 'POST':  # 새로운 리뷰 생성
        movie = get_object_or_404(Movie, pk=movie_pk)
        
        # 이미 있으면 해당리뷰 수정
        if Review.objects.filter(movie=movie, user=request.user).exists():
            review = get_object_or_404(Review, movie=movie_pk, user=request.user)
            serializer = ReviewSerializer(instance=review, data=request.data, context={'user': request.user})
        else:
            serializer = ReviewSerializer(data=request.data, context={'user': request.user})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# 리뷰 수정&삭제 / 댓글 조회&작성
@api_view(['PUT', 'DELETE', 'GET', 'POST'])
def update_or_delete_review_or_get_or_create_comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':   # 리뷰 수정
        serializer = ReviewSerializer(instance=review, data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':  # 리뷰 삭제
        review.delete()
        return Response(data=f'{review_pk}번 리뷰 삭제', status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET':  # 댓글 조회
        comments = Comment.objects.filter(review=review)
        serializer = CommentSerializer(comments, many=True, context={'user': request.user})
        return Response(serializer.data)

    elif request.method == 'POST':    # 새로운 댓글 작성
        serializer = CommentSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save(review=review, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 댓글 수정 및 삭제
@api_view(['PUT', 'DELETE'])
def update_or_delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(data=f'{comment_pk}번 댓글 삭제', status=status.HTTP_204_NO_CONTENT)

# 영화 좋아요
@api_view(['POST'])
def like_movie(request):
    movie_id = request.data.get('movieId')
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.favorite_movies.filter(id=movie_id).exists():
        request.user.favorite_movies.remove(movie)
    else:
        request.user.favorite_movies.add(movie)
    serializer = MovieSerializer(movie, context={'user': request.user})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 저장
@api_view(['POST'])
def bookmark_movie(request):
    movie_id = request.data.get('movieId')
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.bookmark_movies.filter(id=movie_id).exists():
        request.user.bookmark_movies.remove(movie)
    else:
        request.user.bookmark_movies.add(movie)
    serializer = MovieSerializer(movie, context={'user': request.user})
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# 리뷰 좋아요
@api_view(['POST'])
def like_review(request):
    review_id = request.data.get('reviewId')
    review = get_object_or_404(Review, id=review_id)
    if request.user.like_reviews.filter(id=review_id).exists():
        request.user.like_reviews.remove(review)
        isLiked = False
    else:
        request.user.like_reviews.add(review)
        isLiked = True
    serializer = ReviewSerializer(review, context={'user': request.user})
    serializer.data['isLiked'] = isLiked
    print(type(serializer.data))
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
                'language': 'ko-KR',
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
            'language': 'ko-KR',
        }
        res = requests.get(url, params=params).json().get('results')
        return res

    def save_credit_info(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/credits'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko-KR'
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
            'language': 'ko-KR'
        }
        res = requests.get(url, params=params)
        return res.json().get('genres')

    def get_video(self, movie_id):
        url = f'{self.BASE_URL}/movie/{movie_id}/videos'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko-KR',
        }
        res = requests.get(url, params=params).json()
        for video in res['results']:
            if video['site'] == 'YouTube':
                return video['key']
    
    def get_people_detail(self, people_id):
        url = f'{self.BASE_URL}/person/{people_id}'
        params = {
            'api_key': self.API_KEY,
            'language': 'ko-KR',
        }
        res = requests.get(url, params=params)
        return res.json()


def index(request):
    _movie = GetMovie()
    movie_list = _movie.save_movie_info(100)
    save_movie(movie_list, 'init')


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
    for (idx, movie) in enumerate(movie_list):
        movie_id = movie['id']
        print(movie_id)
        release_date = movie.get('release_date')
        if not release_date:
            release_date = '1111-11-11'
        m = Movie(
            id = movie_id,
            order = idx,
            title = movie['title'],
            overview = movie['overview'],
            release_date = release_date,
            vote_count = movie['vote_count'],
            vote_average = movie['vote_average'],
            poster_path = movie['poster_path'],
            backdrop_path = movie['backdrop_path'],
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
            cast_detail = _movie.get_people_detail(cast_id)
            # 만약 Actor 테이블에 없다면 추가해줌
            if not Actor.objects.filter(id=cast_id).exists():
                a = Actor(
                    id = cast['id'],
                    name = cast['name'],
                    profile_path = cast['profile_path'],
                    birthday = cast_detail['birthday'],
                    deathday = cast_detail['deathday'],
                    homepage = cast_detail['homepage']
                )
                a.save()
            character = CharacterName(movie=m, actor=Actor.objects.get(id=cast_id), character=cast['character'])
            character.save()

        for crew in credit.get('crew'):
            if crew['job'] == 'Director':
                crew_id = crew['id']
                crew_detail = _movie.get_people_detail(crew_id)
                # 만약 Crew 테이블에 없다면 추가해줌
                if not Crew.objects.filter(id=crew_id).exists():
                    c = Crew(
                        id = crew['id'],
                        name = crew['name'],
                        job = crew['job'],
                        profile_path = crew['profile_path'],
                        birthday = crew_detail['birthday'],
                        deathday = crew_detail['deathday'],
                        homepage = crew_detail['homepage'],
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
