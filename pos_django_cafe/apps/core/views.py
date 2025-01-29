from typing import Optional, Any

from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from pos_django_cafe.apps.core.models import Order, OrderStatus
from pos_django_cafe.apps.core.serializers import OrderSerializer, OrderStatusSerializer


def index(request: HttpRequest) -> HttpResponse:
    summ: Optional[float] = Order.objects.filter(status_id=2).aggregate(Sum('total_price'))['total_price__sum']
    return render(request, 'index.html', {'summ': summ})


def orders(request: HttpRequest) -> HttpResponse:
    search_query = request.GET.get('search', '').strip()
    all_orders = Order.objects.all()
    if search_query:
        all_orders = all_orders.filter(
            Q(items__icontains=search_query) |
            Q(total_price__icontains=search_query) |
            Q(status__name__icontains=search_query)
        )

    statuses = OrderStatus.objects.all()

    page = request.GET.get('page', 1)

    orders_per_page = request.GET.get('per_page', 10)

    paginator = Paginator(all_orders, orders_per_page)

    orders_list = paginator.get_page(page)

    context = {
        'orders': orders_list,
        'total_orders': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': orders_list.number,
        'statuses': statuses,
    }

    return render(request, 'orders.html', context)


def create_order(request: HttpRequest) -> HttpResponse:
    return render(request, 'create_order.html')


class OrderViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = OrderSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {
                    "detail": "Ошибка валидации.",
                    "errors": e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Unexpected error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request: Any, pk: Optional[int] = None) -> Response:
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request: Any, pk: Optional[int] = None) -> Response:
        order = get_object_or_404(Order, pk=pk)
        status_id = request.data.get('status')
        try:
            new_status = OrderStatus.objects.get(id=status_id)
        except OrderStatus.DoesNotExist:
            return Response(
                {"error": "Incorrect status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class StatusViewSet(viewsets.ViewSet):
    def list(self, request: Any) -> Response:
        statuses = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(statuses, many=True)
        return Response(serializer.data)
