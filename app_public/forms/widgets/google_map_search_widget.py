from string import Template

from django.forms import Widget
from django.utils.safestring import mark_safe


"""
    Params
        source_url : The url from which results are loaded
        static : boolean, if true, no need to request api on keyborad input, the list is static
        source_url_dynamic : the dynamic url containing the %QUERY for the searched text
        update_callback : the custom JS called when a suggestion is clicked (variable 'data' accessible)
        search_parameters : 
"""


class GoogleMapSearchWidget(Widget):
    def __init__(self, latitude_id: str, longitude_id: str):
        self.latitude_id = latitude_id
        self.longitude_id = longitude_id
        super(GoogleMapSearchWidget, self).__init__()

    def render(self, name, value, attrs=None):
        html = Template("""
                <input name='$name' type='text' value='$value' required class='form-control' id='id_$name'/>
                <script>
                    function initGoogleMapsSearchBar()
                    {
                        init('id_$name', '$latitude', '$longitude');
                    }
                </script>
                <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA5ztaHSbnPz_Xaj7CgxPjUeEPlKglZ10A&libraries=places&callback=initGoogleMapsSearchBar"
                    async defer>
                </script>
            """)
        return mark_safe(html.substitute(name=name, value=value, latitude=self.latitude_id, longitude=self.longitude_id))