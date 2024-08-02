from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class ThemThietBiForm(forms.ModelForm):
    
    class Meta:
        model = ThietBi
        fields = ('ten_thiet_bi', 'loai_thiet_bi', 'hinh_anh', 'mo_ta', 'ngay_mua', 'gia_mua', 'tinh_trang', 'tang', 'phong', 'don_vi_cung_cap')
        widgets = {
            'ten_thiet_bi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên thiết bị'}),
            'loai_thiet_bi': forms.Select(attrs={'class': 'form-control'}),
            'ngay_mua': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gia_mua': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nhập giá mua'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control'}),
            'tinh_trang': forms.Select(attrs={'class': 'form-control'}),
            'tang': forms.Select(attrs={'class': 'form-control', 'name': 'tang'}),
            'phong': forms.Select(attrs={'class': 'form-control', 'name': 'phong'}),
            'don_vi_cung_cap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập đơn vị cung cấp'}),
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['phong'].queryset = Phong.objects.none()
        
    #     if 'tang' in self.data:
    #         try:
    #             tang_id = int(self.data.get('tang'))
    #             self.fields['phong'].queryset = Phong.objects.filter(tang_id=tang_id).order_by('ten_phong')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['phong'].queryset = self.instance.tang.phong_set.order_by('ten_phong')
            
    def clean_gia_mua(self):
        gia_mua = self.cleaned_data.get('gia_mua')
        if gia_mua is not None and gia_mua < 0:
            raise forms.ValidationError("không được là số âm.")
        return gia_mua
    
    def clean_ngay_mua(self):
        ngay_mua = self.cleaned_data['ngay_mua']
        today = date.today()
        if ngay_mua > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        return ngay_mua
    
class LoaiThietBiForm(forms.ModelForm):
        
        class Meta:
            model = LoaiThietBi
            fields = ('ten_loaithietbi',)
            widgets = {
                'ten_loaithietbi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên loại thiết bị'}),
            }
    
class TangForm(forms.ModelForm):
    
    class Meta:
        model = Tang
        fields = ('ten_tang',)
        widgets = {
            'ten_tang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên tầng'}),
        }
        
class PhongForm(forms.ModelForm):
    
    class Meta:
        model = Phong
        fields = ('ten_phong', 'tang')
        widgets = {
            'ten_phong': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên phòng'}),
            'tang': forms.Select(attrs={'class': 'form-control'}),
        }
        
class BaoCaoForm(forms.ModelForm): 
    
    class Meta:
        model = BaoCao
        fields = ('tieu_de', 'noi_dung', 'thiet_bi', 'nguoi_bao_cao', 'ngay_bao_cao', 'thiet_bi_disabled', 'ngay_bao_cao_disabled', 'nguoi_bao_cao_disabled')
        widgets = {
            'tieu_de': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tiêu đề'}),
            'noi_dung': forms.Textarea(attrs={'class': 'form-control'}),
            'thiet_bi': forms.Select(attrs={'class': 'form-control'}),
            'ngay_bao_cao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nguoi_bao_cao': forms.Select(attrs={'class': 'form-control'}),
            
            'thiet_bi_disabled': forms.Select(attrs={'class': 'form-control'}),
            'ngay_bao_cao_disabled': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nguoi_bao_cao_disabled': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_ngay_bao_cao(self):
        ngay_bao_cao = self.cleaned_data['ngay_bao_cao']
        today = date.today()
        if ngay_bao_cao > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        return ngay_bao_cao
        
class HoSoForm(forms.ModelForm): 
    
    class Meta:
        model = CustomUser
        fields = ('ho', 'ten', 'gioi_tinh', 'chuc_vu', 'anh_the', 'ngay_sinh','ngay_vao_lam', 'dia_chi', 'sdt', 'email', 'username', 'password')
        widgets = {
            'ho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ'}),
            'ten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên'}),
            'gioi_tinh': forms.Select(attrs={'class': 'form-control'}),
            'chuc_vu': forms.Select(attrs={'class': 'form-control'}),
            'anh_the': forms.FileInput(attrs={'class': 'form-control'}),
            'ngay_sinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ngay_vao_lam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dia_chi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên đăng nhập'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'}),
        }
        
        
    def clean_ngay_sinh(self):
        ngay_sinh = self.cleaned_data['ngay_sinh']
        today = date.today()
        
        if ngay_sinh is None:
            return ngay_sinh
        
        if ngay_sinh > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        if ngay_sinh.year < 1900:
            raise forms.ValidationError("không được nhỏ hơn năm 1900.")
        if ngay_sinh.year > 2002:
            raise forms.ValidationError("không được lớn hơn năm 2002.")
        
        return ngay_sinh
    
    def clean_sdt(self):
        sdt = self.cleaned_data.get('sdt')
        if sdt is not None and len(str(sdt)) != 10:
            raise forms.ValidationError("phải có 10 chữ số.")
        return sdt
    
    def clean_ngay_sinh(self):
        ngay_sinh = self.cleaned_data['ngay_sinh']
        today = date.today()
        
        if ngay_sinh is None:
            return ngay_sinh
        
        if ngay_sinh > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        if ngay_sinh.year < 1900:
            raise forms.ValidationError("không được nhỏ hơn năm 1900.")
        if ngay_sinh.year > 2002:
            raise forms.ValidationError("không được lớn hơn năm 2002.")
        
        return ngay_sinh
    
    def clean_password(self):
        password = self.cleaned_data['password']
        
        error_messages = {
            "This password is too short. It must contain at least 8 characters.": "Mật khẩu phải có ít nhất 8 ký tự.",
            "This password is too common.": "Mật khẩu quá phổ biến.",
            "This password is entirely numeric.": "Mật khẩu không được toàn số.",
            "This password is too similar to the username.": "Mật khẩu không được giống tên đăng nhập.",
            "The password is too similar to the email address.": "Mật khẩu không được giống email.",
            "The password is too similar to the first name.": "Mật khẩu không được giống tên.",
            "The password is too similar to the last name.": "Mật khẩu không được giống họ.",
            "The password is too similar to the common sequences.": "Mật khẩu không được giống chuỗi phổ biến."
        }
        
        try:
            validate_password(password)
        except ValidationError as error:
            error_messages_vietnamese = [error_messages.get(msg, msg) for msg in error.messages]
            raise forms.ValidationError("Mật khẩu không đúng định dạng. " + " ".join(error_messages_vietnamese))
        
        return password
    
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Mật khẩu hiện tại',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password = forms.CharField(
        label='Mật khẩu mới',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirm_password = forms.CharField(
        label='Xác nhận mật khẩu mới',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Mật khẩu hiện tại không chính xác.')
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Mật khẩu mới và xác nhận mật khẩu không khớp.')

        return cleaned_data

    def save(self):
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        
class SuaHoSoForm(forms.ModelForm): 
    
    class Meta:
        model = CustomUser
        fields = ('ho', 'ten', 'gioi_tinh', 'anh_the', 'ngay_sinh','ngay_vao_lam', 'dia_chi', 'sdt', 'email')
        widgets = {
            'ho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ'}),
            'ten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên'}),
            'gioi_tinh': forms.Select(attrs={'class': 'form-control'}),
            'anh_the': forms.FileInput(attrs={'class': 'form-control'}),
            'ngay_sinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ngay_vao_lam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dia_chi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập địa chỉ'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập số điện thoại'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),
        }
        
        
    def clean_ngay_sinh(self):
        ngay_sinh = self.cleaned_data['ngay_sinh']
        today = date.today()
        
        if ngay_sinh is None:
            return ngay_sinh
        
        if ngay_sinh > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        if ngay_sinh.year < 1900:
            raise forms.ValidationError("không được nhỏ hơn năm 1900.")
        if ngay_sinh.year > 2002:
            raise forms.ValidationError("không được lớn hơn năm 2002.")
        
        return ngay_sinh
    
    def clean_sdt(self):
        sdt = self.cleaned_data.get('sdt')
        if sdt is not None and len(str(sdt)) != 10:
            raise forms.ValidationError("phải có 10 chữ số.")
        return sdt
    
    def clean_ngay_sinh(self):
        ngay_sinh = self.cleaned_data['ngay_sinh']
        today = date.today()
        
        if ngay_sinh is None:
            return ngay_sinh
        
        if ngay_sinh > today:
            raise forms.ValidationError("không được lớn hơn ngày hiện tại.")
        if ngay_sinh.year < 1900:
            raise forms.ValidationError("không được nhỏ hơn năm 1900.")
        if ngay_sinh.year > 2002:
            raise forms.ValidationError("không được lớn hơn năm 2002.")
        
        return ngay_sinh
        
    