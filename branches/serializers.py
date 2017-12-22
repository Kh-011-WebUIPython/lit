from rest_framework import serializers

from branches.models import Branch
from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField


class BranchSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(view_name='branches:branch-detail',
                                                lookup_fields=(('repository_id', 'repository_id'), ('pk', 'branch_id')),
                                                read_only=True)

    def create(self, validated_data):
        branch = Branch(repository_id=self.context['repository_id'],
                        name=validated_data.get('name', None), )
        branch.save()
        return branch

    class Meta:
        model = Branch
        fields = ('url', 'id', 'name',)
