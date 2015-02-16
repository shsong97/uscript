# -*- coding: utf-8 -*-

from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from scripts.models import Scripts, Tag
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.

login_url = '/scripts/login/'
ITEMS_PER_PAGE = 10
PAGE_GROUP = 10

from django.core.paginator import Paginator
from scripts.forms import RegistrationForm, UploadFileForm
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper


def home(request):
    return HttpResponseRedirect('/scripts')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/scripts')


def login_page(request):
    if request.POST:
        username = request.POST['id_username']
        password = request.POST['id_password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(request.POST['next'])
            else:
                # Return a 'disabled account' error message
                return HttpResponse("<script>alert('disabled accout'); window.location='/scripts/login';</script>")
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("<script>alert('invalid accout'); window.location='/scripts/login';</script>")

    return render_to_response('registration/login.html', RequestContext(request))


def register_success(request):
    return render_to_response('registration/register_success.html', RequestContext(request))


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            return HttpResponseRedirect('/scripts/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)


class DetailView(generic.DetailView):
    model = Scripts
    template_name = 'scripts/detail.html'

    def get_queryset(self):
        return Scripts.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        taglist = self.object.tag_set.all()
        tag_string = ','.join(
            tag.tag_title for tag in self.object.tag_set.all()
        )
        context['taglist'] = tag_string
        return context


class ScriptsUpdateView(generic.DetailView):
    model = Scripts
    template_name = 'scripts/update.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptsUpdateView, self).get_context_data(**kwargs)
        taglist = self.object.tag_set.all()
        tag_string = ','.join(
            tag.tag_title for tag in self.object.tag_set.all()
        )
        context['taglist'] = tag_string
        return context


class ScriptsCreate(CreateView):
    model = Scripts
    template_name = 'scripts/add.html'


@login_required(login_url=login_url)
@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request, request.FILES['file'])

            return HttpResponseRedirect('/scripts/')
    else:
        form = UploadFileForm()

    return render_to_response('scripts/upload.html', RequestContext(request, {'form': form}))


@csrf_protect
def handle_uploaded_file(request, f):
    contents = ""
    print f.charset
    for chunk in f.chunks():
        contents = contents + chunk.decode('euc-kr')

    scripts, dummy = Scripts.objects.get_or_create(
        title=f.name, user=request.user, contents=contents)


@login_required(login_url=login_url)
def scripts_update(request, scripts_id):
    scripts = get_object_or_404(Scripts, id=scripts_id)
    scripts.title = request.POST['title']

    if not scripts.title.__contains__('.sql'):
        scripts.title = scripts.title + '.sql'

    scripts.contents = request.POST['contents']

    taglist = request.POST['taglist'].split(',')

    scripts.tag_set.clear()

    for tag in taglist:
        tag_item, dummy = Tag.objects.get_or_create(tag_title=tag.strip())
        scripts.tag_set.add(tag_item)

    scripts.save()
    return HttpResponseRedirect(reverse('scripts:detail', args=(scripts_id,)))


@login_required(login_url=login_url)
def scripts_add(request):
    title = request.POST['title']

    if not title.__contains__('.sql'):
        title = title + '.sql'

    scripts = Scripts(
        title=title, contents=request.POST['contents'], user=request.user)
    scripts.save()

    taglist = request.POST['taglist'].split(',')

    scripts.tag_set.clear()

    for tag in taglist:
        tag_item, dummy = Tag.objects.get_or_create(tag_title=tag.strip())
        scripts.tag_set.add(tag_item)

    scripts.save()
    return HttpResponseRedirect('/scripts/')


@login_required(login_url=login_url)
def scripts_delete(request, scripts_id):
    scripts = get_object_or_404(Scripts, id=scripts_id)
    if scripts.user == request.user:
        scripts.delete()
    return HttpResponseRedirect('/scripts/')


def scripts_download(request, scripts_id):
    scripts = get_object_or_404(Scripts, id=scripts_id)
    title = scripts.title.encode('euc-kr')
    response = HttpResponse(content_type='plain/text')
    response['Content-Disposition'] = 'attachment; filename=' + title
    response.write(scripts.contents.encode('euc-kr'))
    return response


def search_page(request):
    scripts = []

    query_type = 'title'

    if request.POST.has_key('query_type'):
        query_type = request.POST['query_type']

    query = ""

    if request.POST.has_key('query'):
        query = request.POST['query'].strip()
        if query:
            keywords = query.split()
            q = Q()
            for keyword in keywords:
                if query_type == 'title':
                    q = q & Q(title__icontains=keyword)
                elif query_type == 'contents':
                    q = q & Q(contents__icontains=keyword)
                elif query_type == 'tag':
                    q = q & Q(tag_title__icontains=keyword)

            if query_type == 'tag':
                tags = [ tag.scripts.all() for tag in Tag.objects.filter(q) ]
                scripts = []
                for tag in tags:
                    for script in tag:
                        if not script in scripts:
                            scripts.append(script)
            else:
                scripts = Scripts.objects.filter(q).order_by('-pub_date')
        else:  # query is empty
            scripts = Scripts.objects.all().order_by('-pub_date')
    else:  # no query
        scripts = Scripts.objects.all().order_by('-pub_date')

    paginator = Paginator(scripts, ITEMS_PER_PAGE)

    page_group_total = int(paginator.num_pages / PAGE_GROUP)
    if paginator.num_pages % PAGE_GROUP > 0:
        page_group_total = page_group_total + 1

    try:
        page = int(request.POST['page'])
    except:
        page = 1

    page_group_no = int((page - 1) / PAGE_GROUP) + 1
    prev_page = 0
    next_page = 0

    if page_group_no < page_group_total:
        next_page = page_group_no * PAGE_GROUP + 1

    if page_group_total > 1 and page_group_no > 1:
        prev_page = (page_group_no - 1) * PAGE_GROUP

    if page_group_total == page_group_no:
        page_group_mod = paginator.num_pages - (page_group_no - 1) * PAGE_GROUP
    else:
        page_group_mod = PAGE_GROUP

    page_list = [
        (page_group_no - 1) * PAGE_GROUP + i + 1 for i in range(page_group_mod)]

    try:
        if paginator.num_pages < page:
            page = 1
        result_scripts = paginator.page(page)
    except:
        raise Http404

    variables = RequestContext(request, {
        'scripts_list': result_scripts,
        'query_type': query_type,
        'query': query,
        'show_paginator': paginator.num_pages > 1,
        'has_prev': prev_page > 0,
        'has_next': next_page > 0,
        'page': page,
        'page_list': page_list,
        'pages': paginator.num_pages,
        'next_page': next_page,
        'prev_page': prev_page})

    return render_to_response('scripts/index.html', variables)
