//Function to configure input google maps search bar
// search_bar_id = id of the input element
// latitude_id = id of element where the latitude will be saved
// longitude_id = id of element where the longitude will be saved

function init(search_bar_id, latitude_id, longitude_id)
{
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById(search_bar_id),
        {
            types: ['geocode'],
            componentRestrictions:
            {
                country: "pe"
            }
        });
    google.maps.event.addListener(autocomplete, 'place_changed', function ()
    {
        var place = autocomplete.getPlace();
        $('#' + latitude_id).val(place.geometry.location.lat().toFixed(8));
        $('#' + longitude_id).val(place.geometry.location.lng().toFixed(8));
    });
}