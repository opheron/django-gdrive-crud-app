# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import defaults as default_views
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError
from .google_api import build_google_service, get_gdrive_root_folder_items

import logging
logger = logging.getLogger("console")

def index(request):
    return HttpResponse("Hello, world. You're at the gdrivecrud index.")

def list(request):
    logger.warning("Test debug")
    service = build_google_service()

    try:
        results = get_gdrive_root_folder_items(service)
    except RefreshError as err:
        logger.warning(f"Couldn't refresh Google auth: {err}")
        return redirect(default_views.server_error)
    except HttpError as err:
        if err.status_code == 403:
            logger.info("Couldn't access Google API because user didn't provide sufficient permissions.")
            return render(
                request,
                "gdrivecrud/errors.html",
                {
                    "err": err
                }
            )
        return redirect(default_views.server_error)


        # service = build_google_service()
        # results = get_gdrive_root_folder_items(service)

    folder_files = results.get('files', [])
    print(f"{folder_files=}")
    next_page_token = results.get('nextPageToken', None)

    return render(
        request,
        "gdrivecrud/list.html",
        {
            'folder_files': folder_files,
            'next_page_token': next_page_token
        })


# def read(request):
#     return HttpResponse("Reading!")
def read(request):
    # from googleapiclient.discovery import build
    # from google.oauth2.credentials import Credentials
    # from allauth.socialaccount.models import SocialToken, SocialApp
    #
    # # request is the HttpRequest object
    # token = SocialToken.objects.get(
    #     account_id=request.user.id,
    #     # app="sociallogin"
    # )
    #
    # credentials = Credentials(
    #     token=token.token,
    #     refresh_token=token.token_secret,
    #     token_uri="https://oauth2.googleapis.com/token",
    #     client_id="246390019067-00it2n44efq8rj2alkdo9i2agcg682ra.apps.googleusercontent.com",  # replace with yours
    #     client_secret="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",
    # )  # replace with yours
    # from google.auth.transport.requests import Request
    #
    # if creds.refresh_token:
    #     token.token_secret = creds.refresh_token
    #
    # token.token = creds.token
    # token.save()
    # service = build("drive", "v3", credentials=credentials)
    # print(f"{service=}")
    # return HttpResponse("Hello, world. You're at the gdrivecrud list.")
    from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token = SocialToken.objects.get(pk=1)
    # # token = SocialToken.objects.all()
    # all_socialtokens = list(SocialToken.objects.all())
    # print(f"{all_socialtokens=}")
    # print(f"{request.user=}")
    # print("here")
    # for t in all_socialtokens:
    #     print("here")
    #     print(f"{t=}")
    # # print(f"{token.get()=}")
    client = SocialApp.objects.get(
        provider='google')  # assuming you use SocialApp entries, otherwise use django.conf.settings entry.

    scopes = ['profile', 'email']

    creds = Credentials(
        token=token.token,
        refresh_token=token,
        scopes=scopes,
        token_uri='https://accounts.google.com/o/oauth2/token',

        client_id=client.client_id,
        client_secret=client.secret)
    print(f"{creds=}")

    service = build('drive', 'v3', credentials=creds)
    print(f"{service=}")

    # Call the Drive v3 API
    # results = (
    #     service.files()
    #     .list(pageSize=20, fields="nextPageToken, files(id, name)")
    #     .execute()
    # )
    # items = results.get("files", [])
    #
    # if not items:
    #     print("No files found.")
    #     return
    # print("Files:")
    # for item in items:
    #     print(f"{item['name']} ({item['id']})")

    #### more results
    results = (
        service.files()
        .list(
            pageSize=5,
            fields="nextPageToken, files(id, name)",
            q="'root' in parents",
            orderBy="folder,name,modifiedTime desc",
        )
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    print("Files:")
    for item in items:
        print(f"{item['name']} ({item['id']})")

    print(f"{results.items()=}")
    next_page_token = results.get("nextPageToken", "None")
    print(f"{next_page_token=}")
    more_results = (
        service.files()
        .list(
            pageSize=5,
            fields="nextPageToken, files(id, name)",
            q="'root' in parents",
            orderBy="folder,name,modifiedTime desc",
            pageToken=next_page_token,
            # q=f"pageToken={next_page_token}"
        )
        .execute()
    )
    print("more results!")
    more_items = more_results.get("files", [])
    if not more_items:
        print("No files found.")
        return
    print("Files:")
    for item in more_items:
        print(f"{item['name']} ({item['id']})")

    # from googleapiclient.errors import HttpError
    #
    # except HttpError as error:
    # # TODO(developer) - Handle errors from drive API.
    # print(f"An error occurred: {error}")

    return HttpResponse("Hello, world. You're at the gdrivecrud read page.")
