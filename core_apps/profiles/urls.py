from django.urls import path
from . views import (
                    ProfileListAPIView,
                    ProfileDetailAPIView,
                    UpdateProfileAPIView,
                    FollowerListAPIView,
                    FollowingListAPIView,
                    FollowAPIView,
                    UnFollowAPIView,
                    )

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), ),
    path("me/", ProfileDetailAPIView.as_view(), ),
    path("me/update/", UpdateProfileAPIView.as_view(), ),
    path("me/followers/", FollowerListAPIView.as_view(), ),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(),),
    path("<uuid:user_id>/unfollow/", UnFollowAPIView.as_view(),),
]