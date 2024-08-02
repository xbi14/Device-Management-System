from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Max
from django.db.models import F
from django.utils import timezone

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
                                },
                                null = False, blank = False,
                                )
    ho = models.CharField(max_length=30, verbose_name='Họ', blank=False, null=True)
    ten = models.CharField(max_length=30, verbose_name='Tên', blank=False, null=True)
    
    GENDER_CHOICES = [
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ]
    gioi_tinh = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Chưa đặt giới tính', blank=False, null=True, verbose_name='Giới tính')
    
    USER_ROLES = [('quanly', 'Quản Lý'),('kythuatvien', 'Kỹ Thuật Viên'),]
    chuc_vu = models.CharField(choices=USER_ROLES, max_length=20, default='Chưa đặt chức vụ',verbose_name='Chức vụ', blank=False, null=True)
    anh_the = models.ImageField(upload_to='anhthe/', blank=True, null=True, verbose_name='Ảnh thẻ')
    email = models.EmailField(verbose_name='Địa chỉ email', unique=True, null=False, blank=False)
    sdt = models.CharField(max_length=10, null=True, blank=True, verbose_name='Số điện thoại')
    dia_chi = models.CharField(max_length=100, null=True, blank=True, verbose_name='Địa chỉ')
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
    
    def in_chuc_vu(self):
        if self.chuc_vu == 'quanly':
            return f"Quản lý"
        elif self.chuc_vu == 'kythuatvien':
            return f"Kỹ thuật viên"
   
    class Meta:
        verbose_name_plural = 'Người dùng'

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
        
class KyThuatVien(BaseUserProfile):
    def save(self, *args, **kwargs):

        if not self.id_nguoidung:
            self.id_nguoidung = KyThuatVien.objects.aggregate(Max('id_nguoidung'))['id_nguoidung__max']
            if self.id_nguoidung:
                self.id_nguoidung = 'KTV' + str(int(self.id_nguoidung[2:]) + 1).zfill(4)
            else:
                self.id_nguoidung = 'KTV0001'
        super(KyThuatVien, self).save(*args, **kwargs)  
        
class Tang(models.Model):
    ten_tang = models.CharField(max_length=10,verbose_name='Số tầng')
    
    class meta:
        ordering = ['-ten_tang']
        verbose_name_plural = 'Tầng'
        
    def __str__(self):
        return self.ten_tang
    
class Phong(models.Model):
    tang = models.ForeignKey(Tang, on_delete=models.CASCADE, verbose_name='Tầng')
    ten_phong = models.CharField(max_length=30, verbose_name='Tên phòng')
    
    class Meta:
        ordering = ['-ten_phong']
        verbose_name_plural = 'Phòng'
        
    def __str__(self):
        return self.ten_phong
    
class LoaiThietBi(models.Model):
    ten_loaithietbi = models.CharField(max_length=30, verbose_name='Tên loại thiết bị')
    
    class Meta:
        ordering = ['-ten_loaithietbi']
        verbose_name_plural = 'Loại thiết bị'
        
    def __str__(self):
        return self.ten_loaithietbi
    
class ThietBi(models.Model):
    id_thiet_bi = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True, editable=False)
    ten_thiet_bi = models.CharField(max_length=30, verbose_name='Tên thiết bị', blank=False, null=True)
    loai_thiet_bi = models.ForeignKey(LoaiThietBi, on_delete=models.SET_NULL, null=True, verbose_name='Loại thiết bị')
    phong = models.ForeignKey(Phong, on_delete=models.SET_NULL, null=True,blank=False, verbose_name='Phòng')
    tang = models.ForeignKey(Tang, on_delete=models.SET_NULL, null=True,blank=False, verbose_name='Tầng')
    hinh_anh = models.ImageField(upload_to='anhthietbi/', blank=False, null=True, verbose_name='Hình ảnh')
    ngay_mua = models.DateField(verbose_name='Ngày mua')
    gia_mua = models.IntegerField(verbose_name='Giá mua')
    tinh_trang_choices = [
        ('hoatdong', 'Hoạt động'),
        ('dangbaotri', 'Đang bảo trì'),
        ('bihong', 'Bị hỏng'),
    ]
    tinh_trang = models.CharField(max_length=10, choices=tinh_trang_choices, default='hoatdong', verbose_name='Tình trạng', blank=False, null=True)
    ngay_bao_tri = models.DateField(verbose_name='Ngày bảo trì',blank=True, null=True)
    mo_ta = models.TextField(verbose_name='Mô tả', blank=True, null=True)
    don_vi_cung_cap = models.CharField(max_length=30, verbose_name='Đơn vị cung cấp', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Thiết bị'
    
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
    
class BaoCao(models.Model):
    tieu_de = models.CharField(max_length=30, verbose_name='Tiêu đề báo cáo')
    trang_thai_choices = [ 
        ('dangxuly', 'Đang xử lý'),
        ('daxuly', 'Đã xử lý'),
    ]
    trang_thai = models.CharField(max_length=10, choices=trang_thai_choices, default='dangxuly', verbose_name='Trạng thái')
    noi_dung = models.TextField(verbose_name='Nội dung')
    thiet_bi = models.ForeignKey(ThietBi, on_delete=models.SET_NULL, verbose_name='Thiết bị cần sửa chữa', null=True)
    ngay_bao_cao = models.DateField(verbose_name='Ngày báo cáo',default=timezone.now)
    nguoi_bao_cao = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Người báo cáo',related_name='bao_cao_nguoi_bao_cao')
    nguoi_nhan_bao_cao = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Người nhận báo cáo',related_name='bao_cao_nguoi_nhan_bao_cao')
    nguoi_hoan_thanh = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Người hoàn thành',related_name='bao_cao_nguoi_hoan_thanh')
    
    thiet_bi_disabled = models.ForeignKey(ThietBi, on_delete=models.SET_NULL, verbose_name='Thiết bị cần sửa chữa', null=True, blank=True, related_name='bao_cao_thiet_bi_disabled')
    ngay_bao_cao_disabled = models.DateField(verbose_name='Ngày báo cáo',default=timezone.now, null=True, blank=True)
    nguoi_bao_cao_disabled = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Người báo cáo',related_name='bao_cao_nguoi_bao_cao_disabled')
    
    class Meta:
        verbose_name_plural = 'Báo cáo'
    
    def __str__(self):
        return self.tieu_de


