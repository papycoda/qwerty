from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Product, Category
from django.utils.text import slugify
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with 100 products and categories'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create categories
        categories = [
            "Electronics", "Clothing", "Home & Garden", "Sports & Outdoors",
            "Books", "Toys & Games", "Beauty & Personal Care", "Automotive",
            "Health & Wellness", "Food & Grocery"
        ]
        
        with transaction.atomic():
            # Create categories
            for category_name in categories:
                Category.objects.create(
                    name=category_name,
                    description=fake.paragraph()
                )
            
            # Get all category ids
            category_ids = list(Category.objects.values_list('id', flat=True))
            
            # Create 100 products
            for _ in range(100):
                Product.objects.create(
                    name=fake.catch_phrase(),
                    description=fake.paragraph(),
                    price=round(random.uniform(9.99, 999.99), 2),
                    category_id=random.choice(category_ids)
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 100 products and categories'))