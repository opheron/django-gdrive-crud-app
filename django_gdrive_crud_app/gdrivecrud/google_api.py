from typing import Optional

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google.auth.transport.requests import Request

import logging

logger = logging.getLogger("console")

def build_google_service(request) -> Resource | None:
    """Use user info from allauth to build Google API service """

    logger.debug(f"Building Google Service...")

    # TODO: Fix to use current user's Social Token
    current_user = request.user
    social_account = SocialAccount.objects.get(user=current_user)
    token = SocialToken.objects.filter(account=social_account.id).first()

    # use SocialApp to get client info
    client = SocialApp.objects.get(
        provider='google'
    )

    scopes = [
        'profile',
        'email',
        'https://www.googleapis.com/auth/drive'  # include gdrive API scope to ensure permissions request
    ]

    credentials = Credentials(
        token=token.token,
        refresh_token=token,
        scopes=scopes,
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=client.client_id,
        client_secret=client.secret)

    # refresh credentials if invalid or expired
    if not credentials.valid or credentials.expired:
        if credentials.refresh_token:
            token.token_secret = credentials.refresh_token

    token.token = credentials.token
    token.save()

    service = build('drive', 'v3', credentials=credentials)
    return service


def get_gdrive_root_folder_items(service, next_page_token=None) -> list | None:
    list_kwarg_params = {
        "fields": "nextPageToken, files(id, name, modifiedTime, kind, mimeType, webContentLink, webViewLink, fileExtension, exportLinks)",
        # "q": "mimeType != 'application/vnd.google-apps.folder' and trashed = false",
        "q": "trashed = false",
        "orderBy": "modifiedTime desc,folder,name",
        "pageSize": 5,
    }
    if next_page_token is not None:
        list_kwarg_params['pageToken'] = next_page_token
    results = (
        service.files()
        .list(
            **list_kwarg_params
            # fields="nextPageToken, files(id, name, modifiedTime, kind, mimeType, webContentLink, webViewLink, fileExtension, exportLinks)",
            # # q="'root' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false",
            # q="mimeType != 'application/vnd.google-apps.folder' and trashed = false",
            # orderBy="modifiedTime desc,folder,name",
        )
        .execute()
    )
    items = results.get("files", None)

    if not items:
        return None

    return results

def delete_gdrive_file(service, file_id) -> bool:

    body_value = {'trashed': True}
    response = service.files().update(fileId=file_id, body=body_value).execute()
    return response
