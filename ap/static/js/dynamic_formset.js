// Code adapted from http://djangosnippets.org/snippets/1389/
function updateElementIndex(element, prefix, index) {
	var id_regex = new RegExp('(' + prefix + '-\\d+-)');
	var replacement = prefix + '-' + index + '-';
	if ($(element).attr('for')) {
		$(element).attr('for', $(element).attr('for').replace(id_regex, replacement));
	}
	if (element.id) {
		element.id = element.id.replace(id_regex, replacement);
	}
	if (element.name) {
		element.name = element.name.replace(id_regex, replacement);
	}
}

function deleteForm(btn, prefix) {
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	if (formCount > 1) {
		// Delete the item/form
		$(btn).parents('.entry').slideUp({
			'duration': 300, 
			'always': function() {
				$(this).remove();
				var forms = $('.entry'); // Get all the forms
				$('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
				var i = 0;
				// Go through the forms and set their indices, names, and IDs
				for (formCount = forms.length; i < formCount; i++) {
					$(forms.get(i)).children().first().each(function() {
						updateElementIndex(this, prefix, i);
					})
					$(forms.get(i)).children().children("[id^='id_form-']").each(function() {
							updateElementIndex(this, prefix, i);
					});
				}

				// Disable delete if only one form left
				if (formCount == 1) {
					$('.delete').hide();
				}
			}
		});

	}
	return false;
}

function addForm(btn, prefix) {
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	// max num
	if (formCount < parseInt($('#id_' + prefix + '-MAX_NUM_FORMS').val())) {
		// Clone a form (without event handlers) from the first form
		var row = $('.entry:first').clone(false).get(0);

		// Insert it after the last form
		$(row).removeAttr('id').hide().insertAfter('.entry:last').slideDown(300);

		// Remove the bits we don't want in the new row/form
		// e.g. error messages
		$('.errorlist', row).remove();
		$(row).children().removeClass('error');

		// Relabel or rename all the relevant bits
		$(row).children().children().each(function () {
			updateElementIndex(this, prefix, formCount);
			$(this).val('');
		});

		// Add event handler for the delete item/form link
		$(row).find('.delete').click(function () {
			return deleteForm(this, prefix);
		});

		// If there was previously only one form, the delete button was hidden, so show it.
		if (formCount == 1) {
			$('.delete').show();
		}

		// Update total form count
		$('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);

	}	
	else {
		alert('Sorry, you can only enter a maximum of ten trainees.');
	}
	return false;
}

$(document).ready(function () {

	$('#add').click(function () {
		return addForm(this, 'form');
	});

	$('.delete').click(function() {
		return deleteForm(this, 'form');
	});

	// INITIAL_FORMS should match the number of updated forms
	$('form').submit(function(e){
		$('#id_form-INITIAL_FORMS').val($('form .entry').children('input[value]').length);
		return true;
	});
});
