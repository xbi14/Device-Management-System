from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import *
from django import forms

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'ho', 'ten', 'gioi_tinh', 'chuc_vu', 'ngay_sinh', 'email', 'sdt', 'ngay_vao_lam', 'is_staff', 'is_active')
    list_filter = ('chuc_vu', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('ho', 'ten', 'gioi_tinh', 'chuc_vu', 'ngay_sinh', 'email', 'sdt', 'ngay_vao_lam')}),
        ('Quyền hạn', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'ho', 'ten', 'password1', 'password2', 'sdt', 'gioi_tinh', 'ngay_sinh', 'chuc_vu', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username', 'email', 'ho', 'ten')
    ordering = ('id',)
    
admin.site.register(CustomUser, CustomUserAdmin)

class ThietBiInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True
    
class ThietBiInline(admin.TabularInline):
    model = ThietBi

class PhongAdmin(admin.ModelAdmin):
    inlines = [ThietBiInline]
    list_display = ('ten_phong', 'tang')
    list_filter = ('tang',)
    search_fields = ('ten_phong', 'tang')
    list_per_page = 10

class TangAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_tang')
    list_per_page = 10

class LoaiThietBiAdmin(admin.ModelAdmin):
    list_display = ('id','ten_loaithietbi')
    list_per_page = 10

class ThietBiAdmin(admin.ModelAdmin):
    list_display = ['id_thiet_bi', 'ten_thiet_bi','hinh_anh', 'loai_thiet_bi', 'phong', 'ngay_mua', 'gia_mua', 'tinh_trang', 'ngay_bao_tri', 'don_vi_cung_cap', 'mo_ta']
    list_filter = ('loai_thiet_bi', 'tinh_trang', 'tang', 'phong')
    search_fields = ('ten_thiet_bi', 'loai_thiet_bi', 'tinh_trang')
    ordering = ('id_thiet_bi',)
    list_per_page = 10
    
class BaoCaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tieu_de', 'ngay_bao_cao', 'trang_thai', 'nguoi_bao_cao')
    list_per_page = 10
    ordering = ('id',)
    
    
admin.site.register(BaoCao, BaoCaoAdmin)
admin.site.register(Tang, TangAdmin)
admin.site.register(Phong, PhongAdmin)
admin.site.register(LoaiThietBi, LoaiThietBiAdmin)
admin.site.register(ThietBi, ThietBiAdmin)








