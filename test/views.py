from django.shortcuts import render

import urllib.parse
import requests

api_key = "RGAPI-752ec192-ec55-44a8-a900-0d89cef06352"
gameName = '세웠습니다'
gameName = urllib.parse.quote(gameName)
tagLine = 'KR1'
region = "asia"

api_url = {
    "getPuuid": "/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
}
url = ""

def api_test(request):
    result = {}
    header = {"X-Riot-Token" : api_key}

    request_url = "https://"+region+".api.riotgames.com"+url
    print(request_url)

    response = requests.get(request_url, headers=header, timeout=10)
    print("----------response start-----------")
    print(response)
    print("----------response end-----------")

    result = response.json()

    return render(request, 'test.html')
