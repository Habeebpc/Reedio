from rest_framework import serializers
from user_auth.models import User, PartnerAndRetailer
from admin_panel.models import Podcast, PlayList
from retailer.models import AccessCode
import string
import random
import requests
import json
from decouple import config


def generate_random_string(length=15):
    characters = string.ascii_letters.upper() + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_whatsapp_message(mobile, name, code, podcast_name):

    url = 'https://api.msg91.com/api/v5/whatsapp/whatsapp-outbound-message/bulk/'

    headers = {
        'Content-Type': 'application/json',
        'authkey': config('MSG91_AUTH_KEY')
    }

    payload = {
        "integrated_number": "916238769169",
        "content_type": "template",
        "payload": {
            "messaging_product": "whatsapp",
            "type": "template",
            "template": {
                "name": "reedio_freeaccess",
                "language": {
                    "code": "en_GB",
                    "policy": "deterministic"
                },
                "to_and_components": [
                    {
                        "to": [mobile],
                        "components": {
                            "body_1": {
                                "type": "text",
                                "value": name
                            },
                            "body_2": {
                                "type": "text",
                                "value": code
                            },
                            "body_3": {
                                "type": "text",
                                "value": podcast_name
                            },
                            "button_1": {
                                "subtype": "url",
                                "type": "text",
                                "value": "https://play.google.com/store/apps/details?id=com.podcast.reedio"
                            }
                        }
                    }
                ]
            }
        }
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text)


class MyPartnersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='partner.name')
    mobile = serializers.CharField(source='partner.mobile')
    email = serializers.CharField(source='partner.email')
    validity = serializers.DateField(source='partner.validity')

    class Meta:
        model = PartnerAndRetailer
        fields = ('id', 'name', 'mobile', 'email', 'validity')


class MyPartnerPodcastListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ('id', 'image', 'name')


class PlayListInMyPartnerPodcast(serializers.ModelSerializer):

    class Meta:
        model = PlayList
        fields = (
            'id',
            'name',
            'description',
            'audio_url',
            'sub_required',
        )


class MyPartnerPodcastDetailSerializer(serializers.ModelSerializer):
    play_list = serializers.SerializerMethodField()

    class Meta:
        model = Podcast
        fields = (
            'id',
            'image',
            'name',
            'description',
            'updated_on',
            'play_list',
            'price',
            'is_gold',
            'is_diamond'
        )

    def get_play_list(self, obj):
        return PlayListInMyPartnerPodcast(
            obj.play_lists.filter(
                is_trashed=False).order_by('position'),
            many=True,
        ).data


class AccessCodeGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessCode
        fields = ('id', 'podcast', 'sent_to', 'name')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['user']
        validated_data['code'] = generate_random_string()
        validated_data['validity'] = validated_data['podcast'].created_by.validity
        instance = super().create(validated_data)
        send_whatsapp_message(
            instance.sent_to,
            instance.name,
            instance.code,
            instance.podcast.name
        )
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['date'] = instance.created_on
        rep['podcast'] = instance.podcast.name
        rep['code'] = instance.code
        rep['sent_to'] = instance.sent_to
        rep['name'] = instance.name
        rep['redeemed_by'] = {
            'name': instance.redeemed_by.name,
            'mobile': instance.redeemed_by.mobile,
            'date': instance.redeemed_on
        } if instance.redeemed_by else None
        return rep
