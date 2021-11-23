from rest_framework import serializers, status
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from movies.models import Movie, Actor, Crew
from .models import Chatting
from .serializers.User import SignupSerializer, UserSerializer
from movies.serializers.Movie import MovieListSerializer
from movies.serializers.Actor import ActorProfileSerializer
from movies.serializers.Crew import CrewProfileSerializer
from .serializers.Chatting import ChattingSerializer



@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    
    # client에서 비밀번호 정보 받아옴
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
    valid_checked = request.data.get('valid_check')   # true/fales

    # 비밀번호 일치 확인
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 데이터 직렬화
    serializer = SignupSerializer(data=request.data)
    print(valid_checked)
    print(1)
    if serializer.is_valid(raise_exception=True):
        print(2)
        if valid_checked:     # 유효성 검사확인된 것만 db에 저장
            print(3)
            user = serializer.save()
            user.set_password(request.data.get('password'))
            for gen in request.data.get('like_genres'):
                user.like_genres.add(gen)
            for mov in request.data.get('personal_movies'):
                user.personal_movies.add(mov)
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_user(request):
    password = request.data.get('password')
    if not password:
        request.data['password'] = request.user.password
    # 데이터 직렬화
    serializer = SignupSerializer(instance=request.user, data=request.data, context={'user': request.user})

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        if password:
            user.set_password(request.data.get('password'))
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'PUT', 'GET'])
def set_personal_movies(request):

    # 같은 영화를 지정한 사람 리스트
    if request.method == 'GET':
        movieId = request.GET.get('movieId')
        movie = get_object_or_404(Movie, id=movieId)
        users = get_list_or_404(movie.personal_movie_users.all())
        serializer = UserSerializer(users, many=True, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 영화 지정
    elif request.method == 'POST':
        movieId = request.data.get('movieId')
        movie = get_object_or_404(Movie, id=movieId)
        request.user.personal_movies.add(movie)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 영화 수정
    elif request.method == 'PUT':
        originId = request.data.get('originId')
        movieId = request.data.get('movieId')
        movie = get_object_or_404(Movie, id=movieId)
        origin_movie = request.user.personal_movies.get(id=originId)
        request.user.personal_movies.remove(origin_movie)
        request.user.personal_movies.add(movie)
        serializer = MovieListSerializer(origin_movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def chatting(request):
    me = request.user
    if request.method == 'GET':
        get_messages = me.from_chatting.through.objects.filter(user=me, to_user=me).order_by('-id')
        serializer_get_messages = ChattingSerializer(get_messages, many=True)
        send_messages = me.from_chatting.through.objects.filter(user=me, from_user=me).order_by('-id')
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
        from_message = Chatting(user=me, from_user=me, to_user=to_user, content=content)
        to_message = Chatting(user=to_user, from_user=me, to_user=to_user, content=content)
        from_message_data = from_message.save()
        to_message_data = to_message.save()
        serializer_from = ChattingSerializer(from_message_data)
        return Response(serializer_from.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        chatId = request.data.get('chatId')
        if not chatId:
            return Response({'error': 'chatId가 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
        chatting = Chatting.objects.get(id=chatId)
        chatting.delete()
        return Response({'delete': "삭제되었습니다"}, status=status.HTTP_201_CREATED)
    # 읽음 확인
    elif request.method == 'PUT':
        chatId = request.data.get('chatId')
        if not chatId:
            return Response({'error': 'chatId가 없습니다'}, status=status.HTTP_400_BAD_REQUEST)
        chatting = Chatting.objects.get(id=chatId)
        chatting.is_read = True
        chatting.save()
        return Response({'update': f"{chatting.id}가 업데이트 되었습니다."}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def get_or_set_profile_image(request):
    if request.method == 'GET':
        if request.GET.get('nickname'):
            serializer = UserSerializer(get_object_or_404(get_user_model(), nickname=request.GET.get('nickname')), context={'user': request.user})
        else:
            serializer = UserSerializer(request.user, context={'user': request.user})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        img = request.FILES['files']
        user = request.user
        user.profile_img = img
        user.save()
        serializer = UserSerializer(user, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def follow(request):
    # 팔로우 리스트 반환
    if request.method == 'GET':
        followers = request.user.followers.all()
        followings = request.user.followings.all()
        actors = request.user.actor_following.all()
        crews = request.user.crew_following.all()
        serializer_followers = UserSerializer(followers, many=True, context={'user': request.user})
        serializer_followings = UserSerializer(followings, many=True, context={'user': request.user})
        serializer_actors = ActorProfileSerializer(actors, many=True, context={'user': request.user})
        serializer_crews = CrewProfileSerializer(crews, many=True, context={'user': request.user})
        data = {
            'followers': serializer_followers.data,
            'followings': serializer_followings.data,
            'actors': serializer_actors.data,
            'crews': serializer_crews.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # 유저, 배우, 감독 팔로우
    elif request.method == 'POST':
        me = request.user
        # 팔로우 할 종류
        follow = request.data.get('follow')
        if follow == 'user':
            user_id = request.data.get('follow_id')
            print(user_id)
            you = get_object_or_404(get_user_model(), id=user_id)

            if me.followings.filter(id=you.id).exists():
                me.followings.remove(you)
            else:
                me.followings.add(you)
            
            serializer = UserSerializer(you, context={'user': request.user})

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif follow == 'actor':
            actor_id = request.data.get('follow_id')
            actor = get_object_or_404(Actor, id=actor_id)
            if me.actor_following.filter(id=actor_id).exists():
                me.actor_following.remove(actor)
            else:
                me.actor_following.add(actor)
            
            serializer = ActorProfileSerializer(actor, context={'user': request.user})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif follow == 'crew':
            crew_id = request.data.get('follow_id')
            crew = get_object_or_404(Crew, id=crew_id)
            if me.crew_following.filter(id=crew_id).exists():
                me.crew_following.remove(crew)
            else:
                me.crew_following.add(crew)
            
            serializer = CrewProfileSerializer(crew, context={'user': request.user})
            return Response(serializer.data, status=status.HTTP_201_CREATED)