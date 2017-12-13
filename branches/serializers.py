from rest_framework import serializers

from branches.models import Branch, BranchCommit


class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Branch
        fields = ('url', 'id', 'name', 'repository', 'status')
        extra_kwargs = {
            'url': {
                'view_name': 'branches:branch-detail',
            }
        }


# class BranchCommitSerializer(serializers.HyperlinkedModelSerializer):
#     branch = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     commit = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#
#
#     class Meta:
#         model = BranchCommit
#         fields = ('url', 'id', 'branch', 'commit')
