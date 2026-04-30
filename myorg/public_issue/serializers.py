# from rest_framework import serializers
# from .models import User, Issue, Rating


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class IssueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Issue
#         fields = '__all__'


# class RatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rating
#         fields = '__all__'

from rest_framework import serializers
from .models import User, Issue, Rating


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_name',
            'email',
            'contact_no'
        ]


# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'issue_id',
            'issue_type',
            'description',
            'location',
            'status',
            'created_date',
            'updated_date',
            'user',
            'user_name',
            'issue_img'
        ]


# Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    issue_id = serializers.CharField(source='issue.issue_id', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'rating_id',
            'issue',
            'issue_id',
            'rating_value',
            'created_date'
        ]
