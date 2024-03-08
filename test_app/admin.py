from django.contrib import admin
from test_app.models import Category
from functools import partial, update_wrapper


import copy
import json
import re
from functools import partial, update_wrapper
from urllib.parse import quote as urlquote

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin import helpers, widgets
from django.contrib.admin.checks import (
    BaseModelAdminChecks,
    InlineModelAdminChecks,
    ModelAdminChecks,
)
from django.contrib.admin.decorators import display
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (
    NestedObjects,
    construct_change_message,
    flatten_fieldsets,
    get_deleted_objects,
    lookup_spawns_duplicates,
    model_format_dict,
    model_ngettext,
    quote,
    unquote,
)
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from django.contrib.auth import get_permission_codename
from django.core.exceptions import (
    FieldDoesNotExist,
    FieldError,
    PermissionDenied,
    ValidationError,
)
from django.core.paginator import Paginator
from django.db import models, router, transaction
from django.db.models.constants import LOOKUP_SEP
from django.forms.formsets import DELETION_FIELD_NAME, all_valid
from django.forms.models import (
    BaseInlineFormSet,
    inlineformset_factory,
    modelform_defines_fields,
    modelform_factory,
    modelformset_factory,
)
from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.text import (
    capfirst,
    format_lazy,
    get_text_list,
    smart_split,
    unescape_string_literal,
)
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView


def get_content_type_for_model(obj):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.
    from django.contrib.contenttypes.models import ContentType

    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'preview_link')
    # change_list_template = 'admin/test_app/change_list.html'
    change_form_template = 'admin/test_app/change_form.html'


    def preview_link(self, obj):
        url = reverse('admin:%s_%s_preview' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        print(url)
        return mark_safe(f'<a href={url}>LINK</a>')

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.opts.app_label, self.opts.model_name
        return [
            path(
                "<path:object_id>/preview/",
                wrap(self.preview_view),
                name="%s_%s_preview" % info,
            ),
            *super().get_urls(),

        ]

    def preview_view(self, request, object_id, extra_context=None):
        "The 'history' admin view for this model."
        from django.contrib.admin.models import LogEntry
        from django.contrib.admin.views.main import PAGE_VAR

        # First check if the user can see this history.
        model = self.model
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(
                request, model._meta, object_id
            )

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied

        # Then get the history for this object.
        # app_label = self.opts.app_label
        # action_list = (
        #     LogEntry.objects.filter(
        #         object_id=unquote(object_id),
        #         content_type=get_content_type_for_model(model),
        #     )
        #     .select_related()
        #     .order_by("action_time")
        # )

        # paginator = self.get_paginator(request, action_list, 100)
        # page_number = request.GET.get(PAGE_VAR, 1)
        # page_obj = paginator.get_page(page_number)
        # page_range = paginator.get_elided_page_range(page_obj.number)
        children_categories = Category.objects.get(id=object_id).category_parent.all()

        print(self.opts.model_name)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Tree object: %s") % obj,
            # "action_list": page_obj,
            # "page_range": page_range,
            # "page_var": PAGE_VAR,
            # "pagination_required": paginator.count > 100,
            "children_categories": children_categories,
            "module_name": str(capfirst(self.opts.verbose_name_plural)),
            "object": obj,
            "opts": self.opts,
            # "preserved_filters": self.get_preserved_filters(request),
            **(extra_context or {}),
        }
        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            'admin/test_app/preview.html',
            context,
        )

    @property
    def urls(self):
        return self.get_urls()


