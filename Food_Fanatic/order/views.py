from rest_framework.response import Response
from menu.filters import ProductFilter
from .serializers import CartSerializer, ProductSerializer, CategorySerializer, ReviewSerializers, CartItemSerializer, AddCartItemSerializer,OrderSerializer,SpecialOfferSerializer
from menu.models import Cart, Category, FoodItem, Review, Cartitems,SpecialOffer
from order.models import Order,OrderItem
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
import datetime


# Create your views here.
class ProductsViewSet(ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = ProductSerializer
    
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = ProductFilter
    # search_fields = ['name', 'description']
    # ordering_fields = ['old_price']
    pagination_class = PageNumberPagination



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

        
            

class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)
    
class SpecialOfferViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly] 
    queryset = SpecialOffer.objects.filter(active=True, start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today()) 
    serializer_class = SpecialOfferSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Optionally filter or modify queryset based on user permissions
            return queryset
        return queryset