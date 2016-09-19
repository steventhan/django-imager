from django.apps import AppConfig


class ImagerImagesConfig(AppConfig):
    name = 'imager_images'

    def ready(self):
        """Code to run when the app is ready"""
        from imager_images import handlers
