# backend/jazzmin_settings.py

# backend/jazzmin_settings.py

JAZZMIN_SETTINGS = {
    "site_title": "Bubble Curtain Admin",
    "site_header": "AI-Enhanced Bubble Curtain System",
    "site_brand": "BubbleCurtain",
    "welcome_sign": "Welcome to the Bubble Curtain Monitoring System",
    "copyright": "AI-Enhanced Bubble Curtain System",

    "topmenu_links": [
        {"name": "Administrator Page", "url": "admin:index"},
        {"name": "View Site", "url": "/"},
        {"name": "⚙️ UI Settings", "url": "/admin/ui-settings/"},
    ],

    "icons": {
        "accounts.CustomUser": "fas fa-users",
        "api.Device": "fas fa-microchip",
        "api.Signal": "fas fa-chart-line",
        "imaging.RawImage": "fas fa-camera",
        "imaging.ClassificationResult": "fas fa-robot",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "custom_css": "admin/css/theme_toggle.css",   
    "custom_js": "admin/js/theme_toggle.js",       
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
}                                                  
