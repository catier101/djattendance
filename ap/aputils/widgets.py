from django.forms.widgets import DateInput, TimeInput
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

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
