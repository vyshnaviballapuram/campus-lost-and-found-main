"""
Database models for the Items app.
Yeh file database tables ke models define karti hai.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Item(models.Model):
    """
    Item model - Lost aur Found items ke liye main model.
    Yeh model ek item ki sari details store karta hai.
    """
    
    # Item status choices - Lost ya Found
    STATUS_CHOICES = [
        ('lost', 'Lost'),      # Gum ho gaya
        ('found', 'Found'),    # Mil gaya
    ]
    
    # Category choices - Item ki category
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),           # Mobile, laptop, etc.
        ('documents', 'Documents & ID Cards'),    # CNIC, license, etc.
        ('accessories', 'Accessories'),           # Watch, jewelry, etc.
        ('clothing', 'Clothing'),                 # Kapray
        ('books', 'Books & Stationery'),          # Kitaabein
        ('keys', 'Keys'),                         # Chabiyan
        ('wallet', 'Wallet & Money'),             # Batua
        ('bags', 'Bags & Luggage'),               # Bags
        ('other', 'Other'),                       # Aur kuch bhi
    ]
    
    # Basic item information fields
    title = models.CharField(
        max_length=200,
        help_text="Item ka title dein"
    )
    
    description = models.TextField(
        help_text="Item ki mukammal description likhein"
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Item ki category select karein"
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='lost',
        help_text="Item lost hai ya found"
    )
    
    # Image field - item ki tasveer ke liye
    image = models.ImageField(
        upload_to='item_images/',
        blank=True,
        null=True,
        help_text="Item ki tasveer upload karein (optional)"
    )
    
    # Location aur date information
    location = models.CharField(
        max_length=255,
        help_text="Jahan item mili ya gumi - wo jagah likhein"
    )
    
    date_lost_found = models.DateField(
        help_text="Jis din item gumi ya mili"
    )
    
    # Contact information
    contact_email = models.EmailField(
        help_text="Contact email address"
    )
    
    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number (optional)"
    )
    
    # Relationship with User model - item kis user ne post ki
    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # User delete ho to items bhi delete
        related_name='items',       # user.items se access kar sakte hain
        help_text="Jis user ne item post ki"
    )
    
    # Timestamps - kab create aur update hui
    created_at = models.DateTimeField(auto_now_add=True)  # Sirf create par
    updated_at = models.DateTimeField(auto_now=True)      # Har update par
    
    # Admin verification status
    is_verified = models.BooleanField(
        default=False,
        help_text="Admin ne verify kiya hai ya nahi"
    )
    
    # Item resolved status - claim ho gayi ya nahi
    is_resolved = models.BooleanField(
        default=False,
        help_text="Item claim ho gayi ya nahi"
    )
    
    class Meta:
        """
        Model ki meta information.
        Ordering aur display name set karte hain.
        """
        ordering = ['-created_at']  # Newest first
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
    
    def __str__(self):
        """
        Item ka string representation.
        Admin panel aur debugging mein kaam aata hai.
        """
        return f"{self.get_status_display()}: {self.title}"
    
    def get_absolute_url(self):
        """
        Item detail page ka URL return karta hai.
        CreateView aur UpdateView mein use hota hai.
        """
        return reverse('item_detail', kwargs={'pk': self.pk})
    
    @property
    def status_badge_class(self):
        """
        Bootstrap badge class return karta hai status ke hisaab se.
        Templates mein color coding ke liye use hota hai.
        """
        if self.status == 'lost':
            return 'bg-danger'    # Red color for lost
        return 'bg-success'       # Green color for found
