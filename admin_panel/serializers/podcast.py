from rest_framework import serializers
from admin_panel.models import (
    Category,
    SubCategory,
    Podcast,
    PlayList,
    Package
)
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon')


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'description', 'icon')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'description', 'amount', 'validity')


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        exclude = ('added_on', 'podcast', 'is_trashed')


class PodcastSerializer(serializers.ModelSerializer):
    play_list = PlayListSerializer(write_only=True, many=True)
    created_user = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = (
            'id',
            'category',
            'sub_category',
            'name',
            'description',
            'price',
            'is_gold',
            'is_diamond',
            'image',
            'created_user',
            'play_list'
        )

    def get_created_user(self, obj):
        if obj.created_by:
            return {'id': obj.created_by.id, 'name': obj.created_by.name}
        return {'id': None, 'name': None}

    def create(self, validated_data):
        validated_data['created_by'] = self.context['user']
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
            instance.play_lists.filter(
                is_trashed=False).order_by('position'), many=True).data
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
        exclude = ('added_on', 'podcast', 'is_trashed')

    def create(self, validated_data):
        podcast = get_object_or_404(Podcast, id=self.context['podcast_id'])
        validated_data['podcast'] = podcast
        return super().create(validated_data)


class RestorePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ()

    def update(self, instance, validated_data):
        instance.is_trashed = False
        return super().update(instance, validated_data)


class DeletedPlayListSerializer(serializers.ModelSerializer):
    podcast = serializers.CharField(source='podcast.name')

    class Meta:
        model = PlayList
        fields = ('id', 'podcast', 'name', 'description', 'audio_url')
