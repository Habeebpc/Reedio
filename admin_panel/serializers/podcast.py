from rest_framework import serializers
from admin_panel.models import (
    Category,
    SubCategory,
    Podcast,
    PlayList,
    Package
)
from django.shortcuts import get_object_or_404
from retailer.models import AccessCode
from customer.models import AudioProgress
from user_auth.models import User
from django.db.models import Q


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


class PodcastAnalyticsSerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    premium_users = serializers.SerializerMethodField()
    coupon_users = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = (
            'id',
            'created_user',
            'category',
            'sub_category',
            'name',
            'description',
            'image',
            'premium_users',
            'coupon_users'
        )

    def get_created_user(self, obj):
        if obj.created_by:
            return {'id': obj.created_by.id, 'name': obj.created_by.name}
        return {'id': None, 'name': None}

    def get_premium_users(self, obj):
        try:
            if obj.is_gold and not obj.is_diamond:
                premium_users = User.objects.filter(
                    Q(gold_user=True) | Q(diamond_user=True)
                ).distinct()
            elif obj.is_diamond:
                premium_users = User.objects.filter(
                    diamond_user=True
                )
            elif obj.is_gold:
                premium_users = User.objects.filter(
                    gold_user=True
                )
            count = premium_users.count()
            total_playlist = PlayList.objects.filter(podcast=obj).count()
            playlist_completed = AudioProgress.objects.filter(
                audio__podcast=obj,
                is_completed=True
            ).count()
            total_playlist_to_play = total_playlist * count

            try:
                total = (playlist_completed/total_playlist_to_play) * 100
            except Exception:
                total = 0

            return {
                'total_users': count,
                'completed_percentage': total
            }
        except Exception:
            return None

    def get_coupon_users(self, obj):
        access_code = AccessCode.objects.filter(
            podcast=obj,
            redeemed_by__isnull=False
        )
        count = access_code.count()
        total_playlist = PlayList.objects.filter(podcast=obj).count()
        playlist_completed = AudioProgress.objects.filter(
            audio__podcast=obj,
            is_completed=True
        ).count()
        total_playlist_to_play = total_playlist * count

        try:
            total = (playlist_completed/total_playlist_to_play) * 100
        except Exception:
            total = 0

        return {
            'total_users': count,
            'completed_percentage': total
        }


class AdminAccessCodeEnrolledSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_on')
    created_by = serializers.CharField(source='created_by.name')
    partner = serializers.CharField(source='podcast.created_by.name')
    podcast = serializers.CharField(source='podcast.name')
    redeemed_by = serializers.SerializerMethodField()

    class Meta:
        model = AccessCode
        fields = (
            'id',
            'date',
            'created_by',
            'partner',
            'podcast',
            'code',
            'sent_to',
            'redeemed_by'
        )

    def get_redeemed_by(self, obj):
        return {
            'name': obj.redeemed_by.name,
            'mobile': obj.redeemed_by.mobile,
            'date': obj.redeemed_on
        } if obj.redeemed_by else None
