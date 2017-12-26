from rest_framework import serializers

from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer needs for serialize base user fields like(username, password, email, avatar, url)
    """
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(use_url=True, required=False)
    url = ParameterisedHyperlinkedIdentityField(view_name='users:user-detail', lookup_fields=(('pk', 'user_id'),),
                                                read_only=True)

    def create(self, validated_data: dict) -> User:
        """
        Create User object and commit to database

        :param validated_data: data form http request
        :return: User object
        """
        user = User(username=validated_data.get('username', None),
                    email=validated_data.get('email', None),
                    avatar=validated_data.get('avatar', None))
        user.set_password(validated_data.get('password', None))
        user.save()
        return user

    def update(self, instance: User, validated_data: dict) -> User:
        """
        Update all fields for specific instance

        :param instance: user object
        :param validated_data: data form http request
        :return: updated User object
        """
        for field in validated_data:
            if field == 'password':
                instance.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'email', 'avatar')
