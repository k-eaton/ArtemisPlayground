from django.apps import AppConfig


class ShareConfig(AppConfig):
    name = 'share'

    def ready(self):
        import share.signals

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
