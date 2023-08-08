import json
from .models import *
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        role = data['role']
        user = User.objects.create_user(username=username, password=password)
        try:
            group = Group.objects.get(name=role)
            user.groups.add(group)
            if role == 'Members':
                Member.objects.create(user=user)
            return Response({'message': 'User registered successfully'})
        except:
            return Response({'message': 'The role does not exists'})
    except Exception as e:
        return Response({'message': 'Internal server error', 'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'message': 'Logged In', 'access_token': access_token, 'user_id': user.id, 'group_id':user.groups.first().id}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'message': 'Internal server error', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
