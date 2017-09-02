from string import Template

from django.forms import Widget
from django.utils.safestring import mark_safe


class DateTimePickerWidget(Widget):
    def render(self, name, value, attrs=None):
        html = Template("""
                    <div class='input-group date' id='$id'>
                    <input type='text' class="form-control" />
                    <span class="input-group-addon">
                        <span class="glyphicon glyphicon-calendar"></span>
                    </span>
                    </div>
                    <input type='hidden' name='$name' value="" />
                    <script type="text/javascript">
                        $$("#$id").on('dp.change',
                            function (e)
                            {
                                $$("input[name='$name']").val($$("#$id").data("DateTimePicker").date().toISOString());
                            }
                        );
                    </script>
                    """)
        return mark_safe(html.substitute(name=name, id='id_%s' % name))
