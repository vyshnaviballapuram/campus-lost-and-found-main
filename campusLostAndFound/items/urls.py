"""
URL configuration for Items app.
Yeh file items app ke sab URLs define karti hai.
"""

from django.urls import path
from . import views

# URL patterns - sab URLs yahan define hain
urlpatterns = [
    # Home/Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Item listing views
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/lost/', views.LostItemListView.as_view(), name='lost_items'),
    path('items/found/', views.FoundItemListView.as_view(), name='found_items'),
    
    # Item detail view
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    
    # Item CRUD operations
    path('items/new/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # User specific views
    path('my-items/', views.my_items_view, name='my_items'),
    path('items/<int:pk>/resolve/', views.mark_resolved_view, name='mark_resolved'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
]
