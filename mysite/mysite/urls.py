from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('handaioh_NLP/', include('handaioh_NLP.urls')),
    path('admin/', admin.site.urls),
]