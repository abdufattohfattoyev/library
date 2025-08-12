from django.urls import path
from .views import (
    home,
    get_bolimlar,
    JurnalListView,
    JurnalDetailView
)

urlpatterns = [
    # Asosiy sahifa - fanlar ro'yxati
    path('', home, name='home'),

    # AJAX orqali bo'limlarni olish
    path('fanlar/<int:fan_id>/bolimlar/ajax/', get_bolimlar, name='get-bolimlar'),

    # Jurnallar ro'yxati
    path('fanlar/<int:fan_id>/bolimlar/<int:bolim_id>/jurnallar/',
         JurnalListView.as_view(), name='jurnal_list'),

    # Jurnal tafsilotlari
    path('fanlar/<int:fan_id>/bolimlar/<int:bolim_id>/jurnallar/<int:pk>/',
         JurnalDetailView.as_view(), name='jurnal_detail'),
]