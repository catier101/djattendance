function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function post_locality(id){
    var city_name = $('#id_locality-' + id + '-name').val();
    var state_id = $('#id_locality-' + id + '-state').val();
    var country_code = $('#id_locality-' + id + '-country').val();

    console.log("posting locality creation requestion");
    $.ajax({
        type:"POST",
        url: "save-data",
        data: {
            'type' : 'locality',
            'city_name' : city_name,
            'state_id' : state_id,
            'country_code' : country_code,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data){
            console.log("success message received");
            $('#locality_' + id).hide(400);
        }
    });

    return false;   
}

function post_team(id){
    var team_name = $('#id_team-' + id + '-name').val();
    var team_code = $('#id_team-' + id + '-code').val();
    var team_type = $('#id_team-' + id + '-type').val();
    var team_locality = $('#id_team-' + id + '-locality').val();

    console.log("posting team creation requestion");
    $.ajax({
        type:"POST",
        url: "save-data",
        data: {
            'type' : 'team',
            'team_name' : team_name,
            'team_code' : team_code,
            'team_type' : team_type,
            'team_locality' : team_locality,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data){
            console.log("success message received");
            $('#team_' + id).hide(400);
        }
    });
}

function post_house(id){
    var house_name = $('#id_house-' + id + '-name').val();
    var house_gender = $('#id_house-' + id + '-gender').val();
    var house_address = $('#id_house-' + id + '-address').val();
    var house_city = $('#id_house-' + id + '-city').val();
    var house_zip = $('#id_house-' + id + '-zip').val();

    console.log("posting team creation requestion");
    $.ajax({
        type:"POST",
        url: "save-data",
        data: {
            'type' : 'house',
            'house_name' : house_name,
            'house_gender' : house_gender,
            'house_address' : house_address,
            'house_city' : house_city,
            'house_zip' : house_zip,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data){
            console.log("success message received");
            $('#house_' + id).hide(400);
        }
    });   
}
