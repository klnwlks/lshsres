from rest_framework import serializers
from .models import User, Post, Section

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with basic information.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'section', 'isStudent', 'datemade']
        read_only_fields = ['datemade']

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed User serializer including related posts.
    """
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'name', 'section', 'isStudent', 'datemade', 'posts']
        read_only_fields = ['datemade']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Posts with author details.
    """
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'author_name', 'date_made']
        read_only_fields = ['date_made', 'author_name']

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Post serializer with full author information.
    """
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'date_made']
        read_only_fields = ['date_made']

class SectionSerializer(serializers.ModelSerializer):
    """
    Basic Section serializer.
    """
    class Meta:
        model = Section
        fields = ['id', 'adviser', 'students']

class SectionDetailSerializer(serializers.ModelSerializer):
    """
    Detailed Section serializer with adviser and students information.
    """
    adviser = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Section
        fields = ['id', 'adviser', 'students', 'member_count', 'members']
    
    def get_member_count(self, obj):
        return len(obj.students) if obj.students else 0