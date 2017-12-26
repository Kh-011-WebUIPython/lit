from rest_framework import serializers

from branches.models import Branch
from lit.parameterised_hyperlinkedidentityfield import ParameterisedHyperlinkedIdentityField


# TODO implement initialization default branch for repository
# TODO add branch commits in serializer

class BranchSerializer(serializers.ModelSerializer):
    """
    Branch serializer needs for render base branch fields(url, id, name, commits) in JSON or XML

    """
    url = ParameterisedHyperlinkedIdentityField(view_name='branches:branch-detail',
                                                lookup_fields=(('repository_id', 'repository_id'), ('pk', 'branch_id')),
                                                read_only=True)

    def create(self, validated_data: dict) -> Branch:
        """
        Create branch object and save to DB

        :param validated_data: data form http request
        :return: Branch object
        """
        branch = Branch(repository_id=self.context['repository_id'],
                        name=validated_data.get('name', None), )
        branch.save()
        return branch

    # TODO
    def update(self, instance: Branch, validated_data: dict) -> Branch:
        pass

    class Meta:
        model = Branch
        fields = ('url', 'id', 'name',)
