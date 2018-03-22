from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
from pod.video.models import Video
from pod.completion.models import Contributor
from pod.completion.forms import ContributorForm
from pod.completion.forms import DocumentForm
from pod.completion.forms import TrackForm

import json


@csrf_protect
def video_completion(request, slug):
    return HttpResponse('TODO')


@csrf_protect
def video_completion_contributor(request, slug):
    if not request.user.is_authenticated():
        raise PermissionDenied
    video = get_object_or_404(Video, slug=slug)
    if request.user != video.owner and not request.user.is_superuser:
        messages.add_message(
            request, messages.ERROR, _(u'You cannot complement this video.'))
        raise PermissionDenied

    list_contributor = video.contributor_set.all()
    list_track = video.track_set.all()
    list_document = video.document_set.all()
    list_overlay = video.overlay_set.all()

    if request.POST:
        if request.POST.get('action') and request.POST['action'] == 'new':
            form_contributor = ContributorForm(initial={'video': video})
            if request.is_ajax():
                return render(
                    request,
                    'contributor/form_contributor.html',
                    {'form_contributor': form_contributor,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'form_contributor': form_contributor,
                     'list_track': list_track,
                     'list_document': list_document,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'save':
            form_contributor = None
            if (request.POST.get('contributor_id') and
                    request.POST['contributor_id'] != 'None'):
                contributor = get_object_or_404(
                    Contributor, id=request.POST['contributor_id'])
                form_contributor = ContributorForm(
                    request.POST, instance=contributor)
            else:
                form_contributor = ContributorForm(request.POST)
            if form_contributor.is_valid():
                form_contributor.save()
                list_contributor = video.contributor_set.all()
                if request.is_ajax():
                    some_data_to_dump = {'list_data': render_to_string(
                        'contributor/list_contributor.html',
                        {'list_contributor': list_contributor,
                         'video': video},
                        request=request),
                    }
                    data = json.dumps(some_data_to_dump)
                    return HttpResponse(data, content_type='application/json')
                else:
                    return render(
                        request,
                        'videos/video_completion.html',
                        {'video': video,
                         'list_contributor': list_contributor,
                         'list_document': list_document,
                         'list_track': list_track,
                         'list_overlay': list_overlay})
            else:
                if request.is_ajax():
                    some_data_to_dump = {
                        'errors': '{0}'.format(_('Please correct errors')),
                        'form': render_to_string(
                            'contributor/form_contributor.html',
                            {'video': video,
                             'form_contributor': form_contributor},
                            request=request)
                    }
                    data = json.dumps(some_data_to_dump)
                    return HttpResponse(data, content_type='application/json')
                else:
                    return render(
                        request,
                        'video_completion.html',
                        {'video': video,
                         'list_contributor': list_contributor,
                         'form_contributor': form_contributor,
                         'list_document': list_document,
                         'list_track': list_track,
                         'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'modify':
            contributor = get_object_or_404(
                Contributor, id=request.POST['id'])
            form_contributor = ContributorForm(instance=contributor)
            if request.is_ajax():
                return render(
                    request,
                    'contributor/form_contributor.html',
                    {'form_contributor': form_contributor,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'form_contributor': form_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'delete':
            contributor = get_object_or_404(
                Contributor, id=request.POST['id'])
            contributor_delete = contributor.delete()
            list_contributor = video.contributor_set.all()
            if request.is_ajax():
                some_data_to_dump = {
                    'list_data': render_to_string(
                        'contributor/list_contributor.html',
                        {'list_contributor': list_contributor,
                         'video': video},
                        request=request)
                }
                data = json.dumps(some_data_to_dump)
                return HttpResponse(data, content_type='application/json')
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_document': list_document,
                     'list_track': list_track,
                     'list_overlay': list_overlay})

    return render(
        request,
        'video_completion.html',
        {'video': video,
         'list_contributor': list_contributor,
         'list_document': list_document,
         'list_track': list_track,
         'list_overlay': list_overlay})


@csrf_protect
def video_completion_document(request, slug):
    if not request.user.is_authenticated():
        raise PermissionDenied
    video = get_object_or_404(Video, slug=slug)
    if request.user != video.owner and not request.user.is_superuser:
        messages.add_message(
            request, messages.ERROR, _(u'You cannot complement this video.'))
        raise PermissionDenied

    list_contributor = video.contributor_set.all()
    list_document = video.document_set.all()
    list_track = video.track_set.all()
    list_overlay = video.overlay_set.all()

    if request.POST:
        if request.POST.get('action') and request.POST['action'] == 'new':
            form_document = DocumentForm(initial={'video': video})
            if request.is_ajax():
                return render(
                    request,
                    'document/form_document.html',
                    {'form_document': form_document,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'form_document': form_document,
                     'list_track': list_track,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'save':
            form_document = None
            if (request.POST.get('document_id') and
                    request.POST['document_id'] != 'None'):
                document = get_object_or_404(
                    Document, id=request.POST['document_id'])
                form_document = DocumentForm(request.POST, instance=document)
                else:
                    form_document = DocumentForm(request.POST)
                if form_document.is_valid():
                    form_document.save()
                    list_document = video.document_set.all()
                    if request.is_ajax():
                        some_data_to_dump = {
                            'list_data': render_to_string(
                                'document/list_document.html',
                                {'list_document': list_document,
                                 'video': video},
                                request=request)
                        }
                        data = json.dumps(some_data_to_dump)
                        return HttpResponse(
                            data,
                            content_type='application/json')
                    else:
                        return render(
                            request,
                            'video_completion.html',
                            {'video': video,
                             'list_contributor': list_contributor,
                             'list_document': list_document,
                             'list_track': list_track,
                             'list_overlay': list_overlay})
                else:
                    if request.is_ajax():
                        some_data_to_dump = {
                            'errors': '{0}'.format(_('Please correct errors')),
                            'form': render_to_string(
                                'document/form_document.html',
                                {'video': video,
                                 'form_document': form_document},
                                request=request)
                        }
                        data = json.dumps(some_data_to_dump)
                        return HttpResponse(
                            data,
                            content_type='application/json')
                    else:
                        return render(
                            request,
                            'video_completion.html',
                            {'video': video,
                             'list_contributor': list_contributor,
                             'list_document': list_document,
                             'list_track': list_track,
                             'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'modify':
            document = get_object_or_404(Document, id=request.POST['id'])
            form_document = DocumentForm(instance=document)
            if request.is_ajax():
                return render(
                    request,
                    'document/form_document.html',
                    {'form_document': form_document,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'form_document': form_document,
                     'list_track': list_track,
                     'list_overlay'})

        if request.POST.get('action') and request.POST['action'] == 'delete':
            document = get_object_or_404(Document, id=request.POST['id'])
            document_delete = document.delete()
            list_document = video.document_set.all()
            if request.is_ajax():
                some_data_to_dump = {
                    'list_data': render_to_string(
                        'document/list_document.html',
                        {'list_document': list_document,
                         'video': video},
                        request=request)
                }
                data = json.dumps(some_data_to_dump)
                return HttpResponse(data, content_type='application/json')
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'list_overlay': list_overlay})

    return render(
        request,
        'video_completion.html',
        {'video': video,
         'list_contributor': list_contributor,
         'list_document': list_document,
         'list_track': list_track,
         'list_overlay': list_overlay})


@csrf_protect
def video_completion_track(request, slug):
    if not request.user.is_authenticated() or not request.user.is_staff:
        raise PermissionDenied
    video = get_object_or_404(Video, slug=slug)
    if request.user != video.owner and not request.user.is_superuser:
        messages.add_message(
            request, messages.ERROR, _(u'You cannot complement this video.'))
        raise PermissionDenied

    list_contributor = video.contributor_set.all()
    list_track = video.track_set.all()
    list_document = video.document_set.all()
    list_overlay = video.overlay_set.all()

    if request.POST:
        if request.POST.get('action') and request.POST['action'] == 'new':
            form_track = TrackForm(initial={'video': video})
            if request.is_ajax():
                return render(
                    request,
                    'track/form_track.html',
                    {'form_track': form_track,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'form_track': form_track,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'save':
            form_track = None
            if (request.POST.get('track_id') and
                    request.POST['track_id'] != 'None'):
                track = get_object_or_404(
                    Track, id=request.POST['track_id'])
                form_track = TrackForm(request.POST, instance=track)
            else:
                form_track = TrackForm(request.POST)
            if form_track.is_valid():
                form_track.save()
                list_track = video.track_set.all()
                if request.is_ajax():
                    some_data_to_dump = {'list_data': render_to_string(
                        'track/list_track.html',
                        {'list_track': list_track,
                         'video': video},
                        request=request)
                    }
                    data = json.dumps(some_data_to_dump)
                    return HttpResponse(data, content_type='application/json')
                else:
                    return render(
                        request,
                        'video_completion.html',
                        {'video': video,
                         'list_contributor': list_contributor,
                         'list_document': list_document,
                         'list_track': list_track,
                         'list_overlay': list_overlay})
        else:
            if request.is_ajax():
                some_data_to_dump = {
                    'errors': '{0}'.format('Please correct errors'),
                    'form': render_to_string(
                        'track/form_track.html',
                        {'video': video,
                         'form_track': form_track},
                        request=request)
                }
                data = json.dumps(some_data_to_dump)
                return HttpResponse(data, content_type='application/json')
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'form_track': form_track,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'modify':
            track = get_object_or_404(Track, id=request.POST['id'])
            form_track = TrackForm(instance=track)
            if request.is_ajax():
                return render(
                    request,
                    'track/form_track.html',
                    {'form_track': form_track,
                     'video': video})
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'form_track': form_track,
                     'list_overlay': list_overlay})

        if request.POST.get('action') and request.POST['action'] == 'delete':
            track = get_object_or_404(Track, id=request.POST['id'])
            track_delete = track.delete()
            list_track = video.track_set.all()
            if request.is_ajax():
                some_data_to_dump = {
                    'list_data': render_to_string(
                        'track/list_track.html',
                        {'list_track': list_track,
                         'video': video},
                        request=request)
                }
                data = json.dumps(some_data_to_dump)
                return HttpResponse(data, content_type='application/json')
            else:
                return render(
                    request,
                    'video_completion.html',
                    {'video': video,
                     'list_contributor': list_contributor,
                     'list_document': list_document,
                     'list_track': list_track,
                     'list_overlay': list_overlay})

    return render(
        request,
        'video_completion.html',
        {'video': video,
         'list_contributor': list_contributor,
         'list_document': list_document,
         'list_track': list_track,
         'list_overlay': list_overlay})


@csrf_protect
def video_completion_overlay(request, slug):
    return HttpResponse('TODO')
