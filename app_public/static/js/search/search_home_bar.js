function initAutocomplete()
{
    // Create the autocomplete object, restricting the search to geographical
    // location types.

    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */
        (document.getElementById('pac_input')),
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

        document.getElementById('cityLat').value = place.geometry.location.lat();
        document.getElementById('cityLng').value = place.geometry.location.lng();
        //alert("This function is working!");
        //alert(place.name);
        // alert(place.address_components[0].long_name);

    });
    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    //autocomplete.addListener('place_changed', fillInAddress);
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(function (position)
        {
            var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle(
            {
                center: geolocation,
                radius: position.coords.accuracy
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}
$(document).ready(function ()
{

    var kk = 25;

    $(window).resize(function ()
    {
        var w = $('header').width();
        if (w <= 400)
        {

            kk = 7;

        }
        else if (w > 380 && w < 720)
        {

            kk = 15;
        }
        $('.typeahead').trigger('change');

    });

    $('#search-form').submit(function ()
    {
        var str1 = $('#search_text').val();
        var str2 = $('#pac_input').val();
        var ret = true;
        if (!str1)
        {
            $('#search_text').addClass('error-elem');
            $('.typeahead').fadeOut(550).promise().done(function ()
            {
                $('.typeahead').toggleClass("blink-class").fadeIn(550);
            });
            ret = false;
        }
        else
        {
            $('#search_text').removeClass('error-elem');
        }
        if (!str2)
        {
            $('#pac_input').addClass('error-elem');
            $('#pac_input').fadeOut(550).promise().done(function ()
            {
                $('#pac_input').toggleClass("blink-class").fadeIn(550);
            });
            ret = false;
        }
        else
        {
            $('#pac_input').removeClass('error-elem');
        }
        return ret;
    });
    // Create the search box and link it to the UI element.
    // var input = document.getElementById('pac-input');
    //var searchBox = new google.maps.places.SearchBox(input);

    var resultspec = new Bloodhound(
    {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch:
        {
            url : "/api/search/?speciality&search_text=",
            cache : false,
            transform : function (response)
            {
                return response.data;
            }
        }
    });

    var resulthosp = new Bloodhound(
    {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote:
        {
            url: srchUrlHosp,
            wildcard: '%QUERY',
            transform: function (response)
            {
                return response.data;
            }
        }
    });

    var resultdocs = new Bloodhound(
    {
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace(['first_name', 'last_name']),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote:
        {
            url: srchUrlDocs,
            wildcard: '%QUERY',
            transform: function (response)
            {
                return response.data;
            }
        }
    });

    // Initializing the typeahead

    $('.typeahead').typeahead(
        {
            hint: true,
            highlight: true,
            minLength: 0 /* Minimum chars to trigger request to server*/
        },
        {
            name: 'result',
            display: 'name',
            source: resultspec,
            limit: 200,
            templates:
            {
                pending: ['<div class="tt-pending">', '</div>'].join('\n'),
                header: '<div class="headresult">Specialities</div>',
                notFound: '<span class="nodata">No data Found for search</span>'
            }

        },
        {
            name: 'result1',
            display: 'name',
            source: resulthosp,
            limit: 200,
            templates:
            {
                //pending :['<div class="tt-pending">','</div>'].join('\n'),
                header: '<div class="headresult">Hospitals</div>',
                suggestion: function (data)
                {
                    return `<a href=${data.url}>
                                <div class="outerdiv" style="min-height:70px;position:relative; top:0px left:0px;">
                                    <img style="height:40px;width:40px;vertical-align:initial" class="img-circle resultimg" src='${data.photo_url}'>
                                    <div class="infodiv" >
                                        <span class="sugg-main">${data.name}</span>
                                    </div>
                                </div>
                            </a>`;
                }
            }

        },
        {
            name: 'result2',
            display: function (obj)
            {
                return obj.first_name + ' ' + obj.last_name;
            },
            source: resultdocs,
            limit: 200,
            templates:
            {
                //pending :['<div class="tt-pending">','</div>'].join('\n'),
                header: '<div class="headresult">Doctors</div>',
                suggestion: function (data)
                {
                    return `<a href=${data.url}>
                                <div class="outerdiv" style="min-height:70px;position:relative;top:0px left:0px;">
                                    <img style="height:40px;width:40px;vertical-align:initial" class="img-circle resultimg" src='${data.photo_url}'>
                                    <div class="infodiv" >
                                        <span class="sugg-main">${data.first_name} ${data.last_name}</span>
                                        <br>
                                        <span class="sugg-sub">` + formatSubLine(data.speciality, data.location) + `</span>
                                    </div>
                                </div>
                            </a>`;
                }
            }
        }

    );

    $('.typeahead').focus(function ()
    {
        phtoggle('set');
    });
    $("#srchph").click(function ()
    {
        phtoggle('set');
        $('.typeahead').focus();
    });
    $('.typeahead').focusout(function ()
    {
        if (!$(this).val())
            phtoggle('unset');
    });
    $('.typeahead').bind("keyup keydown change", function (e)
    {
        if ($(this).val().length > kk)
        {
            phHidden(true);
        }
        else
        {
            phHidden(false);
        }
    });
    $('.typeahead').on('typeahead:asyncreceive', function (evt, query, name)
    {
        var menu1 = $(this).data('tt-typeahead').menu;
        var ds1 = (menu1.datasets[0].$el)[0].childNodes;
        var ds2 = (menu1.datasets[1].$el)[0].childNodes;
        var ds3 = (menu1.datasets[2].$el)[0].childNodes;
        if (ds1.length <= 1 && ds2.length === 0 && ds3.length === 0)
        {

            $(".nodata").show();
        }
        else
        {

            $(".nodata").hide();
        }

    });
    $('.typeahead').on('typeahead:render', function (evt, query, name, hull)
    {
        $(".outerdiv").each(function (index)
        {
            var $inner = $(this).children('.infodiv');
            var height = parseInt($inner.height()) + parseInt($inner.css('top'));
            $(this).css('height', height);
        });

        var len = $("#search_text").val().length;
        if (len < 3 && len > 0)
        {
            $('.tt-menu').hide();
        }
        else
        {
            $('.tt-menu').show();
        }

    });
    $('.twitter-typeahead').on('mouseover', '.tt-suggestion', function (event)
    {
        $('.tt-suggestion').removeClass('tt-cursor');
        $(this).addClass('tt-tag-hover');
    });

    $('.twitter-typeahead').bind('typeahead:cursorchange', function (ev, suggestion)
    {
        $('.tt-suggestion').removeClass('tt-tag-hover');
    });

    $('.typeahead').on('typeahead:select', function (evt, sugg, ds)
    {
        if ((ds === 'result1' || ds === 'result2') && sugg.next_url)
        {
            window.location = sugg.next_url;
        }

    });
});

function phtoggle(setting)
{
    if (setting == 'set')
    {
        $("#srchph").removeClass("phdefault");
        $("#srchph").addClass("phsidened");
    }
    else
    {
        $("#srchph").removeClass("phsidened");
        $("#srchph").addClass("phdefault");
    }

}

function phHidden(hide)
{
    if (hide)
    {
        $("#srchph").hide();
    }
    else
    {
        $("#srchph").show();
    }
}

function formatSubLine(val1, val2)
{
    if (val1 && val2)
    {
        return val1 + ' , ' + val2;
    }
    else if (val1)
    {
        return val1;
    }
    else if (val2)
    {
        return val2;
    }
    else
    {
        return '';
    }
}