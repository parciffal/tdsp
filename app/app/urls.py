from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import generate_resized_image


urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/creative/<id>', generate_resized_image, name='resized-image'),
    path('', include('api.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
