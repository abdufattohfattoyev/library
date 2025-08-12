from django import forms
from .models import Jurnal

class JurnalForm(forms.ModelForm):
    class Meta:
        model = Jurnal
        fields = '__all__'
        widgets = {
            'nomi': forms.TextInput(attrs={'class': 'form-control'}),
            'fan': forms.Select(attrs={'class': 'form-control'}),
            'bolim': forms.Select(attrs={'class': 'form-control'}),
            'rasmi': forms.FileInput(attrs={'class': 'form-control'}),
            'nashr_chastotasi': forms.TextInput(attrs={'class': 'form-control'}),
            'murojaat_link': forms.URLInput(attrs={'class': 'form-control'}),
            'jurnal_sayti': forms.URLInput(attrs={'class': 'form-control'}),
            'talablar_link': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nomi': 'Jurnal nomi',
            'fan': 'Fan',
            'bolim': 'Bo\'lim',
            'rasmi': 'Jurnal rasmi',
            'nashr_chastotasi': 'Nashr chastotasi',
            'murojaat_link': 'Murojaat uchun havola',
            'jurnal_sayti': 'Jurnal sayti',
            'talablar_link': 'Jurnal talablari havolasi',
        }