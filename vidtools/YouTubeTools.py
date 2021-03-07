'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2021-03-06 11:56:04
 # @ Description:
 '''

try:
    # Python 2
    import httplib
except:
    # Python 3
    import http.client as httplib
import httplib2
import os
import random
import sys
import time

import apiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# TODO get_authenticated_service should accept kwargs
# TODO check authentication json works in /private directory loction

class YouTubeTools():
    '''
    Helper class to make uploading to YouTube easier
    Wrapper class for Google Api Python Client:
        https://developers.google.com/youtube/v3/guides/uploading_a_video

    Make sure to include your client_secrets.json file in vidtools directory!
    '''
    def __init__(self, **kwargs):
        '''
        file (str) path: This argument identifies the location of the video file that you are uploading.
        title (str): The title of the video that you are uploading. 
            The default value is Test title
        description (str): The description of the video that you're uploading. 
            The default value is Test description
        category (str): The category ID for the YouTube video category associated with the video. 
            The default value is 22, which refers to the People & Blogs category
            https://developers.google.com/youtube/v3/docs/videoCategories/list
        keywords (str): A comma-separated list of keywords associated with the video. 
            The default value is an empty string
        privacyStatus (str): The privacy status of the video. 
            The default behavior is for an uploaded video to be publicly visible (public). 
            When uploading test videos, you may want to specify a --privacyStatus argument 
            value to ensure that those videos are private or unlisted. 
            Valid values are public, private, and unlisted
        '''
        # Explicitly tell the underlying HTTP transport library not to retry, since
        # we are handling retry logic ourselves.
        httplib2.RETRIES = 1

        # Maximum number of times to retry before giving up.
        self.MAX_RETRIES = 10

        # Always retry when these exceptions are raised.
        self.RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
            httplib.IncompleteRead, httplib.ImproperConnectionState,
            httplib.CannotSendRequest, httplib.CannotSendHeader,
            httplib.ResponseNotReady, httplib.BadStatusLine
            )

        # Always retry when an apiclient.errors.HttpError with one of these status
        # codes is raised.
        self.RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

        # The self.CLIENT_SECRETS_FILE variable specifies the name of a file that contains
        # the OAuth 2.0 information for this application, including its client_id and
        # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
        # the Google API Console at
        # https://console.developers.google.com/.
        # Please ensure that you have enabled the YouTube Data API for your project.
        # For more information about using OAuth2 to access the YouTube Data API, see:
        #   https://developers.google.com/youtube/v3/guides/authentication
        # For more information about the client_secrets.json file format, see:
        #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        self.CLIENT_SECRETS_FILE = "/private/youtube_client_secrets.json"

        # This OAuth 2.0 access scope allows an application to upload files to the
        # authenticated user's YouTube channel, but doesn't allow other types of access.
        self.YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

        # This variable defines a message to display if the self.CLIENT_SECRETS_FILE is
        # missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

        %s

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        self.CLIENT_SECRETS_FILE))

        self.VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

    def get_authenticated_service(self, args):
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE,
            scope=self.YOUTUBE_UPLOAD_SCOPE,
            message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, args)

        return build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()))

    def initialize_upload(self, youtube, options):
        tags = None
        if options.keywords:
            tags = options.keywords.split(",")

        body=dict(
            snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
            ),
            status=dict(
            privacyStatus=options.privacyStatus
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
        )

        self.resumable_upload(insert_request)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.
    def resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                        e.content)
                else:
                    raise "HttpError occured"
            # TODO for some reason this is throwing an error
            except self.RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > self.MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)