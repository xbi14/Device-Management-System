from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'QLthietbi_app'
urlpatterns = [
    path('login/', views.render_login, name='render_login'),
    path('login', views.perform_login, name='perform_login'),
    path('logout', views.perform_logout, name='perform_logout'),
    path('quanly/', views.render_trangchinh, name='render_trangchinh'),
    path('quanly/', views.render_deletethietbi, name='render_delete'),
    path('themthietbi/', views.render_themthietbi, name='render_themthietbi'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)