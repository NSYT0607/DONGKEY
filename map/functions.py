from django.http import JsonResponse
from django.template.loader import render_to_string
import urllib.request
import json
import re


# data에서 HTML 태그 없애주는 함수
def remove_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)
    return cleantext


# 네이버 지역검색 API로 장소 검색 결과 받아온 후 넘겨주는 함수
def place_search(txt):
    client_id = "HgDOpjOFssES9HHhpUyD"
    client_secret = "F2thiEuvQu"
    encText = urllib.parse.quote(txt)
    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        data = json.loads(response_body.decode('utf-8'))
        print(response_body.decode('utf-8'))
        for datum in data['items']:
            datum['title'] = remove_tag(datum['title'])
        ctx = {
            'data': data['items']
        }
        html = render_to_string('map/search_result.html', ctx)
        return JsonResponse({'success': True, 'html': html, 'First': data['items'][0]})
    else:
        print("Error Code:" + rescode)