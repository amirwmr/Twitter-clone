# TODO: Change this in production
from twitter_api.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer

from .serializers import ProfileSerializers, UpdateProfileSerializers, FollowingSerializers

User = get_user_model()

class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializers
    renderer_classes = (ProfileJSONRenderer,)

    def get_queryset(self):
        return Profile.objects.select_related("user")

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UpdateProfileSerializers

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)


class FollowerListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles= profile.followers.all()
            serializer = FollowingSerializers(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data
            }
            return Response(formatted_response, status = status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class FollowingListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profiles= profile.following.all()
            users = [p.user for p in following_profiles]
            serializer = FollowingSerializers(users, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "users_i_follow": serializer.data
            }
            return Response(formatted_response, status = status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class FollowAPIView(APIView):
    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            follower = Profile.objects.get(user = self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise(CantFollowYourself)

            if user_profile.check_following(profile):
                formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":f"You already following {profile.user.get_full_name}!"
                }
                return Response(formatted_response, status = status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "message":f"You are now following {profile.user.get_full_name}!"
                }
            return Response(formatted_response, status = status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class UnFollowAPIView(APIView):
    def post(self, request, user_id, format=None, *args, **kwargs):

        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile):
                formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message":f"You are not following {profile.user.get_full_name}!"
                }
                return Response(formatted_response, status = status.HTTP_400_BAD_REQUEST)

        user_profile.unfollow(profile)
        formatted_response = {
                "status_code": status.HTTP_200_OK,
                "message":f"You have unfollowed {profile.user.get_full_name}!"
                }
        return Response(formatted_response, status = status.HTTP_200_OK)