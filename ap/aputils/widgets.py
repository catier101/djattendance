from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.templatetags.admin_static import static
from django.forms.widgets import DateInput, TimeInput
from django.forms.widgets import RadioSelect
from django_select2 import *
from django_select2.forms import *


class DatePicker(DateInput):
    format = '%m/%d/%Y'
    
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'class': 'datepicker'}
        super(DatePicker, self).__init__(*args, **kwargs)
        
    class Media:
        css = {
            'all': ('jquery/css/jquery-ui-1.10.3.min.css',
                    'jquery/css/datepicker.css',)
        }
        js = (
            'js/jquery-1.11.1.min.js',
            'jquery/js/jquery.ui.core.js',
            'jquery/js/jquery.ui.datepicker.js',
            'js/datepicker.js',
        )


class HorizRadioRenderer(RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class PlusSelect2MultipleWidget(ModelSelect2MultipleWidget):
  def render(self, name, value, attrs=None, choices=()):
    output = super(PlusSelect2MultipleWidget, self).render(name, value, attrs, choices)
    link = []
    rel_to = self.choices.queryset.model
    info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
    related_url = reverse('admin:%s_%s_add' % info, current_app='admin') + '?_to_field=id&amp;_popup=1'
    link.append(u'<a href="%s" class="related-widget-wrapper-link add-related" id="add_id_%s"> ' % (related_url, name))
    link.append(u'<img src="%s" width="10" height="10" alt="%s"/></a>'
      % (static('admin/img/icon_addlink.gif'), _('Add Another')))
    return output + mark_safe(u''.join(link))