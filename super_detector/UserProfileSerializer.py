from rest_framework import  serializers
from super_detector.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = ('user_id', 'dob', 'delivary_address', 'city', 'country', 'pin')