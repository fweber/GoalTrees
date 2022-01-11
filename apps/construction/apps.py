from django.apps import AppConfig


class ConstructionConfig(AppConfig):
    name = 'apps.construction'

    def ready(self):
        # initialize studies at startup
        from apps.construction.studies import study_functions
        study_functions.initialize_studies()