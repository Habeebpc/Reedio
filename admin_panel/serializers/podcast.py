from rest_framework import serializers
from admin_panel.models import (
    Category,
    SubCategory,
    Podcast,
    PlayList,
)
from django.shortcuts import get_object_or_404

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'description')


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        exclude = ('added_on', 'podcast')


class PodcastSerializer(serializers.ModelSerializer):
    play_list = PlayListSerializer(write_only=True, many=True)

    class Meta:
        model = Podcast
        fields = ('id', 'category', 'sub_category', 'name',
                  'description', 'image', 'play_list')

    def create(self, validated_data):
        play_list = validated_data.pop('play_list', [])
        instance = super().create(validated_data)
        for item in play_list:
            PlayList.objects.create(podcast=instance, **item)
        return instance

    def update(self, instance, validated_data):
        play_list = validated_data.pop('play_list', [])
        instance = super().update(instance, validated_data)
        for item in play_list:
            PlayList.objects.create(podcast=instance, **item)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['is_approved'] = instance.is_approved
        rep['play_list'] = PlayListSerializer(
            instance.play_lists.all(), many=True).data
        return rep


class PodcastAdminApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ()

    def update(self, instance, validated_data):
        instance.is_approved = True
        return super().update(instance, validated_data)


class AddPlayListToPodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        exclude = ('added_on', 'podcast')

    def create(self, validated_data):
        podcast = get_object_or_404(Podcast, id=self.context['podcast_id'])
        validated_data['podcast'] = podcast
        return super().create(validated_data)
