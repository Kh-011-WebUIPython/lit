import logging

from rest_framework import serializers

from commits.models import Commit
from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField

logger = logging.getLogger(__name__)


class CommitSerializer(serializers.ModelSerializer):
    # url = ParameterisedHyperlinkedIdentityField(view_name='commits:commit-detail',
    #                                              lookup_fields=(
    #                                                  ('repository_id', 'repository_id'), ('branch_id', 'branch_id'),
    #                                                  ('pk', 'commit_id')),
    #                                             read_only=True)

    def create(self, validated_data):
        commit_to_save = Commit(id=validated_data.get('id'),
                                long_hash=validated_data.get('long_hash', None),
                                commit_time=validated_data.get('commit_time', None),
                                comment=validated_data.get('message', None))
        commit_to_save.save()

    def update(self, instance, validated_data):
        for field in validated_data:
            instance.__setattr__(field, validated_data)
        instance.save()
        return instance

    class Meta:
        model = Commit
        fields = ('id', 'long_hash', 'comment', 'commit_time',)
