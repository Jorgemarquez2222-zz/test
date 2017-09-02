function setSubmitListener(form_id, url)
{
    var form = $('#' + form_id);
	form.submit(function(event) {
		event.preventDefault();
		$.post(url, form.serialize(), function(data, textStatus, xhr) {
			if (xhr.status == 200)
				location.reload();
		});
	});
}