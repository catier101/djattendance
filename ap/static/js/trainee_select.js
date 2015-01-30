$(document).ready(function(){
    var base_url = window.location.protocol + '//' + window.location.host;
    var api_base = '/api'

    function getTrainees(data) {
        var trainee_groups = {'terms': [], 
                              'gender': [],
                              'hc': [],
                              'team_types': [],
                              'teams': [],
                              'houses': [],
                              'localities': []
                             }

        var deferreds = []; // all ajax deferred objects get pushed into here

        for (i = 0; i < data['terms'].length; i++) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/term/' + data['terms'][i] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['terms'] = _.union(trainee_groups['terms'], getTraineeIDs(data));
                    }
                }));
        }

        if (data['gender']) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/gender/' + data['gender'] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['gender'] = getTraineeIDs(data);
                    }
                }));
        }

        if (data['hc']) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/HC/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['hc'] = getTraineeIDs(data);
                    }
                }));
        }

        for (i = 0; i < data['team_types'].length; i++) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/teamtype/' + data['team_types'][i] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['team_types'] = _.union(trainee_groups['team_types'], getTraineeIDs(data));
                    }
                }));
        }

        for (i = 0; i < data['teams'].length; i++) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/team/' + data['teams'][i] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['teams'] = _.union(trainee_groups['teams'], getTraineeIDs(data));
                    }
                }));
        }

        for (i = 0; i < data['houses'].length; i++) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/house/' + data['houses'][i] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['houses'] = _.union(trainee_groups['houses'], getTraineeIDs(data));
                    }
                }));
        }

        for (i = 0; i < data['localities'].length; i++) {
            deferreds.push(
                $.ajax({
                    url: base_url + api_base + '/trainees/locality/' + data['localities'][i] + '/?format=json',
                    contentType: 'application/json',
                    data: data,
                    dataType: 'json',
                    success: function(data) {
                        trainee_groups['localities'] = _.union(trainee_groups['localities'], getTraineeIDs(data));
                    }
                }));
        }

        // when all ajax calls are successful, find intersection of
        // all trainee groups and add trainees to Trainee field.
        $.when.apply($, deferreds).then(function(){
            var intersect = [];
            for (k in data) {
                console.log(data[k]);
                console.log(data[k] != false);
                if (data[k] != false && data[k] != undefined) {
                    intersect[intersect.length] = trainee_groups[k];
                }
            }
            console.log(intersect);
            addTrainees(_.intersection.apply(this, intersect));
        });

    }

    // data: trainees in JSON
    // return array of trainee ids
    function getTraineeIDs(data) {
        var trainee_ids = [];
        for (i = 0; i < data.length; i++) {
            trainee_ids[trainee_ids.length] = data[i]['id'];
        };
        return trainee_ids;
    }

    // data: array of trainee ids to be added into the Trainee field
    // function selects trainees in Trainee Select2 field.
    function addTrainees(trainee_ids) {
        if ($('#id_trainees').val()){
            trainee_ids = _.union(trainee_ids, $('#id_trainees').val());
        }

        $('#id_trainees').select2("val", trainee_ids);
        return;
    }

    $('#trainee_select_form').submit(function(event) {
        event.preventDefault();
        form_data = {
            'terms': getValues($('input[name=term]:checked')),
            'gender': $('input[name=gender]:checked').attr('value'),
            'hc': $('#id_hc').is(":checked"),
            'team_types': getValues($('input[name=team_type]:checked')),
            'teams': getValues($('select[name=team] option:selected')),
            'houses': getValues($('select[name=house] option:selected')),
            'localities': getValues($('select[name=locality] option:selected')),
        };
        getTrainees(form_data);
        $('#trainee_select').modal('hide');
        clearForm();
    })

    function getValues(object) {
        var values = [];
        object.each(function() {
            values[values.length] = $(this).attr('value');
        })
        return values;
    }

    function clearForm() {
        document.getElementById('trainee_select_form').reset();
        $('#id_team').select2('val', []);
        $('#id_house').select2('val', []);
        $('#id_locality').select2('val', []);
    }
})