from unicodedata import category
from django.shortcuts import render, redirect
from admin_app.models import Product
from user_app.models import *
from django.db.models import Sum
import string
import random
import json
import datetime
from django.core.paginator import Paginator, EmptyPage

# Create your views here.


def product(request):
    category = Category.objects.all()
    
    prod = Product.objects.all()
    for i in prod:
        i.price=i.price_actual
        i.save()
    now=datetime.date.today()
    cate_off = CategoryOffer.objects.all()
    if cate_off:
        for j in cate_off:
            if j.valid_till < now:
                print('2666')
                j.status = False
                j.save()
    else:
        pass
    print(now)
    actual_price=0
    
    cate = CategoryOffer.objects.all()
    for i in prod:
        cate_off = CategoryOffer.objects.filter(cid=i.cid)
        
        
        if cate_off:
            for j in cate_off:
                if j.status == True:
                    # sale=j.percentage
                    actual_price=i.price_actual
                    amount = (j.percentage*i.price)/100
                    i.price = i.price-amount
                    print(j.percentage)
                if j.valid_till < now:
                    print('2666')
                    j.status = False
                    j.save()
                
                # if j.status == False:
                #     amount = (j.percentage*i.price_actual)/100
                #     i.price += amount
                #     print('old price')
                

                    
        if ProductOffer.objects.filter(pid=i.id):
            prod_off = ProductOffer.objects.filter(pid=i.id)
            for poff in prod_off:
                if poff.status == True:
                    cate_off = CategoryOffer.objects.filter(cid=i.cid)
                    for coff in cate_off:
                        if coff.cid == poff.pid.cid:
                            if coff.percentage < poff.percentage:
                                print("productname",poff.pid.series)
                                print("success yadhu")
                                amt = (poff.percentage*i.price_actual)/100
                                i.price = i.price_actual-amt
                
        # prod_off = ProductOffer.objects.filter(pid=i.id)
        # for poff in prod_off:
        #     if poff.status == True:
        #         if i.is_offer_apply == True:
        #             cate_off_check = CategoryOffer.objects.filter(cid=i.cid)
        #             for coff in cate_off_check:
        #                 if poff.percentage > coff.percentage:
        #                     i.price 
                
                
    
        
        i.save()
        
    p = Paginator(prod, 6)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {
            'items': page,
            #'user': user,
            'category': category,
            #'brand': brand,
            #'cart':cart,
            'actual_price':actual_price,
            'cate':cate,
        }
    if request.method == "POST":
        search = request.POST['search']
        if len(search) > 0:
            
            
            if Product.objects.filter(series__icontains=search):
                prod = Product.objects.filter(series__icontains=search)
                cate = CategoryOffer.objects.all()
                for i in prod:
                    cate_off = CategoryOffer.objects.filter(cid=i.cid)
                    if cate_off:
                        for j in cate_off:
                            if j.status == True:
                                i.price = i.price-j.percentage
                                i.is_offer_apply = True
                            if j.valid_till < now:
                                print('2666')
                                
                                j.status = False
                                j.save()
                            
                            if j.status == False:
                                i.price += j.percentage
                                print('old price')
                                    
                    else:
                        pass    
                    i.save()
                p = Paginator(prod, 6)
                page_num = request.GET.get('page', 1)
                try:
                    page = p.page(page_num)
                except EmptyPage:
                    page = p.page(1)
                context = {
                    'items': page,
                    #'user': user,
                    'category': category,
                    'prod':prod,
                    #'brand': brand,
                    #'cart':cart,
                    'actual_price':actual_price,
                    'cate':cate,
                    }
                
                return render(request, 'store_temp/prod_view_all.html', context)

            if Category.objects.filter(cate_name__icontains=search):
                    cate_obj = Category.objects.get(cate_name=search)
                    prod = Product.objects.filter(cid=cate_obj)
                    cate = CategoryOffer.objects.all()
                    for i in prod:
                        cate_off = CategoryOffer.objects.filter(cid=i.cid)
                        if cate_off:
                            for j in cate_off:
                                if j.status == True:
                                    i.price = i.price-j.percentage
                                    i.is_offer_apply = True
                                if j.valid_till < now:
                                    print('2666')
                                    
                                    j.status = False
                                    j.save()
                                
                                if j.status == False:
                                    i.price += j.percentage
                                    print('old price')
                                        
                        else:
                            pass    
                        i.save()
                    p = Paginator(prod, 2)
                    page_num = request.GET.get('page', 1)
                    try:
                        page = p.page(page_num)
                    except EmptyPage:
                        page = p.page(1)
                    context = {
                        'items': page,
                        #'user': user,
                        'category': category,
                        'prod':prod,
                        #'brand': brand,
                        #'cart':cart,
                        'actual_price':actual_price,
                        'cate':cate,
                        }
                    
                    return render(request, 'store_temp/prod_view_all.html', context)

    # if 'uname' in request.session:
    #     uname = request.session.get('uname')
    #     user_info = UserSignUp.objects.get(name=uname)
    #     return render(request, 'store_temp/prod_view_all.html', {'items': page, 'user_info':user_info})
    # else:
    return render(request, 'store_temp/prod_view_all.html',context)


def filter_prod(request, id,name):

        
    category = Category.objects.all()

    prod = Product.objects.all()
    if request.method == "POST":
        search = request.POST['search']
        if len(search) > 0:
            
            if Product.objects.filter(product_name__icontains=search):
                prod = Product.objects.filter(product_name__icontains=search)
                p = Paginator(prod, 6)
                page_num = request.GET.get('page', 1)
                try:
                    page = p.page(page_num)
                except EmptyPage:
                    page = p.page(1)
                context = {
                    'items': page,
                    #'user': user,
                    'category': category,
                    'prod':prod,
                    }
                return render(request, 'store_temp/filter_prod_view.html', context)
            elif Product.objects.filter(series__icontains=search):
                prod = Product.objects.filter(series__icontains=search)
                p = Paginator(prod, 6)
                page_num = request.GET.get('page', 1)
                try:
                    page = p.page(page_num)
                except EmptyPage:
                    page = p.page(1)
                context = {
                    'items': page,
                    #'user': user,
                    'category': category,
                    'prod':prod,

                    }
                
                return render(request, 'store_temp/filter_prod_view.html', context)
    
    if Product.objects.filter(cid_id=id):
        print("hello",id)
    
        prod = Product.objects.filter(cid_id=id)
        
        p = Paginator(prod, 6)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {
            'items': page,
            #'user': user,
            'category': category,
            
        }
    elif Product.objects.filter(product_name=name):
        prod = prod.filter(product_name=name)
        p = Paginator(prod, 6)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {
            'items': page,
            #'user': user,
            'category': category,
        }
    else:
            context = {
            'error':'Notihg found!!',
            #'user': user,
            'category': category,
        }
    
        
    return render(request, 'store_temp/filter_prod_view.html', context)


def detail_view(request, id):
    prod = Product.objects.get(id=id)
    return render(request, 'store_temp/detail.html', {'prod': prod})


def home_page(request):
    
    return render(request, 'store_temp/home_page.html')

def add_cart_guest(request,pid):
    if 'guest' in request.session:
        prod = Product.objects.get(id=pid)
        gcart = CartGuestUser()
        gcart.user_session = request.session['guest']
        gcart.pid = prod
        gcart.qty = 1
        gcart.price = float(prod.price*gcart.qty)
        gcart.total_price = float(prod.price*gcart.qty)
        gcart.save()

        print("no use")
    else:
        prod = Product.objects.get(id=pid)
        S=10
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        guser_session = str(ran)
        request.session['guest'] = guser_session
        
        gcart = CartGuestUser()
        gcart.user_session = guser_session
        gcart.pid = prod
        gcart.qty = 1
        gcart.price = float(prod.price*gcart.qty)
        gcart.total_price = float(prod.price*gcart.qty)
        gcart.save()
    return redirect(gcart_view)

def gcart_view(request):
    if 'guest' in request.session:
        guser = request.session['guest']
        
        cart = CartGuestUser.objects.filter(user_session=guser)
        car = CartGuestUser.objects.filter(user_session=guser).aggregate(Sum('total_price'))
        context = {
            'cart':cart,
            'car':car['total_price__sum']
        }
        return render(request, 'user_temp/cart_page.html',context)
    else:
         return render(request, 'user_temp/cart_page.html')
def gcart_update(request):
   body = json.loads(request.body)
   cart = CartGuestUser.objects.get(id=body['cart_id'])
   cart.qty = body['product_qty']
   cart.total_price = body['total']
   cart.save()
   print("cart_test",body)
   print("update cart")
   return redirect(gcart_view)
def gcart_remove(request,id):
    gcart = CartGuestUser.objects.get(id=id)
    gcart.delete()
    return redirect(gcart_view)
