from rest_framework import serializers

from branches.models import Branch, STATUS_ACTIVE


class BranchSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        branch = Branch(repository_id=self.context['repository_id'],
                        name=validated_data.get('name', None),
                        status=STATUS_ACTIVE)
        branch.save()
        return branch

    # def update(self, instance, validated_data):
    #     pass

    class Meta:
        model = Branch
        fields = ('id', 'name', 'status')
        # extra_kwargs = {
        #     'url': {
        #         'view_name': 'repositories:repository-detail:branches:branch-detail',
        #     }
        # }
