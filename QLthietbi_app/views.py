from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import csv
import io
from .filters import ThietBiFilter
from django.template import loader
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

def is_quanly(user):
    return user.chuc_vu == 'quanly'

def is_kythuatvien(user):
    return user.chuc_vu == 'kythuatvien'

def tao_file_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="thietbi.txt"'
    listThietBi = ThietBi.objects.all()
    lines = []
    for thietbi in listThietBi:
        ngay_mua = thietbi.ngay_mua.strftime('%d/%m/%Y') if thietbi.ngay_mua else ''
        ngay_bao_tri = thietbi.ngay_bao_tri.strftime('%d/%m/%Y') if thietbi.ngay_bao_tri else ''
        lines.append(f'Tên thiết bị: {thietbi.ten_thiet_bi}\n'
                     f'Loại thiết bị: {thietbi.loai_thiet_bi.ten_loaithietbi}\n'
                     f'Phòng: {thietbi.phong.ten_phong}\n'
                     f'Tầng: {thietbi.tang.ten_tang}\n'
                     f'Ngày mua: {ngay_mua}\n'
                     f'Giá mua: {thietbi.gia_mua}\n'
                     f'Tình trạng: {thietbi.tinh_trang}\n'
                     f'Ngày bảo trì: {ngay_bao_tri}\n'
                     f'Mô tả: {thietbi.mo_ta}\n\n')
    response.writelines(lines)
    return response

def tao_file_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="thietbi.csv"'

    listThietBi = ThietBi.objects.all()

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Tên thiết bị', 'Loại thiết bị', 'Phòng', 'Tầng', 'Ngày mua', 'Giá mua', 'Tình trạng', 'Ngày bảo trì', 'Mô tả'])

    for thietbi in listThietBi:
        ngay_mua = thietbi.ngay_mua.strftime('%d/%m/%Y') if thietbi.ngay_mua else ''
        ngay_bao_tri = thietbi.ngay_bao_tri.strftime('%d/%m/%Y') if thietbi.ngay_bao_tri else ''
        writer.writerow([
            thietbi.ten_thiet_bi,
            thietbi.loai_thiet_bi.ten_loaithietbi,
            thietbi.phong.ten_phong,
            thietbi.tang.ten_tang,
            ngay_mua,
            thietbi.gia_mua,
            thietbi.tinh_trang,
            ngay_bao_tri,
            thietbi.mo_ta
        ])

    csv_buffer.seek(0)
    response.write(csv_buffer.getvalue().encode('utf-8-sig'))

    return response

def render_login(request):
    return render(request, 'dangnhap.html')

def perform_login(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')
        
        if remember_me == 'on':
            request.session.set_expiry(1209600)
        
        if not username or not password:
            messages.error(request, "Vui lòng nhập tên tài khoản và mật khẩu!")
            return HttpResponseRedirect('/')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.chuc_vu == 'quanly':
                return redirect('quanly/')
            elif user.chuc_vu == 'kythuatvien':
                return redirect('danhsachthietbi/')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại!")
            return HttpResponseRedirect('/')
        
def perform_logout(requet):
    return HttpResponseRedirect('/')

@method_decorator(user_passes_test(is_quanly), name='dispatch')
class ThietBi_view(ListView, FormView):
    template_name = "quanly.html"
    model = ThietBi
    form_class = ThemThietBiForm
    success_url = reverse_lazy("QLthietbi_app:render_trangchinh")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listThietBi = self.get_queryset()
        myFilter = ThietBiFilter(self.request.GET, queryset=listThietBi)
        context['listThietBi'] = myFilter.qs
        context['myFilter'] = myFilter
        context['form'] = ThemThietBiForm()
        return context

    def post(self, request):
        selected_rows = request.POST.getlist('selectedItems[]')
        for id in selected_rows:
            thietbi = ThietBi.objects.get(pk=id)
            thietbi.delete()
        return redirect(self.success_url)

def render_themthietbi(request):
    form_error = False
    listThietBi = ThietBi.objects.all()
    myFilter = ThietBiFilter(request.GET, queryset=listThietBi)
    listThietBi = myFilter.qs
    form = ThemThietBiForm()
    if request.method == "POST":
        form = ThemThietBiForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('QLthietbi_app:render_trangchinh')
        else:
            form_error = True
    return render(request,"themtb.html", {'form': form, 'form_error': form_error, 'listThietBi': listThietBi, 'myFilter': myFilter})

def render_capnhap(request, pk):
    thietbi = get_object_or_404(ThietBi, pk=pk)
    form = ThemThietBiForm(instance=thietbi)
    if request.method == "POST":
        form = ThemThietBiForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('QLthietbi_app:render_trangchinh')
    return render(request,"themtb.html", {'form': form}) 

def render_chinhsuathietbi(request, id_thiet_bi):
    listThietBi = ThietBi.objects.all()
    myFilter = ThietBiFilter(request.GET, queryset=listThietBi)
    listThietBi = myFilter.qs
    pk = id_thiet_bi
    thietbi = ThietBi.objects.get(id_thiet_bi=id_thiet_bi)
    form = ThemThietBiForm(instance=thietbi)
    if request.method == "POST":
        form = ThemThietBiForm(request.POST,request.FILES,instance=thietbi)
        if form.is_valid():
            form.save()
            return redirect('QLthietbi_app:render_trangchinh')
    return render(request,"chinhsuatb.html",{'listThietBi': listThietBi, 'myFilter': myFilter, 'form': form, 'pk': pk})
        
# AJAX
def load_phong(request):
    tang_id = request.GET.get('tang_id')
    listPhong = Phong.objects.filter(tang_id=tang_id).order_by('ten_phong')
    return render(request, 'phong_dropdown_list_options.html', {'listPhong': listPhong})

def render_chitietthietbi(request, id_thiet_bi):
    form_error = False
    pk = id_thiet_bi
    thietbi = ThietBi.objects.get(id_thiet_bi=id_thiet_bi)
    gia_mua_str = "{:,.0f}".format(thietbi.gia_mua)
    ngay_mua_str = thietbi.ngay_mua.strftime('%d/%m/%Y') if thietbi.ngay_mua else 'Không có dữ liệu'
    ngay_bao_tri_str = thietbi.ngay_bao_tri.strftime('%d/%m/%Y') if thietbi.ngay_bao_tri else 'Chưa bảo trì'
    form = ThemThietBiForm(instance=thietbi)
    if request.method == "POST":
        form = ThemThietBiForm(request.POST,request.FILES,instance=thietbi)
        if form.is_valid():
            form.save()
            return redirect('QLthietbi_app:render_chitietthietbi', id_thiet_bi)
        else:
            form_error = True
    return render(request,"chitiettb.html", {'thietbi': thietbi, 'pk': pk, 'gia_mua_str': gia_mua_str, 'ngay_mua_str': ngay_mua_str,'ngay_bao_tri_str': ngay_bao_tri_str, 'form': form, 'form_error': form_error})

def render_xoathietbi(request, id_thiet_bi):
    thietbi = ThietBi.objects.get(id_thiet_bi=id_thiet_bi)
    thietbi.delete()
    return redirect('QLthietbi_app:render_trangchinh')

@csrf_exempt
def render_xoanhieutthietbi(request):
    if request.method == "POST":
        selected_rows = request.POST.getlist('list')
        for id in selected_rows:
            thietbi = ThietBi.objects.get(id_thiet_bi=id)
            thietbi.delete()
    return redirect('QLthietbi_app:render_trangchinh')

def render_vitri_thietbi(request):
    listPhong = Phong.objects.all()
    listTang = Tang.objects.all()
    listLoaiThietBi = LoaiThietBi.objects.all()
    ThietBiCount = ThietBi.objects.all().count()
    LoaiForm = LoaiThietBiForm()
    Phongform = PhongForm()
    Tangform = TangForm()
    return render(request, 'vitri_thietbi.html', {'listPhong': listPhong, 'listTang': listTang, 'listLoaiThietBi': listLoaiThietBi, 'ThietBiCount': ThietBiCount, 'LoaiForm': LoaiForm, 'Phongform': Phongform, 'Tangform': Tangform})

def them_loai_thiet_bi(request):
    if request.method == "POST":
        LoaiForm = LoaiThietBiForm(request.POST)
        if LoaiForm.is_valid():
            LoaiForm.save()
            return redirect('QLthietbi_app:render_vitri_thietbi')

def them_phong(request):
    if request.method == "POST":
        Phongform = PhongForm(request.POST)
        if Phongform.is_valid():
            Phongform.save()
            return redirect('QLthietbi_app:render_vitri_thietbi')

def them_tang(request):
    if request.method == "POST":
        Tangform = TangForm(request.POST)
        if Tangform.is_valid():
            Tangform.save()
            return redirect('QLthietbi_app:render_vitri_thietbi')

def xoa_loai_thiet_bi(request, pk):
    loai_thiet_bi = LoaiThietBi.objects.get(pk=pk)
    loai_thiet_bi.delete()
    return redirect('QLthietbi_app:render_vitri_thietbi')

def xoa_phong(request, pk):
    phong = Phong.objects.get(pk=pk)
    phong.delete()
    return redirect('QLthietbi_app:render_vitri_thietbi')

def xoa_tang(request, pk):
    tang = Tang.objects.get(pk=pk)
    tang.delete()
    return redirect('QLthietbi_app:render_vitri_thietbi')

def render_taobaocao(request, id_thiet_bi):
    pk = id_thiet_bi 
    if request.method == "POST":
        baoCaoForm = BaoCaoForm(request.POST)
        if baoCaoForm.is_valid():
            baoCao = baoCaoForm.save(commit=False)
            baoCao.thiet_bi_id = id_thiet_bi
            baoCao.nguoi_bao_cao = request.user
            baoCao.ngay_bao_cao = datetime.now()
            
            baoCao.thiet_bi_id_disabled = id_thiet_bi
            baoCao.nguoi_bao_cao_disabled = request.user
            baoCao.ngay_bao_cao_disabled = datetime.now()
            
            # Thay đổi trạng thái thiết bị thành "bị hỏng"
            thiet_bi = ThietBi.objects.get(pk=id_thiet_bi)
            thiet_bi.tinh_trang = 'bihong'
            thiet_bi.save()
            baoCao.save()
            return redirect('QLthietbi_app:render_baocaolist')
    else:
        initial_data = {
            'thiet_bi': id_thiet_bi,
            'nguoi_bao_cao': request.user,
            'ngay_bao_cao': datetime.now().date(),
            
            'thiet_bi_disabled': id_thiet_bi,
            'nguoi_bao_cao_disabled': request.user,
            'ngay_bao_cao_disabled': datetime.now(),
        }
        baoCaoForm = BaoCaoForm(initial=initial_data)
        baoCaoForm.fields['thiet_bi'].widget = forms.HiddenInput()
        baoCaoForm.fields['nguoi_bao_cao'].widget = forms.HiddenInput()
        baoCaoForm.fields['ngay_bao_cao'].widget = forms.HiddenInput()
        
        baoCaoForm.fields['thiet_bi'].widget.attrs['readonly'] = True
        baoCaoForm.fields['nguoi_bao_cao'].widget.attrs['readonly'] = True
        baoCaoForm.fields['ngay_bao_cao'].widget.attrs['readonly'] = True
        
        baoCaoForm.fields['thiet_bi_disabled'].widget.attrs['disabled'] = True
        baoCaoForm.fields['nguoi_bao_cao_disabled'].widget.attrs['disabled'] = True
        baoCaoForm.fields['ngay_bao_cao_disabled'].widget.attrs['disabled'] = True
    
    return render(request, 'taobaocao.html', {'baoCaoForm': baoCaoForm, 'pk': pk})

def render_baocaolist(request):
    listBaoCao = BaoCao.objects.all()
    return render(request, 'baocaolist.html', {'listBaoCao': listBaoCao})

def xoa_baocao(request, pk):
    baoCao = BaoCao.objects.get(pk=pk)
    thietBi = baoCao.thiet_bi
    thietBi.tinh_trang = 'hoatdong'
    thietBi.save()
    baoCao.delete()
    return redirect('QLthietbi_app:render_baocaolist')

def chinh_sua_baocao(request, pk):
    baoCao = BaoCao.objects.get(pk=pk)
    baoCaoForm = BaoCaoForm(instance=baoCao)
    if request.method == "POST":
        baoCaoForm = BaoCaoForm(request.POST, instance=baoCao)
        if baoCaoForm.is_valid():
            baoCaoForm.save()
            return redirect('QLthietbi_app:render_baocaolist')
    return render(request, 'chinhsua_baocao.html', {'baoCaoForm': baoCaoForm})

# -------------------------Kỹ thuật viên--------------------------------
class DanhSachThietBi_view(ListView):
    template_name = "ktv/ds_thietbi.html"
    model = ThietBi
    success_url = reverse_lazy("QLthietbi_app:render_danhsachthietbi")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listThietBi = self.get_queryset()
        myFilter = ThietBiFilter(self.request.GET, queryset=listThietBi)
        baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao =self.request.user).count()
        context['listThietBi'] = myFilter.qs
        context['myFilter'] = myFilter
        context['baoCaoCount'] = baoCaoCount
        return context
    
def render_baocaolist_ktv(request):
    listBaoCao = BaoCao.objects.all()
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    return render(request, 'ktv/baocaolist_ktv.html', {'listBaoCao': listBaoCao, 'baoCaoCount': baoCaoCount})

def nhansua_baocao(request,pk):
    baoCao = BaoCao.objects.get(pk=pk)
    baoCao.nguoi_nhan_bao_cao = request.user
    thietBi = baoCao.thiet_bi
    thietBi.tinh_trang = 'dangbaotri'
    thietBi.save()
    baoCao.save()
    return redirect('QLthietbi_app:baocao_danhan')

def baocao_danhan(request):
    listBaoCao = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user)
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    return render(request, 'ktv/baocao_danhan.html', {'listBaoCao': listBaoCao, 'baoCaoCount': baoCaoCount})

def hoanthanh_baocao(request,pk):
    baoCao = BaoCao.objects.get(pk=pk)
    baoCao.trang_thai = 'daxuly'
    baoCao.nguoi_nhan_bao_cao = None
    baoCao.nguoi_hoan_thanh = request.user
    thietBi = baoCao.thiet_bi
    thietBi.tinh_trang = 'hoatdong'
    thietBi.ngay_bao_tri = datetime.now()
    thietBi.save()
    baoCao.save()
    return redirect('QLthietbi_app:baocao_danhan')

def huynhan_baocao(request,pk):
    baoCao = BaoCao.objects.get(pk=pk)
    baoCao.trang_thai = 'chuaxuly'
    baoCao.nguoi_nhan_bao_cao = None
    thietBi = baoCao.thiet_bi
    thietBi.tinh_trang = 'bihong'
    thietBi.save()
    baoCao.save()
    return redirect('QLthietbi_app:baocao_danhan')

def khongthe_suachua(request,pk):
    baoCao = BaoCao.objects.get(pk=pk)
    baoCao.trang_thai = 'daxuly'
    thietBi = baoCao.thiet_bi
    thietBi.tinh_trang = 'bihong'
    baoCao.nguoi_nhan_bao_cao = None
    baoCao.nguoi_hoan_thanh = request.user
    thietBi.save()
    baoCao.save()
    return redirect('QLthietbi_app:render_baocaolist_ktv')

def render_chitietthietbi_ktv(request, id_thiet_bi):
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    form_error = False
    pk = id_thiet_bi
    thietbi = ThietBi.objects.get(id_thiet_bi=id_thiet_bi)
    gia_mua_str = "{:,.0f}".format(thietbi.gia_mua)
    ngay_mua_str = thietbi.ngay_mua.strftime('%d/%m/%Y') if thietbi.ngay_mua else 'Không có dữ liệu'
    ngay_bao_tri_str = thietbi.ngay_bao_tri.strftime('%d/%m/%Y') if thietbi.ngay_bao_tri else 'Chưa bảo trì'
    form = ThemThietBiForm(instance=thietbi)
    if request.method == "POST":
        form = ThemThietBiForm(request.POST,request.FILES,instance=thietbi)
        if form.is_valid():
            form.save()
            return redirect('QLthietbi_app:render_chitietthietbi_ktv', id_thiet_bi)
        else:
            form_error = True
    return render(request,"ktv/chitiettb_ktv.html", {'thietbi': thietbi, 'pk': pk, 'gia_mua_str': gia_mua_str, 'ngay_mua_str': ngay_mua_str,'ngay_bao_tri_str': ngay_bao_tri_str, 'form': form, 'form_error': form_error, 'baoCaoCount': baoCaoCount})

def hoso_user_ktv(request, id):
    user = get_object_or_404(CustomUser, id=id)
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    if request.method == 'POST':
        form = HoSoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('QLthietbi_app:hoso_user_ktv')
    else:
        form = HoSoForm(instance=user)
    
    return render(request, 'ktv/hoso_user_ktv.html', {'form': form, 'baoCaoCount': baoCaoCount})

def capnhap_user_ktv(request, id):
    user = get_object_or_404(CustomUser, id=id)
    success = False
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    if request.method == 'POST':
        form = SuaHoSoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            success = True
            return render(request, 'ktv/capnhap_user_ktv.html', {'form': form, 'success': success})
    else:
        form = SuaHoSoForm(instance=user)
    
    return render(request, 'ktv/capnhap_user_ktv.html', {'form': form, 'success': success, 'baoCaoCount': baoCaoCount})

def doi_matkhau_ktv(request):
    user = request.user
    success = False
    baoCaoCount = BaoCao.objects.filter(nguoi_nhan_bao_cao = request.user).count()
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            success = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'ktv/doi_matkhau_ktv.html', {'form': form, 'success': success})
    else:
        form = ChangePasswordForm(user)

    return render(request, 'ktv/doi_matkhau_ktv.html', {'form': form, 'success': success, 'baoCaoCount': baoCaoCount})
# -------------------------------Hồ Sơ----------------------------------
def tao_user(request):
    
    if request.method == 'POST':
        form = HoSoForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = request.POST['password']
            user.set_password(password)
            user.save()

            
            if user.chuc_vu == 'quanly':
                user.is_staff = True
                user.is_superuser = True
                password = request.POST['password']
                user.set_password(password)
                user.save()
            
            return redirect('QLthietbi_app:hoso_list')
    else:
        form = HoSoForm()
    
    return render(request, 'tao_user.html', {'form': form})

def hoso_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    
    if request.method == 'POST':
        form = HoSoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('QLthietbi_app:hoso_user')
    else:
        form = HoSoForm(instance=user)
    
    return render(request, 'hoso_user.html', {'form': form})

def capnhap_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    success = False
    if request.method == 'POST':
        form = SuaHoSoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            success = True
            return render(request, 'capnhap_user.html', {'form': form, 'success': success})
    else:
        form = SuaHoSoForm(instance=user)
    
    return render(request, 'capnhap_user.html', {'form': form, 'success': success})

def hoso_list(request):
    listUser = CustomUser.objects.all()
    return render(request, 'taikhoan_list.html', {'listUser': listUser})

def hoso_xoa(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return redirect('QLthietbi_app:hoso_list')

def sua_user(request, id):
    pk = id
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = HoSoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = request.POST['password']
            user.set_password(password)
            form.save()
            
            if user.chuc_vu == 'quanly':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                    
            elif user.chuc_vu == 'kythuatvien':
                user.is_staff = False
                user.is_superuser = False
                user.save()
            
            return redirect('QLthietbi_app:hoso_list')
    else:
        form = HoSoForm(instance=user)

    return render(request, 'sua_user.html', {'form': form, 'pk': pk})

from django.contrib.auth import login
        
def doi_matkhau(request):
    user = request.user
    success = False

    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            success = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'doi_matkhau.html', {'form': form, 'success': success})
    else:
        form = ChangePasswordForm(user)

    return render(request, 'doi_matkhau.html', {'form': form, 'success': success})