from django.utils.translation import gettext_lazy as _
from feincms.module.page.models import Page

from feincms_button.contents import ButtonContent

Page.register_templates(
    {
        "title": _("Standard template"),
        "path": "base.html",
        "regions": (("main", "Main content area"),),
    }
)
PageButtonContent = Page.create_content_type(ButtonContent)
