from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'QLthietbi_app'
urlpatterns = [
    path('dangnhap/', views.render_login, name='render_login'),
    path('login', views.perform_login, name='perform_login'),
    path('logout', views.perform_logout, name='perform_logout'),
    path('quanly/', views.ThietBi_view.as_view(), name='render_trangchinh'),
    path('tao_file.txt/', views.tao_file_txt, name='tao_file_txt'),
    path('tao_file.csv/', views.tao_file_csv, name='tao_file_csv'),
    path('vitri/', views.render_vitri_thietbi, name='render_vitri_thietbi'),
    path('xoa_loai_thiet_bi/<int:pk>', views.xoa_loai_thiet_bi, name='xoa_loai_thiet_bi'),
    path('xoa_phong/<int:pk>', views.xoa_phong, name='xoa_phong'),
    path('xoa_tang/<int:pk>', views.xoa_tang, name='xoa_tang'),
    path('them_loai_thiet_bi/', views.them_loai_thiet_bi, name='them_loai_thiet_bi'),
    path('them_phong/', views.them_phong, name='them_phong'),
    path('them_tang/', views.them_tang, name='them_tang'),
    path('taobaocao/<str:id_thiet_bi>', views.render_taobaocao, name='render_taobaocao'),
    path('baocao/', views.render_baocaolist, name='render_baocaolist'),
    path('xoabaocao/<int:pk>', views.xoa_baocao, name='xoabaocao'),
    path('chinhsuabaocao/<int:pk>', views.chinh_sua_baocao, name='chinhsua_baocao'),
    # -------------------------Kỹ thuật viên--------------------------------
    path('danhsachthietbi/', views.DanhSachThietBi_view.as_view(), name='render_danhsachthietbi'),
    path('danhsachbaocao/', views.render_baocaolist_ktv, name='render_baocaolist_ktv'),
    path('nhansua_baocao/<int:pk>', views.nhansua_baocao, name='nhansua_baocao'),
    path('baocao_danhan/', views.baocao_danhan, name='baocao_danhan'),
    path('hoanthanh_baocao/<int:pk>', views.hoanthanh_baocao, name='hoanthanh_baocao'),
    path('huynhan_baocao/<int:pk>', views.huynhan_baocao, name='huynhan_baocao'),
    path('khongthe_suachua/<int:pk>', views.khongthe_suachua, name='khongthe_suachua'),
    path('hosocanhan_ktv/<int:id>', views.hoso_user_ktv, name='hoso_user_ktv'),
    path('capnhapthongtin_ktv/<int:id>', views.capnhap_user_ktv, name='capnhap_user_ktv'),
    path('doimatkhau_ktv/', views.doi_matkhau_ktv, name='doi_matkhau_ktv'),
    # -------------------------Tài khoản------------------------------------
    path('hosocanhan/<int:id>', views.hoso_user, name='hoso_user'),
    path('taotaikhoan/', views.tao_user, name='tao_user'),
    path('danhsachtaikhoan/', views.hoso_list, name='hoso_list'),
    path('xoataikhoan/<int:id>', views.hoso_xoa, name='hoso_xoa'),
    path('chinhsuataikhoan/<int:id>', views.sua_user, name='sua_user'),
    path('doimatkhau/', views.doi_matkhau, name='doi_matkhau'),
    path('capnhapthongtin/<int:id>', views.capnhap_user, name='capnhap_user'),
    # ------------------------------Ajax------------------------------------
    path('themthietbi/', views.render_themthietbi, name='render_themthietbi'),
    path('<str:pk>/', views.render_capnhap, name='render_capnhap'), # cập nhập thông tin thiết bị lúc thay đổi phòng
    path('ajax/laythongtinphong/', views.load_phong, name='ajax_load_phong'),
    
    path('ktvthietbi/<str:id_thiet_bi>', views.render_chitietthietbi_ktv, name='render_chitietthietbi_ktv'),
    path('thietbi/<str:id_thiet_bi>', views.render_chitietthietbi, name='render_chitietthietbi'),
    path('chinhsuathietbi/<str:id_thiet_bi>', views.render_chinhsuathietbi, name='render_chinhsuathietbi'),
    path('xoathietbi/<str:id_thiet_bi>', views.render_xoathietbi, name='render_xoathietbi'),
    path('xoanhieu/', views.ThietBi_view.as_view(), name='xoa_nhieu'),
    
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
