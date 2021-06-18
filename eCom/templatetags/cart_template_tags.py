from django import template
from eCom.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        s=Order.objects.filter(user=user,ordered=False)
        if s.exists():
            return s[0].items.count()
        return 0
