from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q  # Qidiruv uchun import qilindi
from .models import Fan, Bolim, Jurnal


def home(request):
    """
    Asosiy sahifa - barcha fanlar ro'yxati ko'rsatiladi
    """
    fanlar = Fan.objects.order_by('nomi')
    return render(request, 'jurnallar/home.html', {'fanlar': fanlar})


def get_bolimlar(request, fan_id):
    """
    AJAX orqali tanlangan fan uchun bo'limlarni qaytaradi
    """
    if request.method == 'GET':
        try:
            fan = get_object_or_404(Fan, pk=fan_id)
            bolimlar = Bolim.objects.order_by('id')
            bolimlar_data = [{'id': bolim.id, 'nomi': bolim.nomi} for bolim in bolimlar]
            return JsonResponse({'success': True, 'bolimlar': bolimlar_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


class JurnalListView(ListView):
    """
    Tanlangan fan va bo'lim uchun jurnallar ro'yxati
    Qidiruv va Pagination funksiyalari qo'shilgan
    """
    template_name = 'jurnallar/jurnal_list.html'
    context_object_name = 'jurnallar'
    paginate_by = 12

    def get_queryset(self):
        # URL dan fan va bo'limni olish
        self.fan = get_object_or_404(Fan, pk=self.kwargs['fan_id'])
        self.bolim = get_object_or_404(Bolim, pk=self.kwargs['bolim_id'])

        # Asosiy queryset
        queryset = Jurnal.objects.filter(fan=self.fan, bolim=self.bolim).order_by('nomi')

        # Qidiruv so'rovini olish
        query = self.request.GET.get('q')
        if query:
            # Jurnal nomi bo'yicha qidirish (katta-kichik harflarni farqlamaydi)
            queryset = queryset.filter(Q(nomi__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fan'] = self.fan
        context['bolim'] = self.bolim
        # Qidiruv so'rovini shablonga uzatish (inputda ko'rsatish uchun)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class JurnalDetailView(DetailView):
    """
    Jurnal tafsilotlari
    """
    model = Jurnal
    template_name = 'jurnallar/jurnal_detail.html'
    context_object_name = 'jurnal'

    def get_queryset(self):
        return Jurnal.objects.filter(
            pk=self.kwargs['pk'],
            bolim_id=self.kwargs['bolim_id'],
            fan_id=self.kwargs['fan_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jurnal = self.get_object()
        context['fan'] = jurnal.fan
        context['bolim'] = jurnal.bolim
        return context
