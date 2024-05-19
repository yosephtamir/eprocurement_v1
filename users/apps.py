#!/usr/bin/python3
'''Applications associated to the user'''
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    #used to make the signal functional
    def ready(self):
        import users.signals