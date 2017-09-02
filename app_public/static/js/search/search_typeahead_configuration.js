/*
*   static : boolean, if true, no need to request api on keyborad input, the list is static
*   staticUrl : the url to prefetch data from
*   apiUrl : the dynamic url containing the %QUERY for the searched text
*   searchFields : the fields to search the text in
*   suggestionTag : Text in header of suggestions
*   inputValueParser : function called to transforms api's output and return a list of objects
*   display_callback : function that converts the suggestion to a text displayed
*/


function searchTypeAheadConfiguration(static, staticUrl, apiUrl, searchFields, suggestionTag, inputValueParser, display_callback, id)
{
    var prefetch_opt = undefined;
    if (staticUrl !== undefined)
    {
        prefetch_opt = {
                url : staticUrl,
                transform : inputValueParser,
                cache : false};
    }

    var remote_opt = undefined;
    if (apiUrl !== undefined && !static)
    {
        remote_opt = {
            url : apiUrl,
            wildcard : '%QUERY',
            transform : inputValueParser
        };
    }
    //for substring matching:
    /*
    datumTokenizer: function(d) { var test = Bloodhound.tokenizers.whitespace(d); $.each(test,function(k,v){ i = 0; while( (i+1) < v.length ){ test.push(v.substr(i,v.length)); i++; } }) return test; },
    */
    var resultspec = new Bloodhound(
    {
        initialize: false,
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace(searchFields),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: prefetch_opt
    });

    resultspec.clearPrefetchCache();
    resultspec.initialize();

    //this wrapper is used to force the display of all suggestions when the query(input) is empty
    var bloodHoundWrapper = function (query, sync)
    {
        if (query === '')
        {
            sync(resultspec.all());
        }
        else
        {
            resultspec.search(query, sync);
        }
    };

    $('#' + id).typeahead(
        {
            hint: true,
            highlight: true,
            minLength: 0 /* Minimum chars to trigger request to server*/
        },
        {
            name: 'result',
            source: bloodHoundWrapper,
            display : display_callback,
            limit : 10,
            /*
            templates:
            {
                pending: ['<div class="tt-pending">', '</div>'].join('\n'),
                header: '<div class="headresult">' + suggestionTag + '</div>',
                notFound: '<span class="nodata">No data Found for search</span>'
            }*/
        }
    );
};