from rest_framework import serializers
import logging

from commits.models import Commit


from branches.models import Branch

logger = logging.getLogger(__name__)


class CommitSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.__setattr__(field, validated_data)
        instance.save()
        return instance


    class Meta:
        model = Commit
        fields = ('user','branch','url','id')
        extra_kwargs = {
            'url': {
                'view_name': 'commits:commit-detail',
            }
        }