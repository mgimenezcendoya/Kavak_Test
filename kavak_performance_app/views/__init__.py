# Views module

from .ceo_dashboard import render_ceo_dashboard
from .city_manager_dashboard import render_city_manager_dashboard
from .customer_profile import render_customer_profile
from .kavako_dashboard import render_kavako_dashboard
from .login import render_login_page

__all__ = [
    "render_login_page",
    "render_ceo_dashboard",
    "render_city_manager_dashboard",
    "render_kavako_dashboard",
    "render_customer_profile",
]
