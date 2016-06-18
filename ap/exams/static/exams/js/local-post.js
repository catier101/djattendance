function submit_form(name, value){
    var form = document.getElementById("hidden-form");
    var field = document.createElement("input");
    field.setAttribute("type", "hidden");
    field.setAttribute("name", name);
    field.setAttribute("value", value);
    form.appendChild(field);

    document.body.appendChild(form);
    form.submit();      
}

function unfinalize_grade(session_id){
    submit_form("unfinalize-session-id", session_id);
}

function delete_exam(session_id){
    submit_form("delete-session-id", session_id);
}

function open_for_retake(trainee_id){
    submit_form("retake-trainee-id", trainee_id);
}