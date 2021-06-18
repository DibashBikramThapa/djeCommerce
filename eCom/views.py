from django.shortcuts import render,get_object_or_404,redirect
from .models import Item, OrderItem, Order, BillingAddress
from django.urls import reverse_lazy
from eCom.forms import CheckoutForm

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model=Item
    paginate_by=4

    template_name='eCom/home-page.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object':order
            }
            return render(self.request,'eCom/order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You dont have active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name='eCom/product-page.html'

class PaymentView(View):
    def get(self, *arags, **kwargs):

        return render(self.request,"eCom/payment.html")


class Checkout(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context={
        'form': form
        }
        return render(self.request,"eCom/checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address=form.cleaned_data.get('street_address')
                appartment_address=form.cleaned_data.get('appartment_address')
                country=form.cleaned_data.get('country')
                zip=form.cleaned_data.get('zip')

                #same_billing_address=form.cleaned_data.get('same_billing_address')
                #save_info= form.cleaned_data.get('save_info')

                payment_option=form.cleaned_data.get('payment_option')
                billing_address=BillingAddress(
                user=self.request.user,
                street_address=street_address,
                country=country,
                zip=zip
                )
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                return redirect('eCom:checkout')
            messages.warning(self.request,"Failed Checkout")
            return redirect('eCom:checkout')
        except ObjectDoesNotExist:
            messsages.error(self.request,"You dont have active order")
            return redirect("eCom:order_summary")


@login_required
def add_to_cart(request,pk):
    item=get_object_or_404(Item,pk=pk)
    orderitem,created=OrderItem.objects.get_or_create(item=item,user=request.user,
        ordered=False)
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]
        if order.items.filter(item__pk=item.pk).exists():
            orderitem.quantity +=1
            orderitem.save()
            messages.info(request,"This item quantity was updated")
            return redirect("eCom:order_summary")
        else:
            messages.info(request,"This item was added")
            order.items.add(orderitem)

            return redirect("eCom:order_summary")
    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(orderitem)
        messages.info(request,"This item was added")
        return redirect("eCom:order_summary")

@login_required
def remove_from_cart(request,pk):
    item=get_object_or_404(Item,pk=pk)
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]

        #if order item is in order
        if order.items.filter(item__pk=item.pk).exists():
            order_item=OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False,
            )[0]
            order.items.remove(order_item)

            messages.info(request,"This item was removed from cart")
            return redirect("eCom:order_summary")
        else:
        #messafe if no order
            messages.info(request,"This item not in cart")
            return redirect("eCom:productpage",pk=pk)
    else:
        #messafe if no order
        messages.info(request,"No active order")
        return redirect("eCom:productpage",pk=pk)

@login_required
def remove_single_item_from_cart(request,pk):
    item=get_object_or_404(Item,pk=pk)
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]
        #if order item is in order
        if order.items.filter(item__pk=item.pk).exists():
            order_item=OrderItem.objects.filter(
            item=item,
            user=request.user,
            ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request,"One quantity removed")
            return redirect("eCom:order_summary")
        else:
        #messafe if no order
            messages.info(request,"This item not in cart")
            return redirect("eCom:productpage",pk=pk)
    else:
        #messafe if no order
        messages.info(request,"No active order")
        return redirect("eCom:productpage",pk=pk)


class OrderItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('eCom:order_summary')
