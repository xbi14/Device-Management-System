from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.db.models import F

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Phải có tên đăng nhập'))
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Yêu cầu 30 ký tự hoặc ít hơn. Chỉ chứa chữ cái, số và các ký tự @/./+/-/_'),
                                error_messages={
                                    'unique': _("Tên đăng nhập đã tồn tại."),
                                })
    ho = models.CharField(max_length=30, verbose_name='Họ')
    ten = models.CharField(max_length=30, verbose_name='Tên')
    
    GENDER_CHOICES = [
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ]
    gioi_tinh = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Chưa đặt giới tính', blank=True, null=True, verbose_name='Giới tính')
    
    USER_ROLES = [    ('quanly', 'Quản Lý'),    ('nhanvien', 'Nhân Viên'),    ('kythuatvien', 'Kỹ Thuật Viên'),]
    chuc_vu = models.CharField(choices=USER_ROLES, max_length=20, default='Chưa đặt chức vụ',verbose_name='Chức vụ')

    email = models.EmailField(verbose_name='Địa chỉ email', unique=True)
    sdt = models.CharField(max_length=10, null=True, blank=True, verbose_name='Số điện thoại')
    ngay_sinh = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    ngay_vao_lam = models.DateField(null=True, blank=True, verbose_name='Ngày vào làm')
    is_active = models.BooleanField(default=True, verbose_name='Đang làm việc')
    is_staff = models.BooleanField(default=False, verbose_name='Nhân viên quản lý')
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.ho} {self.ten}"

    def get_short_name(self):
        return self.ten

class BaseUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_nguoidung = models.CharField(max_length=10, primary_key=True, blank=True, null=False, unique=True, editable=False)
    class Meta:
        abstract = True 
        ordering = ['-id_nguoidung']
        
@receiver(post_save, sender=BaseUserProfile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'quanly':
            QuanLy.objects.create(user=instance)
        elif instance.role == 'nhanvien':
            NhanVien.objects.create(user=instance)
        elif instance.role == 'kythuatvien':
            KyThuatVien.objects.create(user=instance)

class QuanLy(BaseUserProfile):
    def save(self, *args, **kwargs):

        if not self.id_nguoidung:
            self.id_nguoidung = QuanLy.objects.aggregate(Max('id_nguoidung'))['id_nguoidung__max']
            if self.id_nguoidung:
                self.id_nguoidung = 'QL' + str(int(self.id_nguoidung[2:]) + 1).zfill(4)
            else:
                self.id_nguoidung = 'QL0001'
        super(QuanLy, self).save(*args, **kwargs)  
    
class NhanVien(BaseUserProfile):

    def save(self, *args, **kwargs):

        if not self.id_nguoidung:
            self.id_nguoidung = NhanVien.objects.aggregate(Max('id_nguoidung'))['id_nguoidung__max']
            if self.id_nguoidung:
                self.id_nguoidung = 'NV' + str(int(self.id_nguoidung[2:]) + 1).zfill(4)
            else:
                self.id_nguoidung = 'NV0001'
        super(NhanVien, self).save(*args, **kwargs)  
        
class KyThuatVien(BaseUserProfile):
    def save(self, *args, **kwargs):

        if not self.id_nguoidung:
            self.id_nguoidung = KyThuatVien.objects.aggregate(Max('id_nguoidung'))['id_nguoidung__max']
            if self.id_nguoidung:
                self.id_nguoidung = 'KTV' + str(int(self.id_nguoidung[2:]) + 1).zfill(4)
            else:
                self.id_nguoidung = 'KTV0001'
        super(KyThuatVien, self).save(*args, **kwargs)  
    
class Phong(models.Model):
    id_phong = models.CharField(max_length=10, primary_key=True, blank=True, null=False, unique=True, editable=False)
    ten_phong = models.CharField(max_length=30, verbose_name='Tên phòng')
    so_tang = models.IntegerField(verbose_name='Số tầng')
    class Meta:
        ordering = ['-id_phong']
    def save(self, *args, **kwargs):
        if not self.id_phong:
            self.id_phong = Phong.objects.aggregate(Max('id_phong'))['id_phong__max']
            if self.id_phong:
                self.id_phong = 'P' + str(int(self.id_phong[1:]) + 1).zfill(4)
            else:
                self.id_phong = 'P0001'
        super(Phong, self).save(*args, **kwargs)
    def __str__(self):
        return self.ten_phong
    
class LoaiThietBi(models.Model):
    id_loai_thiet_bi = models.CharField(max_length=10, primary_key=True, blank=True, null=False, unique=True, editable=False)
    ten_loai_thiet_bi = models.CharField(max_length=30, verbose_name='Tên loại thiết bị')
    class Meta:
        ordering = ['-id_loai_thiet_bi']
    def save(self, *args, **kwargs):
        if not self.id_loai_thiet_bi:
            self.id_loai_thiet_bi = LoaiThietBi.objects.aggregate(Max('id_loai_thiet_bi'))['id_loai_thiet_bi__max']
            if self.id_loai_thiet_bi:
                self.id_loai_thiet_bi = 'LTB' + str(int(self.id_loai_thiet_bi[3:]) + 1).zfill(4)
            else:
                self.id_loai_thiet_bi = 'LTB0001'
        super(LoaiThietBi, self).save(*args, **kwargs)
    def __str__(self):
        return self.ten_loai_thiet_bi
    
class ThietBi(models.Model):
    id_thiet_bi = models.CharField(max_length=10, primary_key=True, blank=True, null=False, unique=True, editable=False)
    ten_thiet_bi = models.CharField(max_length=30, verbose_name='Tên thiết bị')
    loai_thiet_bi = models.ForeignKey(LoaiThietBi, on_delete=models.CASCADE, verbose_name='Loại thiết bị') # Thiết bị điện, thiết bị y tế, thiết bị văn phòng,...
    phong = models.ForeignKey(Phong, on_delete=models.CASCADE, verbose_name='Phòng',)
    hinh_anh = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Hình ảnh')
    ngay_mua = models.DateField(verbose_name='Ngày mua')
    gia_mua = models.IntegerField(verbose_name='Giá mua')
    tinh_trang_choices = [
        ('hoatdong', 'Hoạt động'),
        ('dangbaotri', 'Đang bảo trì'),
        ('bihong', 'Bị hỏng'),
    ]
    tinh_trang = models.CharField(max_length=10, choices=tinh_trang_choices, default='hoatdong', verbose_name='Tình trạng')
    ngay_bao_tri = models.DateField(verbose_name='Ngày bảo trì',blank=True, null=True)
    mo_ta = models.TextField(verbose_name='Mô tả', blank=True, null=True)
    class Meta:
        ordering = ['-id_thiet_bi']
    
    def save(self, *args, **kwargs):
        if not self.id_thiet_bi:
            self.id_thiet_bi = ThietBi.objects.aggregate(Max('id_thiet_bi'))['id_thiet_bi__max']
            if self.id_thiet_bi:
                self.id_thiet_bi = 'TB' + str(int(self.id_thiet_bi[2:]) + 1).zfill(4)
            else:
                self.id_thiet_bi = 'TB0001'
        super(ThietBi, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.ten_thiet_bi

