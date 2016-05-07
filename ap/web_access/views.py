from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from .forms import WebAccessRequestCreateForm, WebAccessRequestTACommentForm
from .models import WebRequest
from accounts.models import User


class WebAccessCreate(generic.CreateView):
    model = WebRequest
    template_name = 'web_access/web_access_create.html'
    form_class = WebAccessRequestCreateForm

    def form_valid(self, form):
        req = form.save(commit=False)
        user = User.objects.get(id=self.request.user.id)
        req.trainee = user.trainee
        req.save()
        return super(WebAccessCreate, self).form_valid(form)


class WebAccessUpdate(generic.UpdateView):

    model = WebRequest
    template_name = 'web_access/web_access_update.html'
    form_class = WebAccessRequestCreateForm


class WebAccessDelete(generic.DeleteView):

    model = WebRequest


class WebAccessDetail(generic.DetailView):

    model = WebRequest
    template_name = 'web_access/web_access_detail.html'
    context_object_name = 'web_access'


class WebRequestList(generic.ListView):

    model = WebRequest
    template_name = 'web_access/webrequest_list.html'

    def get_queryset(self):
        return WebRequest.objects.filter(trainee=self.request.user.trainee.id).order_by('status')


class TAWebRequestList(generic.ListView):

    model = WebRequest
    template_name = 'web_access/ta_webrequest_list.html'
    context_object_name = 'web_access'

    def get_queryset(self):
        return WebRequest.objects.filter(status__in=['P', 'F']).order_by('date_assigned')


class TAWebAccessUpdate(generic.UpdateView):

    model = WebRequest
    template_name = 'web_access/ta_web_access_update.html'
    form_class = WebAccessRequestTACommentForm
    context_object_name = 'web_access'


def modify_status(request, status, id):
    """ Changes status of web access request """
    webRequest = get_object_or_404(WebRequest, pk=id)
    webRequest.status = status
    webRequest.save()
    webRequest = get_object_or_404(WebRequest, pk=id)
    message = "%s's %s web request was " % (webRequest.trainee, webRequest.get_reason_display())
    if status == 'A':
        message += 'approved.'
    if status == 'D':
        message += 'denied.'
    if status == 'F':
        message += 'marked for fellowship.'
    messages.add_message(request, messages.SUCCESS, message)

    return redirect('web_access:ta-web_access-list')
