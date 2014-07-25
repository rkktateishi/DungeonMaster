from django.views.generic import CreateView

from .models import *


class CharacterCreateView(CreateView):
    model=Character
    template_name='Character/Character/create_character.html'
    
