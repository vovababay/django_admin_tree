"""
https://github.com/mqsoh/django-gfklookupwidget
"""
import json

from random import randint

from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
import django.forms


class GfkLookupWidget(django.forms.Widget):
    """
    Виджет для выбора объекта GenericForeignKey по content_type
    """

    def __init__(self, *args, **kwargs):
        """Args:
            content_type_field_name: This is name of the field that becomes a
                select box in the admin.
            parent_field: This is a field on the model. It's used to find the
                related content_type field to generate URLs for the choices.
        """
        self.ct_field_name = kwargs.pop('content_type_field_name')
        self.parent_field = kwargs.pop('parent_field')
        self.app_label = kwargs.pop('app_label')
        self.model_name = kwargs.pop('model_name')

        super(GfkLookupWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # model = self.parent_field.model
        # ct_field = self.parent_field.model._meta.get_field(self.ct_field_name)
        # choices = ct_field.get_choices()

        # We'll generate the URLs for each supported content type upfront and
        # store them in a dict indexed on the model name. This will allow the
        # JavaScript to get the URL based on the <select> box markup.
        urls = {}
        # for type_id, type_name in choices:
        #     # This is the default "-------" entry.
        #     if not type_id:
        #         continue
        #
        #     content_type = django.contrib.contenttypes.models\
        #         .ContentType.objects.get_for_id(type_id)

            # The URLs for the anchors used by showRelatedObjectLookupPopup
            # have the form of:
            #
            #     /<app_label>/<model>/?t=<pk_field_name>
            #     /myapp/foomodel/?t=id
        try:
            url = reverse(
                'admin:{app}_{model}_changelist'.format(
                    app=self.app_label,
                    model=self.model_name))
        except NoReverseMatch:
            # This content type isn't available in the admin, so we can't
            # provide the lookup. This is common, so we'll just ignore this
            # one.
            pass

        urls['test'] = url

        # When default value is None, input box should be empty.
        if value is None:
            value = ""

        # JavaScript braces need to be doubled due to the string formatting.
        #
        # vForeignKeyRawIdAdminField is required by the popup to target this
        # field.
        #
        # This script must be called from the onclick attribute. When this
        # widget is displayed inline, the DOM nodes are copied from templated
        # nodes and a '__prefix__' token is replaced with the index of the new
        # row. The Django code that does this doesn't do that replacement
        # inside the script node so the IDs end up as
        # 'lookup_id_foomodel_set-__prefix__-foofield'.
        #
        # In this situation the script will have been rendered with a
        # ct_field_name with the __prefix__ template, so  we also need to use
        # the ID on the link node as a template for finding the related select
        # box.
        return mark_safe("""
            <input class="vForeignKeyRawIdAdminField" id="id_{name}" name="{name}" value="{value}" type="text" />
            <a id="lookup_id_{name}" class="related-lookup gfklookup" onclick="return gfklookupwidget_{uniq}_click(django.jQuery, this, event);"></a>
            <script type="text/javascript">
                if (typeof(gfklookupwidget_{uniq}_click) == 'undefined') {{
                    function gfklookupwidget_{uniq}_click($, element, event) {{
                        if (event) {{
                            event.preventDefault();
                            event.stopPropagation();
                        }}

                        var urls = {urls};
                        var $this = $(element);
                        var ct_field_name = "{ct_field_name}";

                        var prefix = "";
                        var id = $this.attr('id');
                        if (id.indexOf('-')) {{
                            ct_field_name = id.substring(0, id.lastIndexOf('-') + 1).replace('lookup_id_', '') + ct_field_name;
                        }}

                        var selected = $('select[name="'+ct_field_name+'"]').find('option:selected');
                        var content_type_id = selected.val();
                        var content_type = selected.text();

                        if (!content_type) {{
                            alert('No content type found for GenericForeignKey lookup.');
                            return false;
                        }}

                        if (!content_type_id) {{
                            alert('You must select: '+ct_field_name+'.');
                            return false;
                        }}

                        $this.attr('href', urls[content_type]);

                        return showRelatedObjectLookupPopup(element);
                    }}
                }}
            </script>
        """.format(
            uniq='{:X}'.format(randint(1, 1000000)),
            name=name,
            value=value,
            urls=json.dumps(urls),
            ct_field_name=self.ct_field_name,
        ))

