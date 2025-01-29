from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from pos_django_cafe.apps.core.models import OrderStatus, Order


class OrderViewSetTest(TestCase):
    def setUp(self) -> None:
        self.status = OrderStatus.objects.create(name='New')
        self.url = reverse('order-list')

    def test_create_order(self) -> None:
        url = reverse('order-list')
        data = {
            'table_number': 1,
            'items': [
                {'name': 'item1', 'price': 50.00},
                {'name': 'item2', 'price': 50.00}
            ],
            'status': self.status.id
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        assert order is not None
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.total_price, 100.00)
        self.assertEqual(order.status, self.status)

    def test_missing_required_field(self) -> None:
        data = {
            'items': ['item1', 'item2'],
            'total_price': 100.00,
            'status': self.status.id
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('table_number', response.json()['errors'])

    def test_invalid_status(self) -> None:
        data = {
            'table_number': 1,
            'items': ['item1', 'item2'],
            'total_price': 100.00,
            'status': 9999
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('status', response.json()['errors'])

    def test_invalid_data_format(self) -> None:
        data = {
            'table_number': 'not_a_number',
            'items': ['item1', 'item2'],
            'total_price': 100.00,
            'status': self.status.id
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('table_number', response.json()['errors'])

    def test_missing_json_body(self) -> None:
        response = self.client.post(self.url, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())
