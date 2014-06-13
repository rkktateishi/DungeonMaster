#!/usr/bin/env python
import os
import sys

def here(*paths):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *paths))

if not hasattr(sys, 'real_prefix'):
    activate_this = here('bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here())
sys.path.insert(0, here('DungeonMaster'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
            "DungeonMaster.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
