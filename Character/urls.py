from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from .views import CharacterCreateView

urlpatterns = [
    url(r'^character/create/$', CharacterCreateView.as_view(), name='create_character'),
]
