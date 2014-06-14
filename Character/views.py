from django.views.generic import CreateView

from .models import Character

class CharacterCreateView(CreateView):
    model=Character
