from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from dialogflow_lite.dialogflow import Dialogflow
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from string import ascii_letters
from .scraping.lirr_schedule import *
import json


def serviceworker(request, js):
    print("INSIDE")
    template = get_template('serviceworker.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")

def base_layout(request):
    template='app.html'
    return render(request,template)


def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

    return data


@require_http_methods(['GET'])
def index_view(request):
    return render(request, 'app.html')


@csrf_exempt 
@require_http_methods(['POST'])
def chat_view(request):
    dialogflow = Dialogflow(**settings.DIALOGFLOW)
    input_dict = convert(request.body)
    print(request.body)
    input_text = json.loads(input_dict)['text']
    responses = dialogflow.text_request(str(input_text))

    if request.method == "GET":
        # Return a method not allowed response
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }
        return JsonResponse(data, status=405)

    elif request.method == "POST":
        print(responses)
        data = {
            'text': responses[0],
        }
        return JsonResponse(data, status=200)
    
    elif request.method == "PATCH":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    elif request.method == "DELETE":
        data = {
            'detail': 'You should make a POST request to this endpoint.',
            'name': '/chat'
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)


# def getDirection(addr):
#     #gmaps = googlemaps.Client(key='AIzaSyAtGao993KaxBlVtbynXlYWW97arJmxNtg')
#     #geocode_result = gmaps.geocode(addr)
#     #directions_result = gmaps.directions("Sydney Town Hall", "Parramatta, NSW", mode="transit",departure_time=now)
#     api = Geocoding()


@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    # print(req["queryResult"]["parameters"])
    help_message = ""

    if action == "location":
        url = 'https://maps.google.com/maps?q='
        my_loc = req["queryResult"]["parameters"]["given-name"]
        allowed = set(ascii_letters + ' ')
        my_loc = ''.join(l for l in my_loc if l in allowed)
  
        url += my_loc + " Stony Brook University"
        url = url.replace(' ','+')
        help_message = "Maybe this link can help - "
        fulfillmentText = {'fulfillmentText': help_message + url}

    elif action == "lirr_schedule":
        fromStn= req["queryResult"]["parameters"]["from-name"]
        toStn= req["queryResult"]["parameters"]["to-name"]
        message = getTrains(fromStn, toStn, time)
        fulfillmentText = {'fulfillmentText': help_message}
        

    # return a fulfillment message
    return JsonResponse(fulfillmentText, safe=False)