from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from app.models import Order
import json
import datetime, pytz

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def orders(request, sale_id=None):
