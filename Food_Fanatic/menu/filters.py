from django_filters.rest_framework import FilterSet
from .models import FoodItem


class ProductFilter(FilterSet):
    class Meta:
        model = FoodItem
        fields = {
            # 'category_id': ['exact'],
            'price': ['gt', 'lt']
        }