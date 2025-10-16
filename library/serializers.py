from rest_framework import serializers
from .models import Fan, Bolim, Jurnal


class FanSerializer(serializers.ModelSerializer):
    """Fan serializer - faqat fan ma'lumotlari"""

    class Meta:
        model = Fan
        fields = ['id', 'nomi']


class BolimSerializer(serializers.ModelSerializer):
    """Bo'lim serializer - faqat bo'lim ma'lumotlari"""

    class Meta:
        model = Bolim
        fields = ['id', 'nomi']


class JurnalSerializer(serializers.ModelSerializer):
    """Jurnal serializer - barcha ma'lumotlar"""
    fan_nomi = serializers.CharField(source='fan.nomi', read_only=True)
    bolim_nomi = serializers.CharField(source='bolim.nomi', read_only=True)
    rasm_url = serializers.SerializerMethodField()

    class Meta:
        model = Jurnal
        fields = [
            'id',
            'nomi',
            'fan',
            'fan_nomi',
            'bolim',
            'bolim_nomi',
            'rasm_url',
            'nashr_chastotasi',
            'murojaat_link',
            'jurnal_sayti',
            'talablar_link'
        ]

    def get_rasm_url(self, obj):
        """Rasm URL ni qaytaradi"""
        if obj.rasmi:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.rasmi.url)
            return obj.rasmi.url
        return None