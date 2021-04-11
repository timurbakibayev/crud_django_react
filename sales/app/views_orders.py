from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework import status
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from app.models import Order
import json
import datetime


def serialize_order(order):
    serialized = model_to_dict(order)
    serialized["date"] = str(order.date)
    serialized["amount"] = float(order.amount)
    serialized["price"] = float(order.price)
    serialized["quantity"] = float(order.quantity)
    return serialized


def save_order(request, order, success_status):
    errors = []
    item = request.data.get("item", "")
    if item == "":
        errors.append({"item": "This field is required"})

    try:
        price = request.data.get("price", "")
        if price == "":
            errors.append({"price": "This field is required"})
        else:
            price = int(price)
            if price < 0:
                errors.append({"price": "Price cannot be negative"})
    except ValueError:
        errors.append({"price": "Could not parse field"})

    try:
        quantity = request.data.get("quantity", "")
        if quantity == "":
            errors.append({"quantity": "This field is required"})
        else:
            quantity = int(quantity)
            if quantity < 0:
                errors.append({"quantity": "Quantity cannot be negative"})
    except ValueError:
        errors.append({"quantity": "Could not parse field"})

    date = request.data.get("date", "")
    if date == "":
        date = datetime.datetime.now()

    if len(errors) > 0:
        return HttpResponse(json.dumps(
            {
                "errors": errors
            }), status=status.HTTP_400_BAD_REQUEST)

    try:
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

    return HttpResponse(json.dumps({"data": serialize_order(order)}), status=success_status)


@api_view(['GET', 'POST'])
def orders(request):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        orders_data = Order.objects.all()

        orders_count = orders_data.count()

        page_size = int(request.GET.get("page_size", "10"))
        page_no = int(request.GET.get("page_no", "0"))
        orders_data = list(orders_data[page_no * page_size:page_no * page_size + page_size])

        orders_data = [serialize_order(order) for order in orders_data]
        return HttpResponse(json.dumps({"count": orders_count, "data": orders_data}), status=status.HTTP_200_OK)

    if request.method == "POST":
        order = Order()
        return save_order(request, order, status.HTTP_201_CREATED)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET', 'PUT', 'DELETE'])
def order(request, order_id):
    if request.user.is_anonymous:
        return HttpResponse(json.dumps({"detail": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

    try:
        order = Order.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"detail": "Not found"}), status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return HttpResponse(json.dumps({"data": serialize_order(order)}), status=status.HTTP_200_OK)

    if request.method == "PUT":
        return save_order(request, order, status.HTTP_200_OK)

    if request.method == "DELETE":
        order.delete()
        return HttpResponse(json.dumps({"detail": "deleted"}), status=status.HTTP_410_GONE)

    return HttpResponse(json.dumps({"detail": "Wrong method"}), status=status.HTTP_501_NOT_IMPLEMENTED)
