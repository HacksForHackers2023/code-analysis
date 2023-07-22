import urllib.error

import radon
from radon import complexity, raw
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from binaryornot.check import is_binary
from collections import deque
import pandas as pd
import json
from util import auth

urlparse("scheme://netloc/path;parameters?query#fragment")
REPOS = 'https://api.github.com/repos'
NO_CHECKS = {'html', 'svg', 'txt', 'md', 'css', 'LICENSE', '.gitignore', 'min.js', 'png', 'jpg', 'ico', 'gif', 'woff'}

r = 'https://github.com/PrideHacks-2023/mapper'


def repo_parser(repo_url, is_update):
    link = repo_url
    if is_update:
        link = REPOS + urlparse(repo_url).path + '/contents/'
    try:
        req = Request(link, headers={'Authorization': f'Bearer {auth.get_token()}'})
        print(req.data)
        file = urlopen(req)
        data = json.load(file)
        return data
    except urllib.error.HTTPError as e:
        print(f'Unable to proceed: {e}')
        pass


def file_name(url):
    arr = url.split('/')[5:]
    return '/'.join(arr)


def code_complexity(url, repo_url):
    name = file_name(url)
    dir = '/'.join(name.split('/')[:-1])
    output_func = []
    a = repo_url + '/blob/' + name
    req = Request(url, headers={'Authorization': f'{auth.get_token()}'})
    with urlopen(req) as file:
        try:
            data = file.read().decode('utf-8')
            cc = radon.complexity.cc_visit(data)
            soc = radon.raw.analyze(data)
            output_overall = {
                "directory": dir,
                "filename": name,
                "loc": soc.loc,
                "lloc": soc.lloc,
                "sloc": soc.sloc,
                "link": a
            }

            for entry in cc:
                result = {
                    "directory": dir,
                    "filename": name,
                    "function_name": entry.name,
                    "line number": entry.lineno,
                    "complexity": entry.complexity,
                    "link": a
                }
                output_func.append(result)
        except SyntaxError as e:
            print(f'File skipped, {e} \n {name}')
            return None
        except UnicodeDecodeError as e:
            print(f'File skipped, {e} \n {name}')
            return None

    return output_overall, output_func


def file_include(url):
    for extension in NO_CHECKS:
        if extension in url:
            return False
    return True


def walker(data, repo_url):
    output_overall = []
    output_func = []
    q = deque(data)
    while q:
        d = q.pop()
        link = d['download_url']
        if d['type'] == 'file' and not is_binary(link) and file_include(link):
            result = code_complexity(link, repo_url)
            if not result:
                continue
            output_overall.append(result[0])
            output_func.extend(result[1])
        if d['type'] == 'dir':
            arr = repo_parser(d['url'], False)
            q.extend(arr)

    return output_overall, output_func


def stats(repo_url):
    data = repo_parser(repo_url, True)
    output_data = walker(data, repo_url)
    df_overall = pd.DataFrame(output_data[0])
    df_func = pd.DataFrame(output_data[1])
    print(df_overall)
    return df_overall, df_func
