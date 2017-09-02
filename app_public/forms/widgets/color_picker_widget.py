from django import forms
from django.utils.safestring import mark_safe
from string import Template


class ColorPickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        html = Template("""
                <div id="cp_$name" class="input-group colorpicker-component">
                    <input id="id_$name" name="$name" type="text" value="$value" class="form-control" />
                    <span class="input-group-addon"><i></i></span>
                </div>
                <script>
                    $$(function() {
                        $$('#cp_$name').colorpicker({
                            'template': '<div class="colorpicker dropdown-menu"><div class="colorpicker-saturation"><i><b></b></i></div><div class="colorpicker-hue"><i></i></div><div class="colorpicker-color"><div /></div><div class="colorpicker-selectors"></div></div>',
                            'colorSelectors': {'#000000': '#000000','#ffffff': '#ffffff','#FF0000': '#FF0000','#777777': '#777777','#337ab7': '#337ab7','#5cb85c': '#5cb85c','#5bc0de': '#5bc0de','#f0ad4e': '#f0ad4e','#d9534f': '#d9534f'}
                            });
                    });
                </script>
            """)
        return mark_safe(html.substitute(value=value, name=name))