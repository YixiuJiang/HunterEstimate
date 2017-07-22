from django.http import HttpResponse
import requests
import simplejson as json


def index(request):
    totalFee = 0
    result = ''
    dataArray = request.GET.getlist('dataArray')
    suburb = request.GET['suburb']
    postcode = request.GET['postcode']
    state = request.GET['state']
    goods = []
    for data in dataArray:
        postData = data.split(',')
        good = {}
        good['pieces'] = 1
        good['weight'] = postData[0]
        good['width'] = postData[1]
        good['height'] = postData[2]
        good['depth'] = postData[3]
        good['typeCode'] = 'ENV'
        goods.append(good)

    url = "https://api.hunterexpress.com.au/live/rest/hxws/quote/get-quote"
    data = {
        "customerCode": "OLIRF",
        "fromLocation": {
            "suburbName": "MULGRAVE",
            "postCode": "3170",
            "state": "VIC"
        },
        "toLocation": {
            "suburbName": suburb,
            "postCode": postcode,
            "state": state
        },
        "goods": goods
    }
    headers = {'Content-type': 'application/json', 'Authorization': 'Basic T0xJUkY6aHlwaHRyb25pY3M=',
               'Accept': 'application/json'}
    estimates = json.loads(requests.post(url, data=json.dumps(data), headers=headers).text)
    if isinstance(estimates, list):
        for estimate in estimates:
            if estimate.get('serviceCode', 'Error') == 'RF':
                totalFee = estimate['fee'] + totalFee
            if estimate.get('serviceCode', 'Error') == 'Error':
                result = estimate['errorMessage']
    else:
        result = estimates['errorMessage']
    #GST plus another 15%
    if totalFee != 0:
        result = str(round(totalFee * 1.1*1.15, 2))
    return HttpResponse("estimate({'fee':'" + result + "'});")
