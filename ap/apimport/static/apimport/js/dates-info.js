function calculate_dates() {
	var initial_weeks = Number($('#initial_weeks').val());
	var grace_weeks = Number($('#grace_weeks').val());
	var periods = Number($('#periods').val());
	var end_date = addNumWeeks($('#id_start_date').val(), (initial_weeks + grace_weeks + (periods * 2)) * 7, true);
	$('#id_end_date').val(end_date);

	if ($('#initial_weeks').val() == 0 && $('#grace_weeks').val() == 0) {
		$('#init_start').val('');
		$('#init_end').val('');
		$('#grace_start').val('');
		$('#grace_end').val('');
		$('#periods_start').val($('#id_start_date').val());
		$('#periods_end').val(end_date);
		return;
	}

	if($('#initial_weeks').val() == 0) {
		$('#init_start').val('');
		$('#init_end').val('');
		$('#grace_start').val($('#id_start_date').val());
		var grace_end = addNumWeeks($('#grace_start').val(), grace_weeks * 7, true);
		$('#grace_end').val(grace_end);
		$('#periods_start').val(addNumWeeks($('#grace_end').val(), 1, false));
		$('#periods_end').val(end_date);
		return;
	}
	
	if($('#grace_weeks').val() == 0) {
		$('#init_start').val($('#id_start_date').val());
		$('#init_end').val(addNumWeeks($('#id_start_date').val(), initial_weeks * 7, true));
		$('#grace_start').val('');
		$('#grace_end').val('');
		$('#periods_start').val(addNumWeeks($('#init_end').val(), 1, false));
		$('#periods_end').val(end_date);
		return;
	}

	$('#init_start').val($('#id_start_date').val());
	$('#init_end').val(addNumWeeks($('#id_start_date').val(), initial_weeks * 7, true));
	$('#grace_start').val(addNumWeeks($('#init_end').val(), 1, false));
	$('#grace_end').val(addNumWeeks($('#grace_start').val(), grace_weeks * 7, true));
	$('#periods_start').val(addNumWeeks($('#grace_end').val(), 1, false));
	$('#periods_end').val(end_date);
	return;
}

function addNumWeeks(date, days, subOne=false)
{
    var monthDays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    
    var year = Number(date.substring(6, 10));
    var month = Number(date.substring(0, 1));
    var day = Number(date.substring(3, 5));
    
    if ( month == 1 )
        month = 10 + Number(date.substring(1, 2));
    else
        month = Number(date.substring(1, 2));

    var numDays = monthDays[month];
    if ( ( year % 4 == 0 ) && ( month == 2 ) )
        numDays = 29;

    day = day + days;
    if (subOne)
        day--;
    while ( day > numDays )
    {
        day -= numDays;
        month++;
        if ( month == 13 )
        {
            month = 1;
            year++;
        }
        numDays = monthDays[month];
	    if ( ( year % 4 == 0 ) && ( month == 2 ) )
	        numDays = 29;
    }
    
    retval = "";
    if ( month < 10 )
        retval += "0";
    retval += month;
    retval += "/";
    if ( day < 10 )
        retval += "0";
    retval += day;
    retval += "/";
    retval += year;
    return retval;        
}