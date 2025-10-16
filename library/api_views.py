from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Fan, Bolim, Jurnal
from .serializers import FanSerializer, BolimSerializer, JurnalSerializer


class JurnalPagination(PageNumberPagination):
    """Pagination - 10 ta jurnal bitta sahifada"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint - barcha fanlar ro'yxati
    GET /api/fanlar/
    """
    queryset = Fan.objects.all().order_by('nomi')
    serializer_class = FanSerializer


class BolimViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint - barcha bo'limlar ro'yxati
    GET /api/bolimlar/
    """
    queryset = Bolim.objects.all().order_by('id')
    serializer_class = BolimSerializer


class JurnalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint - jurnallar

    Barcha jurnallar:
    GET /api/jurnallar/

    Fan bo'yicha:
    GET /api/jurnallar/?fan=1

    Bo'lim bo'yicha:
    GET /api/jurnallar/?bolim=1

    Fan va Bo'lim bo'yicha:
    GET /api/jurnallar/?fan=1&bolim=2

    Pagination:
    GET /api/jurnallar/?page=2
    """
    queryset = Jurnal.objects.all().select_related('fan', 'bolim')
    serializer_class = JurnalSerializer
    pagination_class = JurnalPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Fan bo'yicha filter
        fan_id = self.request.query_params.get('fan')
        if fan_id:
            queryset = queryset.filter(fan_id=fan_id)

        # Bo'lim bo'yicha filter
        bolim_id = self.request.query_params.get('bolim')
        if bolim_id:
            queryset = queryset.filter(bolim_id=bolim_id)

        return queryset.order_by('nomi')

    @action(detail=False, methods=['get'], url_path='fan/(?P<fan_id>[0-9]+)/bolim/(?P<bolim_id>[0-9]+)')
    def by_fan_bolim(self, request, fan_id=None, bolim_id=None):
        """
        Maxsus endpoint - fan va bo'lim bo'yicha jurnallar
        GET /api/jurnallar/fan/1/bolim/2/
        """
        jurnallar = self.get_queryset().filter(fan_id=fan_id, bolim_id=bolim_id)
        page = self.paginate_queryset(jurnallar)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(jurnallar, many=True)
        return Response(serializer.data)