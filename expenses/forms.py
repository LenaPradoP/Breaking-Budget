from django import forms

class ExpensesFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', 'Filter by Category'), 
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
        ('train', 'Train'),
        ('car', 'Car'),
        ('transportation', 'Transportation'),
        ('food', 'Food'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('', 'Filter by Status'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    ORDER_CHOICES = [
        ('', 'Order by'), 
        ('status', 'Approved first'), 
        ('-status', 'Rejected first'), 
        ('amount', 'Less expensive first'),
        ('-amount', 'More expensive first'),
        ('date', 'Older first'),  
        ('-date', 'Newer first'),
    ]
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False, 
        widget=forms.Select(attrs={
            'id': 'category-filter',
        })
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False, 
        widget=forms.Select(attrs={
            'id': 'status-filter',
        })
    )
    
    order_by = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False, 
        widget=forms.Select(attrs={
            'id': 'order-filter',
        })
    )