from django.db import models


class Fan(models.Model):
    nomi = models.CharField(max_length=255, unique=True, verbose_name="Fan nomi")

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"


class Bolim(models.Model):
    nomi = models.CharField(max_length=255, unique=True, verbose_name="Bo'lim nomi")

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"


class Jurnal(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name='jurnallar', verbose_name="Fan")
    bolim = models.ForeignKey(Bolim, on_delete=models.CASCADE, related_name='jurnallar', verbose_name="Bo'lim")

    nomi = models.CharField(max_length=255, verbose_name="Jurnal nomi")
    rasmi = models.ImageField(upload_to='jurnallar_rasmlari/', blank=True, null=True, verbose_name="Jurnal rasmi")

    nashr_chastotasi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nashr chastotasi")
    murojaat_link = models.URLField(blank=True, null=True, verbose_name="Murojaat uchun havola")
    jurnal_sayti = models.URLField(blank=True, null=True, verbose_name="Jurnal sayti")
    talablar_link = models.URLField(blank=True, null=True, verbose_name="Jurnal talablari havolasi")

    def __str__(self):
        return f"{self.nomi} ({self.bolim.nomi} - {self.fan.nomi})"

    class Meta:
        verbose_name = "Jurnal"
        verbose_name_plural = "Jurnallar"


def populate_initial_data():
    fanlar = [
        "Fizika-matematika fanlari",
        "Kimyo fanlari",
        "Biologiya fanlari",
        "Geologiya-mineralogiya fanlari",
        "Texnika fanlari",
        "Qishloq xo'jaligi fanlari",
        "Tarix fanlari",
        "Iqtisodiyot fanlari",
        "Falsafa fanlari",
        "Filologiya fanlari",
        "Geografiya fanlari",
        "Yuridik fanlar",
        "Pedagogika fanlari",
        "Tibbiyot fanlari",
        "Farmatsevtika fanlari",
        "Veterinariya fanlari",
        "San'atshunoslik fanlari",
        "Arxitektura",
        "Psixologiya fanlari",
        "Harbiy fanlar",
        "Sotsiologiya fanlari",
        "Siyosiy fanlar",
        "Islomshunoslik fanlari"
    ]

    bolimlar = [
        "Milliy nashrlar",
        "Mustaqil davlatlar hamdo'stligi mamlakatlari nashrlari",
        "Evropa mamlakatlari nashrlari",
        "Amerika mamlakatlari nashrlari"
    ]

    for fan_nomi in fanlar:
        Fan.objects.get_or_create(nomi=fan_nomi)

    for bolim_nomi in bolimlar:
        Bolim.objects.get_or_create(nomi=bolim_nomi)
