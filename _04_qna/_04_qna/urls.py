from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qna/', include('qna.urls')),
    path('uauth/', include('uauth.urls')),
    path('', RedirectView.as_view(url='/qna/')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)