from django.db import models

class UISettings(models.Model):
    theme = models.CharField(max_length=50, default="flatly")
    navbar = models.CharField(max_length=100, default="navbar-white navbar-light")
    sidebar = models.CharField(max_length=100, default="sidebar-light-primary")
    accent = models.CharField(max_length=50, default="accent-primary")
    brand_colour = models.CharField(max_length=50, default="navbar-primary")
    button_primary = models.CharField(max_length=50, default="btn-primary")
    button_secondary = models.CharField(max_length=50, default="btn-secondary")
    button_info = models.CharField(max_length=50, default="btn-info")
    button_warning = models.CharField(max_length=50, default="btn-warning")
    button_danger = models.CharField(max_length=50, default="btn-danger")
    button_success = models.CharField(max_length=50, default="btn-success")
    navbar_fixed = models.BooleanField(default=True)
    sidebar_fixed = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "UI Settings"
        verbose_name_plural = "UI Settings"

    def __str__(self):
        return f"UI Settings (theme: {self.theme})"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj