from .models import UISettings

class JazzminUIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            try:
                ui = UISettings.get_settings()
                from django.conf import settings
                print(">>> THEME FROM DB:", ui.theme)
                print(">>> CURRENT TWEAKS:", settings.JAZZMIN_UI_TWEAKS)
                settings.JAZZMIN_SETTINGS.update({
                    "theme": ui.theme,
                    "navbar": ui.navbar,
                    "sidebar": ui.sidebar,
                    "accent": ui.accent,
                    "brand_colour": ui.brand_colour,
                    "navbar_fixed": ui.navbar_fixed,
                    "sidebar_fixed": ui.sidebar_fixed,
                })
                settings.JAZZMIN_UI_TWEAKS = {
                    "theme": ui.theme,
                    "navbar": ui.navbar,
                    "sidebar": ui.sidebar,
                    "accent": ui.accent,
                    "brand_colour": ui.brand_colour,
                    "navbar_fixed": ui.navbar_fixed,
                    "sidebar_fixed": ui.sidebar_fixed,
                }
                print(">>> TWEAKS AFTER UPDATE:", settings.JAZZMIN_UI_TWEAKS)
            except Exception as e:
                print(">>> MIDDLEWARE ERROR:", e)
        return self.get_response(request)