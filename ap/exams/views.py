import datetime
import json

from braces.views import LoginRequiredMixin
from collections import namedtuple
from datetime import timedelta
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.fields import HStoreField
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_select2 import *
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from aputils.utils import trainee_from_user
from terms.models import Term

from .forms import ExamCreateForm
from .models import Class
from .models import Trainee
from .models import Exam, Section, Session, Responses, Retake

from django.contrib.postgres.fields import HStoreField
from exams.utils import get_responses, get_exam_questions, get_edit_exam_context_data, \
    save_exam_creation, get_exam_context_data, retake_available, save_responses, \
    get_exam_section, trainee_can_take_exam

# PDF generation
import cStringIO as StringIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from cgi import escape

class ExamCreateView(LoginRequiredMixin, FormView):

    template_name = 'exams/exam_form.html'
    form_class = ExamCreateForm
    success_url = reverse_lazy('exams:list')

    def get_context_data(self, **kwargs):
        context = super(ExamCreateView, self).get_context_data(**kwargs)

        classes = Class.objects.filter(term=Term.current_term())
        context['exam_not_available'] = True
        context['classes'] = classes
        return context

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()

            for section_form in formset.forms:
                section = Section(exam=self.object, question_count=0)
                section.save()
        else:
            pass
        return super(ExamCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        # -1 value indicates exam is newly created
        save_exam_creation(request, -1)
        messages.success(request, 'Exam created.')
        return HttpResponseRedirect(reverse_lazy('exams:list'))

class ExamEditView(ExamCreateView, FormView):

    template_name = 'exams/exam_form.html'
    form_class = ExamCreateForm
    success_url = reverse_lazy('exams:list')

    def get_context_data(self, **kwargs):
        context = super(ExamEditView, self).get_context_data(**kwargs)
        exam = Exam.objects.get(pk=self.kwargs['pk'])
        training_class = Class.objects.get(id=exam.training_class.id)
        
        return get_edit_exam_context_data(context, exam, training_class)

    def get_form(self, form_class):
        return super(ExamCreateView, self).get_form(form_class)

    def form_valid(self, form):
        return super(ExamCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        pk=self.kwargs['pk']
        save_exam_creation(request, pk)
        messages.success(request, 'Exam saved.')  
        return HttpResponseRedirect(reverse_lazy('exams:list'))
      

class ExamTemplateListView(ListView):
    template_name = 'exams/exam_template_list.html'
    model = Exam
    context_object_name = 'exam_templates'

    def get_queryset(self):
        return Exam.objects.all()

    def exam_in_retakes(self, retakes, exam):
        for retake in retakes:
            if retake.exam == exam and not retake.is_complete:
                return True
        return False

    def get_context_data(self, **kwargs):
        # TODO: there's gotta be a better way of doing this
        context = super(ExamTemplateListView, self).get_context_data(**kwargs)
        context['available'] = []
        user = self.request.user
        retakes = Retake.objects.filter(trainee=user, 
                                            is_complete=False)
        for exam in Exam.objects.all():
            if trainee_can_take_exam(user, exam) and \
                ((not exam.has_trainee_completed(user)) or \
                    (self.exam_in_retakes(retakes, exam))):
                context['available'].append(True)
            else:
                context['available'].append(False)
        return context

class SingleExamGradesListView(CreateView, SuccessMessageMixin):
    template_name = 'exams/single_exam_grades.html'
    model = Exam
    context_object_name = 'exam_grades'
    fields = []
    success_url = reverse_lazy('exams:list')
    success_message = 'Exam grades updated.'

    def get_context_data(self, **kwargs):
        context = super(SingleExamGradesListView, self).get_context_data(**kwargs)
        exam = Exam.objects.get(pk=self.kwargs['pk'])
        context['exam'] = exam

        first_sessions = []
        second_sessions = []

        if exam.training_class.type == 'MAIN':
            trainees = Trainee.objects.filter(is_active=True).order_by('lastname')
        elif exam.training_class.type == '1YR':
            trainees = Trainee.objects.filter(is_active=True, current_term__lte=2)
        elif exam.training_class.type == '2YR':
            trainees = Trainee.objects.filter(is_active=True, current_term__gte=3)

        # TODO: Is there a more efficient way of doing this?  Prefetch_related,
        # maybe?  Is there a way to apply a filter to prefetch related?
        for trainee in trainees:
            try:
                sessions = Session.objects.filter(exam=exam, is_complete=True, 
                    trainee=trainee).order_by('trainee__lastname')
                if sessions.count() > 0:
                    first_sessions.append(sessions[0])
                else:
                    first_sessions.append(None)

                if sessions.count() > 1:
                    second_sessions.append(sessions[sessions.count() - 1])
                else:
                    second_sessions.append(None)
            except Session.DoesNotExist:
                first_sessions.append(None)
                second_sessions.append(None)

        context['data'] = zip(trainees, first_sessions, second_sessions)
        return context

    def post(self, request, *args, **kwargs):
        # User Error?
        if request.method != 'POST':
            messages.add_message(request, messages.ERROR, 'Nothing saved.')
            return redirect('exams:exams_template_list')

        if 'delete-session-id' in request.POST:
            session_id = int(request.POST['delete-session-id'])
            try:
                Session.objects.get(id=session_id).delete()
            except Session.DoesNotExist:
                pass
            messages.success(request, 'Exam deleted')
        elif 'unfinalize-session-id' in request.POST:
            session_id = int(request.POST['unfinalize-session-id'])

            try:
                session = Session.objects.get(id=session_id)
                session.is_graded = False
                session.save()

                if session.is_submitted_online:
                    return HttpResponseRedirect(
                        reverse_lazy('exams:grade', kwargs={'pk': session.id}))
            except Session.DoesNotExist:
                pass
        elif 'retake-trainee-id' in request.POST:
            trainee_id = int(request.POST['retake-trainee-id'])
            try:
                trainee = Trainee.objects.get(id=trainee_id)
                exam = Exam.objects.get(pk=self.kwargs['pk'])
                Retake.objects.get_or_create(trainee=trainee, exam=exam)
            except Trainee.DoesNotExist:
                pass
        else:
            grades = request.POST.getlist('new-grade')
            trainee_ids = request.POST.getlist('trainee-id')
            for index, trainee_id in enumerate(trainee_ids):
                try:
                    trainee = Trainee.objects.get(id=trainee_id)
                    exam = Exam.objects.get(pk=self.kwargs['pk'])
                    if grades[index] == "":
                        continue

                    if not grades[index].isdigit():
                        messages.add_message(request, messages.ERROR, 
                            'Invalid input for trainee ' + str(trainee))
                        continue

                    try:
                        sessions = Session.objects.filter(
                            exam=exam, 
                            is_complete=True, 
                            trainee=trainee).order_by('-retake_number')

                        if (sessions.count() == 0):
                            retake_number = 0
                        else:
                            retake_number = sessions[0].retake_number + 1
                    except Session.DoesNotExist:
                        retake_number = 0

                    session = Session(exam=exam, 
                        trainee=trainee,
                        is_submitted_online=False,
                        is_complete=True,
                        is_graded=True,
                        retake_number=retake_number,
                        grade=int(grades[index]))
                    session.save()
                except Trainee.DoesNotExist:
                    pass

            grades2 = request.POST.getlist('session-id-grade')
            session_ids = request.POST.getlist('session-id')

            for index, session_id in enumerate(session_ids):
                try:
                    session = Session.objects.get(id=session_id)
                    grade = int(grades2[index]) if grades2[index].isdigit() else 0
                    session.grade = grade
                    session.save()
                except Session.DoesNotExist:
                    pass
            messages.success(request, 'Exam grades saved.')

        return self.get(request, *args, **kwargs)

class GenerateGradeReports(CreateView, SuccessMessageMixin):
    model = Session
    template_name = 'exams/exam_grade_reports.html'
    success_url = reverse_lazy('exams:exam_grade_reports')

    def get_context_data(self, **kwargs):
        context = super(GenerateGradeReports, self).get_context_data(**kwargs)
        context['trainee_select_form'] = TraineeSelectForm()
        context['trainees'] = TraineeSelectForm
        trainee_list = self.request.GET.getlist('trainees')
        sessions = {}
        for trainee in trainee_list:
            try:
                sessions[Trainee.objects.get(id=trainee)] = \
                    Session.objects.filter(trainee_id=trainee)
            except Session.DoesNotExist:
                sessions[trainee] = {}                
        context['sessions'] = sessions
        return context

class GenerateOverview(DetailView):
    template_name = 'exams/exam_overview.html'
    model = Exam
    fields = []
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        context = super(GenerateOverview, self).get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(pk=self.kwargs['pk'])
        exam_stats = context['exam'].statistics()
        context['exam_max'] = exam_stats['maximum']
        context['exam_min'] = exam_stats['minimum']
        context['exam_average'] = exam_stats['average']
        try:
            context['sessions'] = Session.objects.filter(exam=context['exam']).order_by('trainee__lastname')
        except Session.DoesNotExist:
            context['sessions'] = []
        return context

class ExamRetakeView(DetailView):
    model = Exam
    context_object_name = 'exam'

    def get_context_data(self, **kwargs):
        context = super(ExamRetakeView, self).get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(pk=self.kwargs['pk'])
        try:
            context['sessions'] = Session.objects.filter(exam=context['exam']).order_by('trainee__lastname')
        except Session.DoesNotExist:
            context['sessions'] = []
        return context

    # pip install pisa, html5lib, pypdf, pdf
    def get(self, request, *args, **kwargs):
        template = get_template('exams/exam_retake_list.html')
        self.object = self.get_object()
        context = super(ExamRetakeView, self).get_context_data(**kwargs)
        html = template.render(context)
        result = StringIO.StringIO()
        
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), mimetype = 'application/pdf')
        return HttpResponse('There were some errors<pre>%s</pre>' %escape(html))

class TakeExamView(SuccessMessageMixin, CreateView):
    template_name = 'exams/exam.html'
    model = Session
    context_object_name = 'exam'
    fields = []

    def _get_exam(self):
        return Exam.objects.get(pk=self.kwargs['pk'])

    def _get_most_recent_session(self):
        try:
            sessions = Session.objects.filter(
                exam=self._get_exam(), 
                trainee=self.request.user).order_by('-id')
            if sessions:
                return sessions[0]
        except Session.DoesNotExist:
            pass

        return None

    def _get_session(self):
        if not self._exam_available():
            return None

        session = self._get_most_recent_session()
        # Create a new exam session if there is no editable exam session
        if session == None or session.is_complete:
            retake_count = session.retake_number + 1 if session != None else 0
            new_session = Session(exam=self._get_exam(), 
                trainee=trainee_from_user(self.request.user),
                is_complete=False,
                is_submitted_online=True,
                retake_number=retake_count)
            if session != None:
                new_session.grade = session.grade
            new_session.save()

            # copy over previous responses
            if session != None:
                responses = Responses.objects.filter(session=session)
                for response in responses:
                    response.pk = None
                    response.session = new_session
                    response.save()

        return session

    def _exam_available(self):
        exam = self._get_exam()
        user = self.request.user

        if not trainee_can_take_exam(user, exam):
            return False

        # if the exam is in progress or doesn't exist, we're in business
        most_recent_session = self._get_most_recent_session()

        if (most_recent_session == None or not most_recent_session.is_complete):
            return True

        return retake_available(exam, user)

    def _is_retake(self):
        return self._get_session().retake_number > 0

    def get_context_data(self, **kwargs):
        context = super(TakeExamView, self).get_context_data(**kwargs)

        return get_exam_context_data(context, 
                                     self._get_exam(), 
                                     self._exam_available(), 
                                     self._get_session(), 
                                     "Retake" if self._is_retake() else "Take")

    def post(self, request, *args, **kwargs):
        is_successful = True
        finalize = False
        if 'Submit' in request.POST:
            finalize = True

        trainee = self.request.user
        exam = self._get_exam()
        session = self._get_session()

        # TODO: for now, only supporting 1-sectioned exams
        try:
            section = Section.objects.get(exam=exam, section_index=0)
        except Section.DoesNotExist:
            is_successful = False

        responses = request.POST.getlist('response_json')
        save_responses(session, section, responses)

        if finalize:
            session = self._get_session()
            session.is_complete = True
            session.save()

            # Grader's request is that eventually this would be displayed as a list for 
            # their reference, so instead of deleting, just mark as complete
            # try:
            #     retake = Retake.objects.filter(exam=exam, trainee=trainee)
            #     if retake:
            #         retake[0].is_complete = True
            #         retake[0].save()
            # except Retake.DoesNotExist:
            #     pass

            try:
                retake = Retake.objects.filter(exam=exam, trainee=trainee).delete()
            except Retake.DoesNotExist:
                pass

            messages.success(request, 'Exam submitted successfully.')
            return HttpResponseRedirect(reverse_lazy('exams:list'))
        else:
            messages.success(request, 'Exam progress saved.')
            return self.get(request, *args, **kwargs)        

class GradeExamView(SuccessMessageMixin, CreateView):
    template_name = 'exams/exam.html'
    model = Session
    context_object_name = 'exam'
    fields = []

    def _get_exam(self):
        session = Session.objects.get(pk=self.kwargs['pk'])
        return Exam.objects.get(pk=session.exam.id)

    def _get_session(self):
        return Session.objects.get(pk=self.kwargs['pk'])

    def _exam_available(self):
        # TODO: should sanity check that user has grader/TA permissions
        return True

    def get_context_data(self, **kwargs):
        context = super(GradeExamView, self).get_context_data(**kwargs)

        return get_exam_context_data(context, 
                                     self._get_exam(), 
                                     self._exam_available(), 
                                     self._get_session(), 
                                     "Grade")

    # Returns true if every score has a valid value
    def calculate_score(self, request, responses, session, section):
        total_score = 0
        can_finalize = True
        for index, response in enumerate(responses):
            response_parsed = json.loads(response);
            if (response_parsed["score"].isdigit()):
                total_score += int(response_parsed["score"])
            else:
                can_finalize = False
                if response_parsed["score"] != "":
                    messages.add_message(request, messages.ERROR, 
                        "Invalid grade value for question" + str(index + 1) + ".")

        try:
            responses_obj = Responses.objects.get(session=session, section=section)
        except Responses.DoesNotExist:
            responses_obj = Responses(session=session, section=section, score=0)

        if (responses_obj.score != total_score):
            session.grade = session.grade - responses_obj.score + total_score
            session.save()

            responses_obj.score = total_score;
            responses_obj.save()

        return can_finalize

    def post(self, request, *args, **kwargs):
        is_successful = True
        finalize = False
        if 'Submit' in request.POST:
            finalize = True
       
        session = Session.objects.get(pk=self.kwargs['pk'])
        exam = Exam.objects.get(pk=session.exam.id)

        # TODO: for now, only supporting 1-sectioned exams
        try:
            section = Section.objects.get(exam=exam, section_index=0)
        except Section.DoesNotExist:
            is_successful = False

        responses = request.POST.getlist('response_json')
        save_responses(session, section, responses)

        if (not self.calculate_score(request, responses, session, section)) and finalize:
            finalize = False
            messages.add_message(request, messages.ERROR, 
                "Cannot finalize grading: at least one invalid grade value.")

        if finalize:
            session = self._get_session()
            session.is_graded = True
            session.save()

            messages.success(request, 'Exam grading submitted successfully.')
            return HttpResponseRedirect(reverse_lazy('exams:grades', 
                                            kwargs={'pk': exam.id}))
        else:
            messages.success(request, 'Exam grading progress saved.')
            return self.get(request, *args, **kwargs)
