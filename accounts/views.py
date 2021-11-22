from rest_framework import serializers, status
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Chatting
from .serializers.User import SignupSerializer, UserSerializer
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

@api_view(['GET', 'POST'])
def chatting(request):
    me = request.user
    if request.method == 'GET':
        messages = me.from_chatting.through.objects.filter(to_user=me)
        serializer = ChattingSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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