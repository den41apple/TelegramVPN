from django.views.generic import TemplateView
from .landing_data import products_data, faq_data


class LandingPageView(TemplateView):
    template_name = "landing_page/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"products_data": products_data,
                        "faq_data": faq_data})
        return context
