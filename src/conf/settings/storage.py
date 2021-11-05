from .common import env

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'static'


# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/_storage/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '_storage'

if env('S3_ACCESS_KEY_ID'):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET')
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_LOCATION = 'static'
    AWS_LOCATION_MEDIA = 'media'
    AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
    AWS_ACCESS_KEY_ID = env('S3_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('S3_SECRET_ACCESS_KEY')

    domain = AWS_STORAGE_BUCKET_NAME + '.storage.yandexcloud.net'
    STATIC_URL = f'https://{domain}/{AWS_LOCATION}/'
    MEDIA_URL = f'https://{domain}/{AWS_LOCATION_MEDIA}/'
