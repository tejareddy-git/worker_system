from django.urls import path
from .views import GetRecentItem, GetItemsbyColor, GetBrandCount

urlpatterns = [
    path('recent_items/', GetRecentItem.as_view(), name='RecentItems'),
    path('brand_count/', GetBrandCount.as_view(), name='BrandCount'),
    path('color_items/', GetItemsbyColor.as_view(), name='ColorItems'),
]