from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework import status
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from app.models import Order
import json
import datetime, pytz


def serialize_order(order):
    serialized = model_to_dict(order)
    serialized["amount_plus_one"] = order.amount + 1
    return serialized


@api_view(['GET', 'POST'])
def orders(request):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        errors = []
        item = request.data.get("item","")
        if item == "":
            errors.append({"item": "This field is required"})

        try:
            price = request.data.get("price","")
            if price == "":
                errors.append({"price": "This field is required"})
            else:
                price = int(price)
                if price < 0:
                    errors.append({"price": "Price cannot be negative"})
        except ValueError:
            errors.append({"price": "Could not parse field"})

        try:
            quantity = request.data.get("quantity","")
            if quantity == "":
                errors.append({"quantity": "This field is required"})
            else:
                quantity = int(quantity)
                if quantity < 0:
                    errors.append({"quantity": "Quantity cannot be negative"})
        except ValueError:
            errors.append({"quantity": "Could not parse field"})

        date = request.data.get("date","")
        if date == "":
            date = datetime.datetime.now()

        if len(errors) > 0:
            return HttpResponse(json.dumps(
                {
                    "errors": errors
                }), status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order()
            order.date = date
            order.item = item
            order.price = price
            order.quantity = quantity
            order.amount = price * quantity
            order.save()
        except Exception as e:
            return HttpResponse(json.dumps(
                {
                    "errors": {"Order": str(e)}
                }), status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(json.dumps({"data": serialize_order(order)}), status=status.HTTP_201_CREATED)


    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'PUT', 'DELETE'])
def order(request, order_id):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)
