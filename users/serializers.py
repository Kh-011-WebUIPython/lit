from rest_framework import serializers

from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(use_url=True)
    url = ParameterisedHyperlinkedIdentityField(view_name='users:user-detail', lookup_fields=(('pk', 'user_id'),),
                                                read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'email', 'avatar')
