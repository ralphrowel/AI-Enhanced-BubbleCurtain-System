from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UISettings

THEME_CHOICES = [
    ("flatly", "Flatly (Light)"),
    ("lumen", "Lumen (Light)"),
    ("minty", "Minty (Light)"),
    ("lux", "Lux (Light)"),
    ("united", "United (Light)"),
    ("yeti", "Yeti (Light)"),
    ("darkly", "Darkly (Dark)"),
    ("cyborg", "Cyborg (Dark)"),
    ("slate", "Slate (Dark)"),
    ("superhero", "Superhero (Dark)"),
    ("solar", "Solar (Dark)"),
]

NAVBAR_CHOICES = [
    ("navbar-white navbar-light", "White (Light)"),
    ("navbar-light", "Light Gray"),
    ("navbar-dark navbar-primary", "Primary (Dark)"),
    ("navbar-dark navbar-secondary", "Secondary (Dark)"),
    ("navbar-dark navbar-info", "Info (Dark)"),
    ("navbar-dark navbar-success", "Success (Dark)"),
    ("navbar-dark navbar-danger", "Danger (Dark)"),
    ("navbar-dark navbar-warning", "Warning (Dark)"),
    ("navbar-dark navbar-dark", "Dark"),
]

SIDEBAR_CHOICES = [
    ("sidebar-light-primary", "Light Primary"),
    ("sidebar-light-secondary", "Light Secondary"),
    ("sidebar-light-info", "Light Info"),
    ("sidebar-light-success", "Light Success"),
    ("sidebar-light-danger", "Light Danger"),
    ("sidebar-light-warning", "Light Warning"),
    ("sidebar-dark-primary", "Dark Primary"),
    ("sidebar-dark-secondary", "Dark Secondary"),
    ("sidebar-dark-info", "Dark Info"),
    ("sidebar-dark-success", "Dark Success"),
    ("sidebar-dark-danger", "Dark Danger"),
    ("sidebar-dark-warning", "Dark Warning"),
]

ACCENT_CHOICES = [
    ("accent-primary", "Primary"),
    ("accent-secondary", "Secondary"),
    ("accent-info", "Info"),
    ("accent-success", "Success"),
    ("accent-danger", "Danger"),
    ("accent-warning", "Warning"),
]

BUTTON_CHOICES = [
    ("btn-primary", "Primary"),
    ("btn-secondary", "Secondary"),
    ("btn-info", "Info"),
    ("btn-success", "Success"),
    ("btn-danger", "Danger"),
    ("btn-warning", "Warning"),
    ("btn-outline-primary", "Outline Primary"),
    ("btn-outline-secondary", "Outline Secondary"),
]

BUTTON_NAMES = ["primary", "secondary", "info", "warning", "danger", "success"]

@staff_member_required
def ui_settings_view(request):
    ui = UISettings.get_settings()

    if request.method == "POST":
        ui.theme = request.POST.get("theme", ui.theme)
        ui.navbar = request.POST.get("navbar", ui.navbar)
        ui.sidebar = request.POST.get("sidebar", ui.sidebar)
        ui.accent = request.POST.get("accent", ui.accent)
        ui.brand_colour = request.POST.get("brand_colour", ui.brand_colour)
        ui.button_primary = request.POST.get("button_primary", ui.button_primary)
        ui.button_secondary = request.POST.get("button_secondary", ui.button_secondary)
        ui.button_info = request.POST.get("button_info", ui.button_info)
        ui.button_warning = request.POST.get("button_warning", ui.button_warning)
        ui.button_danger = request.POST.get("button_danger", ui.button_danger)
        ui.button_success = request.POST.get("button_success", ui.button_success)
        ui.navbar_fixed = request.POST.get("navbar_fixed") == "on"
        ui.sidebar_fixed = request.POST.get("sidebar_fixed") == "on"
        ui.save()
        messages.success(request, "UI Settings saved successfully!")
        return redirect("admin_ui_settings")

    # ✅ Pre-build button rows so template needs no custom filters
    button_fields = [
        {"name": "primary",   "current": ui.button_primary},
        {"name": "secondary", "current": ui.button_secondary},
        {"name": "info",      "current": ui.button_info},
        {"name": "warning",   "current": ui.button_warning},
        {"name": "danger",    "current": ui.button_danger},
        {"name": "success",   "current": ui.button_success},
    ]

    context = {
        "ui": ui,
        "theme_choices": THEME_CHOICES,
        "navbar_choices": NAVBAR_CHOICES,
        "sidebar_choices": SIDEBAR_CHOICES,
        "accent_choices": ACCENT_CHOICES,
        "button_choices": BUTTON_CHOICES,
        "button_fields": button_fields,
        "title": "UI Settings",
    }
    return render(request, "admin/ui_settings.html", context)