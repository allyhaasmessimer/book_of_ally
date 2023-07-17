from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, get_csrf_token, subscribe, create_blog

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('subscribe/', subscribe, name='subscribe'),
    path('create-blog/', create_blog, name='create_blog'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
