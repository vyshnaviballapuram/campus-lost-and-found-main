"""
Views for the Items app.
Yeh file sab views define karti hai jo HTTP requests handle karti hain.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Item
from .forms import ItemForm, UserRegisterForm, ItemSearchForm
from .ai_matching import find_matches_for_lost_item, find_matches_for_found_item


# ==================== Authentication Views ====================

def register_view(request):
    """
    User registration view.
    Naya user account create karne ke liye hai.
    POST request par form validate kar ke user create karta hai.
    """
    if request.user.is_authenticated:
        # Agar user already logged in hai to redirect kar do
        return redirect('item_list')
    
    if request.method == 'POST':
        # Form data se UserRegisterForm create karna
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            # User save karna
            user = form.save()
            
            # User ko automatically login kar dena
            login(request, user)
            
            # Success message show karna
            messages.success(
                request, 
                f'Welcome {user.first_name}! Your account has been created successfully.'
            )
            
            return redirect('item_list')
    else:
        # GET request par empty form dikhana
        form = UserRegisterForm()
    
    context = {
        'form': form,
        'title': 'Sign Up'
    }
    
    return render(request, 'registration/register.html', context)


# ==================== Item List & Search Views ====================

class ItemListView(ListView):
    """
    Items ki list dikhane ka view.
    Home page par sab items cards mein dikhata hai.
    Search aur filter functionality bhi hai.
    """
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 12  # Har page par 12 items
    
    def get_queryset(self):
        """
        Items ka filtered queryset return karta hai.
        Search query aur filters apply karta hai.
        """
        # Base queryset - sirf verified aur unresolved items
        queryset = Item.objects.filter(is_resolved=False)
        
        # Search query apply karna
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        
        # Category filter apply karna
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)
        
        # Status filter apply karna
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Template context mein extra data add karna.
        Search form aur current filters pass karta hai.
        """
        context = super().get_context_data(**kwargs)
        
        # Search form add karna with current values
        context['search_form'] = ItemSearchForm(self.request.GET)
        
        # Statistics add karna
        context['total_lost'] = Item.objects.filter(
            status='lost', 
            is_resolved=False
        ).count()
        context['total_found'] = Item.objects.filter(
            status='found', 
            is_resolved=False
        ).count()
        
        return context


class LostItemListView(ItemListView):
    """
    Sirf Lost items dikhane ka view.
    ItemListView ko extend karta hai.
    """
    
    def get_queryset(self):
        """
        Sirf lost items return karta hai.
        """
        return super().get_queryset().filter(status='lost')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Lost Items'
        context['status_filter'] = 'lost'
        return context


class FoundItemListView(ItemListView):
    """
    Sirf Found items dikhane ka view.
    ItemListView ko extend karta hai.
    """
    
    def get_queryset(self):
        """
        Sirf found items return karta hai.
        """
        return super().get_queryset().filter(status='found')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Found Items'
        context['status_filter'] = 'found'
        return context


# ==================== Item Detail View ====================

class ItemDetailView(DetailView):
    """
    Single item ki detail dikhane ka view.
    AI-based similar items bhi dikhata hai.
    """
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    
    def get_context_data(self, **kwargs):
        """
        Template context mein AI matches add karna.
        Lost item ke liye found matches aur vice versa.
        """
        context = super().get_context_data(**kwargs)
        item = self.object
        
        # AI matching based on item status
        if item.status == 'lost':
            # Lost item ke liye found items mein matches dhundna
            found_items = Item.objects.filter(
                status='found',
                is_resolved=False,
                category=item.category  # Same category mein dhundna
            ).exclude(pk=item.pk)
            
            context['matches'] = find_matches_for_lost_item(
                item, 
                found_items,
                threshold=5,  # 5% se zyada similarity wale
                top_n=5
            )
            context['match_type'] = 'found'
            
        else:
            # Found item ke liye lost items mein matches dhundna
            lost_items = Item.objects.filter(
                status='lost',
                is_resolved=False,
                category=item.category  # Same category mein dhundna
            ).exclude(pk=item.pk)
            
            context['matches'] = find_matches_for_found_item(
                item, 
                lost_items,
                threshold=5,  # 5% se zyada similarity wale
                top_n=5
            )
            context['match_type'] = 'lost'
        
        # Check karna ki current user owner hai ya nahi
        context['is_owner'] = (
            self.request.user.is_authenticated and 
            self.request.user == item.posted_by
        )
        
        return context


# ==================== Item CRUD Views ====================

class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    Naya item create karne ka view.
    Sirf logged in users ke liye accessible hai.
    """
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    
    def form_valid(self, form):
        """
        Form valid hone par item save karna.
        Current user ko posted_by set karta hai.
        """
        # Current user set karna
        form.instance.posted_by = self.request.user
        
        # Default contact email set karna agar empty ho
        if not form.instance.contact_email:
            form.instance.contact_email = self.request.user.email
        
        # Success message
        messages.success(
            self.request, 
            'Your item has been posted successfully!'
        )
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post New Item'
        context['button_text'] = 'Post Item'
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Item update karne ka view.
    Sirf item owner hi update kar sakta hai.
    """
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    
    def test_func(self):
        """
        Check karna ki current user item ka owner hai.
        UserPassesTestMixin ke liye required hai.
        """
        item = self.get_object()
        return self.request.user == item.posted_by
    
    def form_valid(self, form):
        """
        Form valid hone par success message dikhana.
        """
        messages.success(self.request, 'Item updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Item'
        context['button_text'] = 'Update Item'
        return context


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Item delete karne ka view.
    Sirf item owner hi delete kar sakta hai.
    """
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    
    def test_func(self):
        """
        Check karna ki current user item ka owner hai.
        """
        item = self.get_object()
        return self.request.user == item.posted_by
    
    def delete(self, request, *args, **kwargs):
        """
        Delete hone par success message dikhana.
        """
        messages.success(request, 'Item deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== User Profile & My Items ====================

@login_required
def my_items_view(request):
    """
    User ke apne items dikhane ka view.
    Sirf logged in user ke items dikhata hai.
    """
    # Current user ke items
    items = Item.objects.filter(posted_by=request.user)
    
    # Status filter
    status = request.GET.get('status', '')
    if status:
        items = items.filter(status=status)
    
    context = {
        'items': items,
        'title': 'My Items',
        'total_items': items.count(),
        'lost_count': items.filter(status='lost').count(),
        'found_count': items.filter(status='found').count(),
    }
    
    return render(request, 'items/my_items.html', context)


@login_required
def mark_resolved_view(request, pk):
    """
    Item ko resolved mark karne ka view.
    Jab item mil jaye to user isko mark kar sakta hai.
    """
    item = get_object_or_404(Item, pk=pk)
    
    # Check karna ki user owner hai
    if request.user != item.posted_by:
        messages.error(request, 'You can only mark your own items as resolved.')
        return redirect('item_detail', pk=pk)
    
    # Item ko resolved mark karna
    item.is_resolved = True
    item.save()
    
    messages.success(
        request, 
        'Item marked as resolved! Thank you for using Campus Lost & Found.'
    )
    
    return redirect('my_items')


# ==================== Dashboard View ====================

def dashboard_view(request):
    """
    Dashboard/Home page view.
    Statistics aur recent items dikhata hai.
    """
    # Recent items
    recent_lost = Item.objects.filter(
        status='lost', 
        is_resolved=False
    )[:6]
    
    recent_found = Item.objects.filter(
        status='found', 
        is_resolved=False
    )[:6]
    
    # Statistics
    context = {
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'total_lost': Item.objects.filter(status='lost', is_resolved=False).count(),
        'total_found': Item.objects.filter(status='found', is_resolved=False).count(),
        'total_resolved': Item.objects.filter(is_resolved=True).count(),
    }
    
    return render(request, 'items/dashboard.html', context)
