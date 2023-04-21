"""APP about views"""
from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    """returns 'about' page"""

    template_name = 'about/index.html'
