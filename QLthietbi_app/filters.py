import django_filters

from .models import *

class ThietBiFilter(django_filters.FilterSet):
    phong = django_filters.ModelChoiceFilter(queryset=Phong.objects.none())
    class Meta:
        model = ThietBi
        fields = ('loai_thiet_bi','tinh_trang', 'tang', 'phong')
        widgets = { 
            'loai_thiet_bi': django_filters.widgets.LinkWidget(attrs={'class': 'form-control'}),
            'tinh_trang': django_filters.widgets.LinkWidget(attrs={'class': 'form-control'}),
            'tang': django_filters.widgets.LinkWidget(attrs={'class': 'form-control'}),
            'phong': django_filters.widgets.LinkWidget(attrs={'class': 'form-control'}),
        }
    