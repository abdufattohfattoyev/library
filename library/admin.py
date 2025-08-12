from django.contrib import admin
from .models import Fan, Bolim, Jurnal


@admin.register(Fan)
class FanAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'jurnallar_soni')
    search_fields = ('nomi',)

    def jurnallar_soni(self, obj):
        return obj.jurnallar.count()

    jurnallar_soni.short_description = "Jurnallar soni"


@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'jurnallar_soni')
    search_fields = ('nomi',)

    def jurnallar_soni(self, obj):
        return obj.jurnallar.count()

    jurnallar_soni.short_description = "Jurnallar soni"


@admin.register(Jurnal)
class JurnalAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'fan', 'bolim', 'nashr_chastotasi', 'rasmi_tag')
    list_filter = ('fan', 'bolim')
    search_fields = ('nomi', 'fan__nomi', 'bolim__nomi')
    readonly_fields = ('rasmi_preview',)
    fieldsets = (
        (None, {
            'fields': ('nomi', 'fan', 'bolim')
        }),
        ('Media', {
            'fields': ('rasmi', 'rasmi_preview')
        }),
        ('Qoshimcha malumotlar', {
        'fields': ('nashr_chastotasi', 'murojaat_link', 'jurnal_sayti', 'talablar_link'),
        'classes': ('collapse',)
    }),
    )

    def rasmi_tag(self, obj):
        if obj.rasmi:
            return f'<img src="{obj.rasmi.url}" style="max-height: 50px;" />'
        return "-"

    rasmi_tag.short_description = "Rasm"
    rasmi_tag.allow_tags = True

    def rasmi_preview(self, obj):
        if obj.rasmi:
            return f'<img src="{obj.rasmi.url}" style="max-height: 300px;" />'
        return "Rasm yuklanmagan"

    rasmi_preview.short_description = "Rasm ko'rinishi"
    rasmi_preview.allow_tags = True