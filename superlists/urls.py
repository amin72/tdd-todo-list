from django.contrib import admin
from django.urls import path, include
from lists.views import home_page


urlpatterns = [
    path('admin/', admin.site.urls),

    path('lists/', include('lists.urls')),
    path('', home_page, name='home_page'),
]
