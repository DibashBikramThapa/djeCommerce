from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField


# Create your models here.
CATEGORY_CHOICES=(
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Outwear'),
)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    shirt_pic=models.ImageField(upload_to='shirt_pic',blank=True)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label=models.CharField(choices=LABEL_CHOICES,max_length=1)
    description=models.TextField()

    def get_absolute_url(self):
        return reverse("eCom:productpage",
                kwargs={"pk":self.pk})

    def get_add_to_cart_url(self):
        return reverse("eCom:add_to_cart",
                kwargs={"pk":self.pk})

    def get_remove_from_cart_url(self):
        return reverse("eCom:remove_from_cart",
                kwargs={"pk":self.pk})

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey('auth.User',
                on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,
                on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def saved_amount(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey('auth.User',
                on_delete=models.CASCADE)
    items= models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date=models.DateField()
    ordered = models.BooleanField(default=False)
    billing_address=models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    appartment_address=models.CharField(max_length=100)
    country=CountryField(multiple=False)
    zip=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
