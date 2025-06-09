from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = 'Каталог микроорганизмов'
    
    def ready(self):
        # Настройка админки
        from django.contrib import admin
        from django.conf import settings
        
        admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'СИФИБР СО РАН')
        admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'СИФИБР Админ')
        admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Управление коллекциями')
