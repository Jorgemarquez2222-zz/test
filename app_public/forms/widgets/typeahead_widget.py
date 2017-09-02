from string import Template

from django.forms import Widget
from django.utils.safestring import mark_safe

"""
    Params
        tokens : List of fields to perform search in
        input_value_parser : 
        suggestion_tag : 
"""


class SearchParameters:
    def __init__(self, tokens: list, input_value_parser: str, suggestion_tag: str = '', display_callback: str = None):
        self.tokens = tokens
        self.input_value_parser = input_value_parser
        self.suggestion_tag = suggestion_tag
        self.display_callback = display_callback


"""
    Params
        source_url : The url from which results are loaded
        static : boolean, if true, no need to request api on keyborad input, the list is static
        source_url_dynamic : the dynamic url containing the %QUERY for the searched text
        update_callback : the custom JS called when a suggestion is clicked (variable 'data' accessible)
        search_parameters : 
"""


class TypeAheadWidget(Widget):
    def __init__(self,
                 source_url_static: str,
                 static: bool = True,
                 source_url_dynamic: str = None,
                 update_callback: str = None,
                 search_parameters: SearchParameters = None):
        self.source_url_static = source_url_static
        self.static = static
        self.source_url_dynamic = source_url_dynamic
        self.update_callback = update_callback
        self.search_parameters = search_parameters
        super(TypeAheadWidget, self).__init__()

    def render(self, name, value, attrs=None):
        html = Template("""
                <input name='$name' type='text' value='$value' required class='typeahead form-control' id='id_$name' autocomplete="off"/>
                <script>
                    $$("#id_$name").on('typeahead:select', $update_callback);
                    $$(document).ready(
                        searchTypeAheadConfiguration('$static', '$apiUrl', '$apiUrlDynamic', $searchFields, 
                                                    '$suggestionTag', function(data) {$inputValueParser},
                                                    $display_callback, 'id_$name')
                    );
                </script>
            """)
        return mark_safe(html.substitute(name=name,
                                         static='true' if self.static else 'false',
                                         apiUrlDynamic=TypeAheadWidget.convert_field_jsvar(self.source_url_dynamic),
                                         update_callback=TypeAheadWidget.convert_field_jsvar(self.update_callback),
                                         apiUrl=TypeAheadWidget.convert_field_jsvar(self.source_url_static),
                                         searchFields=self.search_parameters.tokens,
                                         suggestionTag=self.search_parameters.suggestion_tag,
                                         inputValueParser=self.search_parameters.input_value_parser,
                                         display_callback=TypeAheadWidget.convert_field_jsvar(
                                             self.search_parameters.display_callback),
                                         value=value if value is not None else ""
                                         ))

    @classmethod
    def convert_field_jsvar(cls, field: str):
        return 'undefined' if field is None else field
