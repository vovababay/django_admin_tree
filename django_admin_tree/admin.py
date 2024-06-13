from functools import update_wrapper
from django.contrib.admin.utils import unquote
from django.core.exceptions import (
    PermissionDenied,
)
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.text import capfirst
from django.utils.translation import gettext as _


class TreeParentAdminMixin:
    change_form_template = 'admin/django_admin_tree/change_form.html'

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
                "<path:object_id>/tree/",
                wrap(self.tree_view),
                name="%s_%s_tree" % info,
            ),
            *super().get_urls(),
        ]

    def tree_view(self, request, object_id, extra_context=None):

        model = self.model
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(
                request, model._meta, object_id
            )

        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied
        descendants = obj.get_descendants(max_depth=self.max_tree_depth)
        add_parent_url = '/admin/{}/{}/add/'.format(self.opts.app_label, self.opts.model_name)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Tree object: %s") % obj,
            "module_name": str(capfirst(self.opts.verbose_name_plural)),
            "object": obj,
            "opts": self.opts,
            'descendants': descendants,
            'add_parent_url': add_parent_url,
            **(extra_context or {}),
        }
        request.current_app = self.admin_site.name
        return TemplateResponse(
            request,
            'admin/django_admin_tree/category_tree.html',
            context,
        )

    @property
    def urls(self):
        return self.get_urls()


    def get_form(self, request, obj=None, **kwargs):
        parent_field = self.model._meta.model.TreeMeta.parent_field_name
        form = super().get_form(request, obj, **kwargs)
        if parent_field in request.GET:
            form.base_fields[parent_field].initial = request.GET[parent_field]
        return form

    def response_add(self, request, obj, post_url_continue=None):
        if "_popup" in request.GET:
            return HttpResponse(f'<script type="text/javascript">window.close();</script>')
        return super().response_add(request, obj, post_url_continue)

