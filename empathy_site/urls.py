from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('forum/', include('forum.urls')),
    #path('news/', include('news.urls')),
    path('article/', include('article.urls')),
    path('diary/', include('diary.urls')),
    #path('', include('users.urls')),
    path('admin/', admin.site.urls),
    #path('tinymce/', include('tinymce.urls')),
    #path('hitcount/', include('hitcount.urls',namespace='hitcount')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

