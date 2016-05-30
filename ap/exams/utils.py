import json

from datetime import timedelta

from .models import Exam, Section, Responses, Retake
from .models import Class


# Returns the section referred to by the args, None if it does not exist
def get_exam_section(exam, section_id):
    try:
        section = Section.objects.get(exam=exam, section_index=section_id)
        return section
    except Section.DoesNotExist:
        return None

# Returns an array containing the interesting data for the given section. None
# returned if the exam is invalid
def get_exam_questions_for_section(exam, section_id):
    section = get_exam_section(exam, section_id)
    questions = []
    if (section == None):
        return None

    for i in range(section.first_question_index - 1, section.question_count):
        questions.append(section.questions[str(i+1)])

    return questions

# Returns an array containing the interesting data.  None is returned if the
# exam is invalid.
def get_exam_questions(exam):
    questions = []
    for i in range(0, exam.section_count):
        section_questions = get_exam_questions_for_section(exam, i)
        if (section_questions != None):
            questions += section_questions
        else:
            return []

        # TODO(verification): We should sanity check that the question numbers
        # per section are vaguely correct whenever we have an exam that has 
        # when we start having exams with more than one section.
    return questions

def get_exam_questions_for_section(exam, section_id):
    section = get_exam_section(exam, section_id)
    questions = []
    if (section == None):
        return None

    for i in range(section.first_question_index - 1, section.question_count):
        questions.append(section.questions[str(i+1)])

    return questions


# Returns a tuple of responses, grader_extras, and scores for the given exam 
# in the given section
def get_responses_for_section(exam_pk, section_id, session, current_question):
    section = get_exam_section(exam_pk, section_id)
    responses = []
    if section == None:
        return []

    try:
        responses_object = Responses.objects.get(session=session, section=section)
    except Responses.DoesNotExist:
        responses_object = None

    for i in range(section.first_question_index - 1, section.question_count):
        if responses_object and str(i+1) in responses_object.responses:
            responses.append(responses_object.responses[str(i+1)])
        else:
            responses.append("{}")

    return responses

# Returns a tuple of responses, grader_extras, and scores for the given exam
def get_responses(exam, session):
    current_question = 1
    responses = []
    grader_extras = []
    scores = []

    for i in range(0, exam.section_count):
        responses += get_responses_for_section(exam, i, session, current_question)
        current_question += len(responses)

    return responses

def get_edit_exam_context_data(context, exam, training_class):
    questions = get_exam_questions(exam)
    duration = exam.duration.seconds / 60

    context['exam_not_available'] = False

    context['trainingclass'] = training_class
    context['examname'] = exam.name
    context['is_open'] = bool(exam.is_open)
    context['is_final'] = bool(exam.category == 'F')
    context['duration'] = duration
    context['data'] = questions
    return context

# if exam is new, pk will be a negative value
def save_exam_creation(request, pk):
    exam_name = request.POST.get('examname', '')
    # bool(request.POST.get('exam-category')=='1')
    exam_category = request.POST.get('exam-category','')
    
    is_open = request.POST.get('is-open','')
    duration = timedelta(minutes=int(request.POST.get('duration','')))
    
    # questions are saved in an array
    question_prompt = request.POST.getlist('question-prompt')
    question_point = request.POST.getlist('question-point')
    question_type = request.POST.getlist('question-type')
    question_count = len(question_prompt)
    
    total_score = 0
    for point in question_point:
        total_score += int(point)

    section_index = 0
    instructions = "Place Holder"
    # section_index = int(request.POST.get('section-index', ''))
    # description = request.POST.get('description', '')

    question_hstore = {}
    for index, (prompt, points, qtype) in enumerate(zip(question_prompt, question_point, question_type)):
        qPack = {}
        qPack['prompt'] = prompt
        qPack['points'] = points
        qPack['type'] = qtype
        question_hstore[str(index+1)] = json.dumps(qPack)

    if pk < 0:
        training_class = Class.objects.get(id=request.POST.get('training-class'))
        exam = Exam(training_class=training_class,
            name=exam_name,
            is_open=is_open,
            duration=duration,
            category=exam_category,
            total_score=total_score)
        exam.save()
        section = Section(exam=exam,
            instructions=instructions,
            section_index=section_index,
            question_count=question_count)
    else:
        exam = Exam.objects.get(pk=pk)
        training_class = Class.objects.get(id=exam.training_class.id)
        exam.is_open = is_open
        exam.duration = duration
        exam.name = exam_name
        exam.category = exam_category
        exam.total_score = total_score
        exam.save()

        '''
        Modify to work for exams with multiple sections
        '''
        section = get_exam_section(exam, 0)

    section.questions = question_hstore
    section.question_count = question_count
    section.save()

def get_exam_context_data(context, exam, is_available, session, role):
    context['role'] = role
    context['exam'] = exam

    if not is_available:
        context['exam_available'] = False
        return context

    context['exam_available'] = True

    questions = get_exam_questions(exam)
    responses = get_responses(exam, session)

    context['data'] = zip(questions, responses)
    return context

def retake_available(exam, trainee):
    try:
        retake = Retake.objects.filter(exam=exam,
                                    trainee=trainee,
                                    is_complete=False)
        # implicit assumption here that there is only one retake possible
        if  retake and not retake[0].is_complete:
            return True
    except Retake.DoesNotExist:
        pass
    return False

def save_responses(session, section, responses):
    try:
        responses_obj = Responses.objects.get(session=session, section=section)
    except Responses.DoesNotExist:
        responses_obj = Responses(session=session, section=section, score=0)

    responses_hstore = responses_obj.responses
    if responses_hstore is None:
        responses_hstore = {}

    for index, response in enumerate(responses):
        responses_hstore[str(index+1)] = response

    responses_obj.responses = responses_hstore
    responses_obj.save()

def trainee_can_take_exam(trainee, exam):
    if exam.training_class.type == 'MAIN':
        return trainee.is_active
    elif exam.training_class.type == '1YR':
        return trainee.current_term <= 2
    elif exam.training_class.type == '2YR':
        return trainee.current_term >= 3
    else:
        return False  #NYI
