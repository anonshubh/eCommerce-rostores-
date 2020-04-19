from django.test import TestCase,Client
from .models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(title='testing',description='hello world',price=100)
        Product.objects.create(title='testing1',description='this is testing',price=500)
        self.client = Client()
    
    def test_product_creation(self):
        c = Product.objects.all().count()
        self.assertEqual(c,2)
    
    def test_invalid_product_page(self):
        response = self.client.get('product/')
        self.assertEqual(response.status_code,404)
    


