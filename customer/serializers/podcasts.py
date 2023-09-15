from rest_framework import serializers
from admin_panel.models import Category, SubCategory, Podcast, PlayList
from customer.models import Favorite


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon')


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'description', 'icon')


class PodcastListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ('id', 'image', 'name')


class PlayListInPodcast(serializers.ModelSerializer):

    class Meta:
        model = PlayList
        fields = ('id', 'name', 'description', 'audio_url', 'sub_required')


class PodcastDetailSerializer(serializers.ModelSerializer):
    play_list = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = ('id', 'image', 'name', 'description',
                  'updated_on', 'play_list', 'favorite')

    def get_play_list(self, obj):
        return PlayListInPodcast(obj.play_lists.all(), many=True).data

    def get_favorite(self, obj):
        if Favorite.objects.filter(
                podcast=obj, user=self.context['user']).exists():
            return True
        return False


class AddToFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('podcast',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'podcast_id': instance.podcast.id,
            'image': instance.podcast.image,
            'name': instance.podcast.name,
        }
