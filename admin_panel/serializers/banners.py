from rest_framework import serializers
from admin_panel.models import Banner, DummyImage


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'name', 'description', 'image', 'redirect_url')


class DummyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyImage
        fields = ('id', 'image', 'redirect_url')
