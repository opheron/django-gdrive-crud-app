# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import defaults as default_views
from django.contrib import messages
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError
from .google_api import build_google_service, get_gdrive_root_folder_items, delete_gdrive_file
from googleapiclient.http import MediaFileUpload
import django.utils.dateparse as dateparse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
import urllib.parse


import logging

logger = logging.getLogger("console")


def index(request):
    service = build_google_service(request)

    next_page_token_arg = request.GET.get('nextpagetoken')

    safe_next_page_token = None
    if next_page_token_arg is not None and len(next_page_token_arg) > 0:
        safe_next_page_token = urllib.parse.quote_plus(next_page_token_arg)

    safe_previous_page_token = None
    # if previous_page_token_arg is not None and len(previous_page_token_arg) > 0:
    #     safe_previous_page_token = urllib.parse.quote_plus(previous_page_token_arg)

    results = None
    try:
        # if safe_previous_page_token and safe_next_page_token:
        if safe_next_page_token:
            # results = get_gdrive_root_folder_items(service, safe_next_page_token)
            results = get_gdrive_root_folder_items(service, next_page_token_arg)
        else:
            results = get_gdrive_root_folder_items(service)
    except RefreshError as err:
        logger.warning(f"Couldn't refresh Google auth: {err}")
        messages.error(
            request,
            "Could not refresh auth credentials. Please sign back in and try again.")
        return HttpResponseRedirect('../')
    except HttpError as err:
        if err.status_code == 403:
            logger.info("Couldn't access Google API because user didn't provide sufficient permissions.")
            messages.error(
                request,
                "Insufficient permissions for Google DriveAPI - please sign in through OAuth again and grant permission!")
            return HttpResponseRedirect('../')

    folder_files = results.get('files', [])
    next_page_token = results.get('nextPageToken', None)

    for file in folder_files:
        file['modifiedTimeParsed'] = dateparse.parse_datetime(file['modifiedTime'])

    return render(
        request,
        "gdrivecrud/list.html",
        {
            'folder_files': folder_files,
            'next_page_token': next_page_token,
            'previous_page_token': safe_previous_page_token
        })

def delete(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        file_id = form_data.get("fileId", None)
        if file_id is None:
            messages.error(request, 'Form is invalid - missing fileId!')
            return HttpResponseRedirect('../')
        service = build_google_service(request)
        response = delete_gdrive_file(service, file_id)
        messages.success(request, 'File deleted successfully!')
        return HttpResponseRedirect('../')

def upload(request):
    if request.method == 'POST':
        import os
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings

        uploaded_file = request.FILES['newFile']
        path = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        service = build_google_service(request)

        file_metadata = {"name": uploaded_file.name}

        media = MediaFileUpload(tmp_file, mimetype=uploaded_file.content_type)

        drive_file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        messages.success(request, "File uploaded successfully!")
        return HttpResponseRedirect('../')


