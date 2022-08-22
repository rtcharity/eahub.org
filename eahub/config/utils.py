import yurl

from six.moves.urllib import parse


def parse_storage_url(url):
  config = {}
  url = parse.urlparse(url)

  scheme = url.scheme.split('+', 1)
  schemes = {
    's3': 'aldryn_django.storage.S3MediaStorage',
    'djfs': 'fs.django_storage.DjeeseFSStorage',
  }

  config['DEFAULT_FILE_STORAGE'] = schemes[scheme[0]]

  if scheme[0] == 's3':
    query = parse.parse_qs(url.query)
    media_domain = query.get('domain', [None])[0]
    signature_ver = query.get('auth', ['s3v4'])[0]
    endpoint = url.hostname.rsplit('.', 3)
    bucket_name = endpoint[0]
    storage_host = '.'.join(endpoint[1:])

    if signature_ver == 's3v4':
      os.environ['S3_USE_SIGV4'] = 'True'
    elif signature_ver == 's3':
      os.environ['S3_USE_SIGV4'] = ''
    else:
      raise Exception('Unknown signature version: {}'
                      .format(signature_ver))

    config.update({
      'AWS_MEDIA_ACCESS_KEY_ID': parse.unquote(url.username or ''),
      'AWS_MEDIA_SECRET_ACCESS_KEY': parse.unquote(url.password or ''),
      'AWS_MEDIA_STORAGE_BUCKET_NAME': bucket_name,
      'AWS_MEDIA_STORAGE_HOST': storage_host,
      'AWS_MEDIA_BUCKET_PREFIX': url.path.lstrip('/'),
      'AWS_MEDIA_DOMAIN': media_domain,
    })

    media_url = yurl.URL(
      scheme='https',
      host=media_domain,
      path=config['AWS_MEDIA_BUCKET_PREFIX'],
    )
    config['MEDIA_URL'] = media_url.as_string()

  if config['MEDIA_URL'] and not config['MEDIA_URL'].endswith('/'):
    # Django (or something else?) silently sets MEDIA_URL to an empty
    # string if it does not end with a '/'
    config['MEDIA_URL'] = '{}/'.format(config['MEDIA_URL'])
  return config