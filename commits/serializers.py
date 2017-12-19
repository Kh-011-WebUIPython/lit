from rest_framework import serializers


from branches.models import Branch


class CommitSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


    class Meta:
        model = Branch
        fields = ('name', 'commits')