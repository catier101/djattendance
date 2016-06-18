function render_question(question_json, response_json, display_type, index){
    var question = JSON.parse(question_json);
    var response = JSON.parse(response_json);
    if (question.type == "essay")
        render_essay_question(question, response, display_type, index);
    else
        alert("Question type not yet implemented!")
}

function render_essay_question(question, response, display_type, index){
    var ol = $('#question-list');

    // Question String
    var li = $(document.createElement('li'));
    var pts = $(document.createElement('b')).html(' (Points: ' + question.points + ')');

    li.append(question.prompt)
    li.append(pts)
    ol.append(li);
    ol.append('<br />');

    // Response area
    var resp_area = $(document.createElement('textarea'));
    resp_area.val(response.response == null ? '' : response.response)
    resp_area.addClass('exam-response');
    resp_area.attr({
        'id': index,
        'cols': '100',
        'rows': '10',
        'placeholder': 'Type your response here.',
        'name': 'response'
    });

    if (display_type != 'Take' && display_type != 'Retake')
        resp_area.prop('disabled', true);

    ol.append(resp_area);
    ol.append('<br />');

    // Word count
    var wc_text = $(document.createElement('b')).html('Word Count: ');
    var wc_span = $(document.createElement('span')).html('0');
    wc_span.attr('id', 'count' + index);

    ol.append(wc_text)
    ol.append(wc_span);
    ol.append('<br />');

    Countable.live(resp_area.get(0), function(counter){
        var span = document.getElementById('count' + index);
        span.innerHTML = counter.words;
    })

    // Score and Grader Comment
    if (display_type == 'Grade' || display_type == 'Retake'){
        var score_text = $(document.createElement('b')).html('Score: ');
        var score_input = $(document.createElement('input'));
        score_input.val(response.score == null ? '' : response.score);
        score_input.addClass('score form-control');
        score_input.attr({
            'id': 'score' + index,
            'type': 'text',
            'name': 'question-score'
        });

        if (display_type != 'Grade')
            score_input.prop('disabled', true);

        ol.append(score_text);
        ol.append(score_input);

        var comment_text = $(document.createElement('b')).html(' Comment: ');
        var comment_input = $(document.createElement('input'));
        comment_input.val(response.comment == null ? '' : response.comment);
        comment_input.addClass('grader-comment form-control');
        comment_input.attr({
            'id': 'comment' + index,
            'type': 'text',
            'name': 'grader-comment'
        });

        if (display_type != 'Grade')
            comment_input.setProp('disabled', true);

        ol.append(comment_text);
        ol.append(comment_input);
    }
}

 function render_question_for_edit(question_json, index){
    var question = JSON.parse(question_json);
    if (question.type == "essay")
        render_essay_question_for_edit(question, index);
    else
        alert("Question type not yet implemented!")
}

function render_essay_question_for_edit(question, index){
    var qBox = $('#qBox');
    var newDiv = $(document.createElement('div'));

    // Question String
    var question_prompt = $(document.createElement('input'));
    question_prompt.addClass('question form-control');
    question_prompt.val(question.prompt);
    question_prompt.attr({
        'id': 'question' + index,
        'type': 'text',
        'name':'question-prompt'
    });

    var question_point = $(document.createElement('input'));
    question_point.addClass('question form-control');
    question_point.val(question.points);
    question_point.attr({
        'id': 'qpoint' + index,
        'type': 'text',
        'name': 'question-point'
    });

    // Create array of question types
    var array = ['Essay'];

    // Create and append select list
    var question_type = $(document.createElement("select"));
    question_type.addClass('question form-control');
    question_type.attr({
        'id': 'selectbasic' + index,
        'name': 'question-type'
    });

    // Create and append the options
    for (var i = 0; i < array.length; i++) {
        var option = $(document.createElement('option'));
        option.val(array[i].toLowerCase());
        option.html(array[i]);

        if (question_type == option.value)
            option.prop('selected', true);

        question_type.append(option);
    }

    newDiv.append(question_prompt);
    newDiv.append(question_point);
    newDiv.append(question_type);

    var remove_button = $(document.createElement('input'));
    remove_button.val('Remove question');
    remove_button.addClass('remove btn btn-info-outline');
    remove_button.attr({
        'id': index,
        'type': 'button'
    });

    newDiv.append(remove_button);
    newDiv.append('<br /><br />')
    qBox.append(newDiv);
}

function package_questions(display_type){
    var question_count = $('#question_count').attr('value');
    for (i = 0; i < question_count; i++){
        var question = JSON.parse($('#question_' + (i+1).toString()).attr('value'));
        var response = JSON.parse($('#response_' + (i+1).toString()).attr('value'));

        if (question.type == 'essay')
            package_essay_question(response, display_type, i+1);
        else
            alert("Question type not yet implemented!")
    }
}

function package_essay_question(response, display_type, index){
    var form = $('#exam_form');
    if (display_type == 'Take' || display_type == 'Retake'){
        response.response = $('#' + index).val();
    }

    if (display_type == 'Grade'){
        response.score = $('#score' + index).val();
        response.comment = $('#comment' + index).val()
    }

    var input_field = $(document.createElement('input'));
    input_field.val(JSON.stringify(response));
    input_field.attr({
        'type': 'hidden',
        'name': 'response_json'
    });

    form.append(input_field);
}