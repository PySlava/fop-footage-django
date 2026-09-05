from django.db import models


class Fops(models.Model):
    class TaxSystem(models.TextChoices):
        GROUP_1 = 'EP_1', 'Спрощена (1 група)'
        GROUP_2 = 'EP_2', 'Спрощена (2 група)'
        GROUP_3_5 = 'EP_3_5', 'Спрощена (3 група 5%)'
        GROUP_3_3 = 'EP_3_3', 'Спрощена (3 група 3% + ПДВ)'
        GENERAL = 'GENERAL', 'Загальна система'

    # Основні дані
    full_name = models.CharField("ПІБ ФОП", max_length=255)
    tax_id = models.CharField("Податковий номер (ІПН / ЄДРПОУ)", max_length=10, unique=True)
    opf_code = models.CharField("Код ОПФ", max_length=10, default="910", help_text="910 — Фізична особа - підприємець")

    # Адреса реєстрації (Прописка)
    postal_code = models.CharField("Поштовий індекс", max_length=5, blank=True)
    region = models.CharField("Область", max_length=100, blank=True)
    district = models.CharField("Район", max_length=100, blank=True, null=True)
    city = models.CharField("Населений пункт", max_length=100, blank=True)
    katottg = models.CharField("Код КАТОТТГ", max_length=19, blank=True)
    street = models.CharField("Вулиця", max_length=150, blank=True)
    building = models.CharField("Будинок / Квартира", max_length=50, blank=True)

    # Діяльність та оподаткування
    main_kved = models.CharField("Основний КВЕД", max_length=100, blank=True)
    additional_kveds = models.TextField("Перелік додаткових КВЕДів", blank=True)
    tax_system = models.CharField("Система оподаткування", max_length=20, choices=TaxSystem.choices, default=TaxSystem.GROUP_3_5)

    # ДПС / ПФУ
    dps_code = models.CharField("Код ДПС", max_length=10, blank=True)
    dps_name = models.CharField("Назва ДПС", max_length=255, blank=True)
    pfu_code = models.CharField("Код органу ПФУ", max_length=10, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ФОП"
        verbose_name_plural = "ФОПи"

    def __str__(self):
        return f"ФОП {self.full_name} ({self.tax_id})"