from rest_framework import serializers, status
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from movies.models import Movie
from .models import Chatting
from .serializers.User import SignupSerializer, UserSerializer
from movies.serializers.Movie import MovieListSerializer
from .serializers.Chatting import ChattingSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    
    # client에서 비밀번호 정보 받아옴
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    # 비밀번호 일치 확인
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 데이터 직렬화
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        for gen in request.data.get('like_genres'):
            user.like_genres.add(gen)
        for mov in request.data.get('personal_movies'):
            user.personal_movies.add(mov)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'PUT'])
def set_personal_movies(request):
    if request.method == 'POST':
        movieId = request.data.get('movieId')
        movie = get_object_or_404(Movie, id=movieId)
        request.user.personal_movies.add(movie)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        originId = request.data.get('originId')
        movieId = request.data.get('movieId')
        movie = get_object_or_404(Movie, id=movieId)
        origin_movie = request.user.personal_movies.get(id=originId)
        request.user.personal_movies.remove(origin_movie)
        request.user.personal_movies.add(movie)
        serializer = MovieListSerializer(origin_movie)
        print(origin_movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
def chatting(request):
    me = request.user
    if request.method == 'GET':
        get_messages = me.from_chatting.through.objects.filter(to_user=me)
        serializer_get_messages = ChattingSerializer(get_messages, many=True)
        send_messages = me.from_chatting.through.objects.filter(from_user=me)
        serializer_send_messages = ChattingSerializer(send_messages, many=True)
        data = {
            'getMessages': serializer_get_messages.data,
            'sendMessages': serializer_send_messages.data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        to_user_id = request.data.get('to_user')
        if not to_user_id:
            return Response({'error': '보내는 상대가 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
        
        to_user = get_object_or_404(get_user_model(), id=to_user_id)
        content = request.data.get('content')
        
        if not content:
            return Response({'error' : '내용이 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
        message = Chatting(from_user=me, to_user=to_user, content=content)
        data = message.save()
        serializer = ChattingSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        chatId = request.data.get('chatId')
        if not chatId:
            return Response({'error': 'chatId가 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
        chatting = Chatting.objects.get(id=chatId)
        chatting.delete()
        return Response({'delete': f"{chatting.id}가 삭제되었습니다"}, status=status.HTTP_201_CREATED) 


@api_view(['GET', 'POST'])
def get_or_set_profile_image(request):
    if request.method == 'GET':
        if request.GET.get('nickname'):
            serializer = UserSerializer(get_object_or_404(get_user_model(), nickname=request.GET.get('nickname')))
            serializer.data.update({'isLoginUser': request.GET.get('nickname') == request.user.nickname})
        else:
            serializer = UserSerializer(request.user)
            serializer.data.update({'isLoginUser': True})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        img = request.FILES['files']
        user = request.user
        user.profile_img = img
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)