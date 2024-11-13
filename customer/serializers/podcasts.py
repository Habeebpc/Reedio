from rest_framework import serializers
from admin_panel.models import Category, SubCategory, Podcast, PlayList
from customer.models import (
    Favorite,
    FavoriteAudio,
    AudioProgress,
    PurchasePodcast
)
from django.shortcuts import get_object_or_404
from retailer.models import AccessCode
from datetime import datetime, date


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'icon')


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'description', 'icon')


class PodcastListSerializer(serializers.ModelSerializer):
    is_redeemed = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = (
            'id',
            'image',
            'name',
            'price',
            'is_gold',
            'is_diamond',
            'is_redeemed',
            'is_purchased'
        )

    def get_is_redeemed(self, obj):
        if AccessCode.objects.filter(
            podcast=obj,
                redeemed_by=self.context['user'],
                validity__gte=date.today()
        ).exists():
            return True
        return False

    def get_is_purchased(self, obj):
        if PurchasePodcast.objects.filter(
            podcast=obj, user=self.context['user']
        ).exists():
            return True
        return False


class PlayListInPodcast(serializers.ModelSerializer):
    favorite = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = PlayList
        fields = (
            'id',
            'name',
            'description',
            'audio_url',
            'sub_required',
            'favorite',
            'favorite_id',
            'progress'
        )

    def get_favorite(self, obj):
        if FavoriteAudio.objects.filter(
                playlist=obj, user=self.context['user']).exists():
            return True
        return False

    def get_favorite_id(self, obj):
        fav = FavoriteAudio.objects.filter(
            playlist=obj, user=self.context['user'])
        if fav.exists():
            return fav.last().id
        return None

    def get_progress(self, obj):
        progress = AudioProgress.objects.filter(
            audio=obj, user=self.context['user'])
        if progress:
            return progress.first().progress
        else:
            progress = AudioProgress.objects.create(
                audio=obj, user=self.context['user'])
            return progress.progress


class PodcastDetailSerializer(serializers.ModelSerializer):
    play_list = serializers.SerializerMethodField()
    favorite = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()
    is_redeemed = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = ('id', 'image', 'name', 'description',
                  'updated_on', 'play_list', 'favorite',
                  'favorite_id', 'is_redeemed')

    def get_play_list(self, obj):
        return PlayListInPodcast(
            obj.play_lists.filter(
                is_trashed=False).order_by('position'),
            many=True,
            context=self.context
        ).data

    def get_favorite(self, obj):
        if Favorite.objects.filter(
                podcast=obj, user=self.context['user']).exists():
            return True
        return False

    def get_favorite_id(self, obj):
        fav = Favorite.objects.filter(podcast=obj, user=self.context['user'])
        if fav.exists():
            return fav.last().id
        return None

    def get_is_redeemed(self, obj):
        if AccessCode.objects.filter(
            podcast=obj,
                redeemed_by=self.context['user'],
                validity__gte=date.today()
        ).exists():
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


class AddToFavoriteAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAudio
        fields = ('playlist',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'playlist_id': instance.playlist.id,
            'name': instance.playlist.name,
            'audio_url': instance.playlist.audio_url,
        }


class AudioProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioProgress
        fields = ('progress', 'is_completed')


class RedeemAccessCodeSerializer(serializers.Serializer):
    access_code = serializers.CharField()

    def validate(self, attrs):
        access_code = attrs['access_code']
        coupon = AccessCode.objects.filter(code=access_code)
        if not coupon.exists():
            raise serializers.ValidationError("Invalid access code")
        coupon = coupon.last()
        if coupon.redeemed_by is not None:
            raise serializers.ValidationError("Access code already redeemed")
        if coupon.validity < date.today():
            raise serializers.ValidationError("Access code expired")
        coupon.redeemed_by = self.context['user']
        coupon.redeemed_on = datetime.now()
        coupon.save(update_fields=['redeemed_by', 'redeemed_on'])
        podcast = coupon.podcast.name

        return {'message': f'Congrats, {podcast} unlocked successfully!!'}


class PurchasePodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasePodcast
        fields = ('podcast', 'transaction_id')

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)
