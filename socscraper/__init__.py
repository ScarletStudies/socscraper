import ujson
import requests
import tempfile


def download_to_file(url):
    r = requests.get(url, stream=True)

    if not r.ok:
        print('Failed to download courses, received status code {}'.format(r.status_code))
        raise RuntimeError('Failed to download courses')

    fp = tempfile.TemporaryFile('wb+')

    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            fp.write(chunk)

    fp.seek(0)

    return fp


def scrape(year,
           term,
           campus,
           output_filename='output.json',
           fieldsMap=None):

    if campus not in ('NK', 'NB', 'CM'):
        raise ValueError('Invalid campus: must be one of NK, NB, or CM')

    if term not in (0, 1, 7, 9):
        raise ValueError('Invalid year: must be one of 0, 1, 7, or 9')

    print('Downloading courses')

    url = 'http://sis.rutgers.edu/soc/api/courses.gzip?year={}&term={}&campus={}'.format(
        year, term, campus)

    fp = download_to_file(url)

    print('Courses downloaded')

    output = []
    courses = ujson.load(fp)

    for course in courses:
        obj = {}

        if fieldsMap is not None:
            for apiKey, outputKey in fieldsMap.items():
                obj[outputKey] = course[apiKey]
        else:
            obj = {**course}

        output.append(obj)

    print('Scraped {} courses'.format(len(output)))

    with open(output_filename, 'w') as fp:
        ujson.dump(output, fp)

    print('Wrote to {}'.format(output_filename))
