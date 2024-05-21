from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile

class ProfileSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.CharField(read_only=True, source="user.get_full_name")
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "full_name", "email", "profile_photo", "phone_number", "gender", "country", "city", "about_me"]

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


class UpdateProfileSerializers(serializers.ModelSerializer):
    country = CountryField(read_only=True)

    class Meta:
        model = Profile
        fields = ["profile_photo", "phone_number", "gender", "country", "city", "about_me"]


class FollowingSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "profile_photo", "about_me"]
