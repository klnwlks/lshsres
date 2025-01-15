# Create your views here.

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import User, Post, Section
from .serializers import (
    UserSerializer, UserDetailSerializer,
    PostSerializer, PostDetailSerializer,
    SectionSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def redirect_to_login(request):
    """
    GET / - Redirects to login page
    """
    return redirect('login/')

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST / - Login and get token
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.isStudent:
        return Response({
            'error': 'Only students can login through this endpoint'
        }, status=status.HTTP_403_FORBIDDEN)

    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'name': user.name,
        'section': user.section.id if user.section else None
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id):
    """
    GET /:userID - Get user profile
    """
    user = get_object_or_404(User, id=user_id)
    serializer = UserDetailSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def global_chat(request):
    """
    GET /board - Get global chat messages
    """
    posts = Post.objects.filter(section=None).order_by('-date_made')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_global_message(request):
    """
    POST /board - Create global message
    """
    serializer = PostSerializer(data={
        **request.data,
        'author': request.user.id,
        'section': None
    })
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SectionAccessMixin:
    """
    Mixin to check if user has access to section
    """
    def check_section_access(self, user, section):
        return user.section == section or user.advised_sections.filter(id=section.id).exists()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def section_chat(request, section_id):
    """
    GET /:section - Get section chat messages
    """
    section = get_object_or_404(Section, id=section_id)
    
    # Check if user has access to this section
    if not SectionAccessMixin().check_section_access(request.user, section):
        return Response({
            'error': 'You do not have access to this section'
        }, status=status.HTTP_403_FORBIDDEN)
    
    posts = Post.objects.filter(section=section).order_by('-date_made')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_section_message(request, section_id):
    """
    POST /:section - Create section message
    """
    section = get_object_or_404(Section, id=section_id)
    
    # Check if user has access to this section
    if not SectionAccessMixin().check_section_access(request.user, section):
        return Response({
            'error': 'You do not have access to this section'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PostSerializer(data={
        **request.data,
        'author': request.user.id,
        'section': section_id
    })
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)