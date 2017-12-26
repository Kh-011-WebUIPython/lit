import logging

from rest_framework import serializers

from commits.models import Commit
from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField

logger = logging.getLogger(__name__)


class CommitSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='commits:commit-detail',
                                                lookup_fields=(
                                                    ('repository_id', 'repository_id'), ('branch_id', 'branch_id'),
                                                    ('pk', 'commit_id')),
                                                read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.__setattr__(field, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Commit
        fields = ('url', 'id', 'user', 'branch',)
