
import datetime

import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from admin_app.models import *
from cart.models import *
from django.views.decorators.cache import never_cache
import random
from twilio.rest import Client
from django.core.paginator import Paginator, EmptyPage
import vonage
from django.db.models import Sum
from django.template.loader import render_to_string
import sweetify
import razorpay


# Create your views here.


def user_sign(request):
    if request.method == 'POST':
        name = request.POST['uname']
        mobile = request.POST['mobile']
        email = request.POST['email']
        psw = request.POST['psw']
        re_psw = request.POST['re_psw']
        usign = UserSignUp.objects.create(name=name, number=mobile, email=email, psw=psw, psw1=re_psw, status=True, logstatus=False)
        usign.save()
        refer_code = request.POST.get('refer_code')
        ref=ReferralCode.objects.filter(refer_code=refer_code)
        if ref:
            ref_check = ReferralCode.objects.get(refer_code=refer_code)
            wallet = Wallet()
            wallet.user = usign
            wallet.money = 20
            wallet.save()
            if Wallet.objects.filter(user_id=ref_check.user):
                wal = Wallet.objects.get(user_id=ref_check.user)
                wal.money = wal.money+100
                wal.save()
            
            else:
                wallet = Wallet()
                wallet.user = ref_check.user
                wallet.money += 100
                wallet.save()
        else:
            print('please enter a valid refer_code')

    return render(request, 'user_temp/user_signup.html')




def otp_verify(re):
    if re.method == 'POST':
        d=re.POST.get('otp')
        t=re.session.get('se')
        client = vonage.Client(key="569ec10a", secret="cepd98rNNZFd4lOn")
        verify = vonage.Verify(client)
        response = verify.check(t, code=d)

        if response["status"] == "0":

            print("Verification successful, event_id is %s" % (response["event_id"]))
            return redirect(product)

        else:
            print("Error: %s" % response["error_text"])
            return redirect(otp_verify)


    return render(re,"user_temp/otp_page_verify.html")

@never_cache
def user_login(request):
    if 'uname' in request.session:
        return redirect(user_home)
    if request.method == 'POST':
        uname = request.POST['uname']
        psw = request.POST['psw']
        
        user_log = UserSignUp.objects.filter(email=uname, psw=psw)
        if user_log:
            user = UserSignUp.objects.get(email=uname)
            if Wallet.objects.filter(user_id=user):
                pass
            else:
                wallet = Wallet()
                wallet.user = user
                wallet.money = 0
                wallet.save()
            if user_log:
                block_user_data = UserSignUp.objects.get(email=uname)

                if block_user_data.status is True:
                    if user_log:
                        request.session['uname'] = uname

                        return redirect(user_home)
                else:
                    messages.info(request,'error')
            print(request.session['guest'])
        else:
            messages.warning(request,'Invalid Email or Password')    
    return render(request, 'user_temp/user_login.html')


def otp_log(r):
    if r.method == 'POST':
        client = vonage.Client(key="569ec10a", secret="cepd98rNNZFd4lOn")
        verify = vonage.Verify(client)
        response = verify.start_verification(number="916282787327", brand="AcmeInc")
        r.session['se'] = response['request_id']

        if response["status"] == "0":
            print("Started verification request_id is %s" % (response["request_id"]))
            return redirect('otp_log_verify')

        else:
            print("Error: %s" % response["error_text"])
            return redirect(otp_log)


    return render(r,"user_temp/otp_page.html")
from django.utils import timezone


@never_cache
def user_home(request):
    if 'uname' in request.session:
        data = request.session['uname']
        user = UserSignUp.objects.get(email=data)
        
        
        
        if 'guest' in request.session:
            guest = request.session['guest']
            print(guest)
            print('quest')
            
            gcart = CartGuestUser.objects.filter(user_session=guest)
            for i in gcart:
                cart = Cart_view()
                cart.qty = i.qty
                cart.pid = i.pid
                cart.uid = user
                cart.total_price = i.total_price
                cart.tot_amt = i.price
                cart.save()
            del request.session['guest']
            gcart.delete()
        
        block_user_data = UserSignUp.objects.get(email=data)
        
        category = Category.objects.all()
        cart = Cart_view.objects.filter(uid_id=user.id).count()
        
        print("cart",cart)
        brand = Brand.objects.all()
        if block_user_data.status is False:
            del request.session['uname']
            return redirect('user_login')
        user.logstatus = True
        user.save()
        print(user.logstatus)
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
            'user': user,
            'category': category,
            'brand': brand,
            'cart':cart,
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
                    p = Paginator(prod, 2)
                    page_num = request.GET.get('page', 1)
                    try:
                        page = p.page(page_num)
                    except EmptyPage:
                        page = p.page(1)
                    context = {
                        'items': page,
                        'user': user,
                        'category': category,
                        'prod':prod,
                        'brand': brand,
                        'cart':cart,
                        'actual_price':actual_price,
                        'cate':cate,
                        }
                    
                    return render(request, 'store_temp/prod_view_all.html', context)
                if Category.objects.filter(cate_name__icontains=search):
                    cate_obj = Category.objects.get(cate_name=search)
                    prod = Product.objects.filter(cid=cate_obj)
                    print("hello category")
                    print(prod)
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
                        'user': user,
                        'category': category,
                        'prod':prod,
                        'brand': brand,
                        'cart':cart,
                        'actual_price':actual_price,
                        'cate':cate,
                        }
                    
                    return render(request, 'store_temp/prod_view_all.html', context)
        return render(request, 'store_temp/prod_view_all.html', context)


    else:
        return redirect('user_login')

def filter_product(request):
    print("helo")
  
    
    return JsonResponse({'data':'helo'})
def filter_price(request,id,m):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        category = Category.objects.all()
        prod = Product.objects.all()
        p = Paginator(prod, 6)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {
            'items': page,
            'user': user,
            'category': category,
            'prod':prod,
            }

        return render(request,'store_temp/filter_prod_view.html',context)
def filter_prod(request, id,name):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        category = Category.objects.all()
        brand = Product.objects.distinct('product_name')
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
                        'user': user,
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
                        'user': user,
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
                'user': user,
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
                'user': user,
                'category': category,
            }
        else:
             context = {
                'error':'Notihg found!!',
                'user': user,
                'category': category,
            }
        
            
        return render(request, 'store_temp/filter_prod_view.html', context)



@never_cache
def logout(request, id):
    if 'uname' in request.session:
        del request.session['uname']
    user = UserSignUp.objects.get(id=id)
    user.logstatus = False
    return redirect('user_login')


def logout_profile(request):
    name = request.session.get('uname')
    user = UserSignUp.objects.get(email=name)
    user.logstatus = False
    if 'uname' in request.session:
        del request.session['uname']

    return redirect('user_login')


def login_otp(request):
    # if request.method=='POST':
        # username = request.POST['username']

    otp = random.randint(1000,9999)
    account_sid = "ACea1db142f98a1e87384255b29ee82e18"
    auth_token = 'a9348108964e344da16c1874447dca33'
    client = Client(account_sid,auth_token)
    msg = client.messages.create(
        body=f"Your OTP is {otp}",
        from_="+16304488428",
        to="+916282787327"
    )
    request.session['otp']=otp
    return render(request, 'login_otp.html')
    #     return redirect(login_home)
    # return render(request, 'login_otp.html')


def product(request):
    prod = Product.objects.all()
    p = Paginator(prod, 1)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {
        'items': page
    }


    return render(request, 'store_temp/prod_view_all.html', context)


def detail_view_user(request, id, uid):
    prod = Product.objects.get(id=id)
    try:
        related_prod = Product.objects.filter(cid=prod.cid)
    except:
        print('null')
    cate = CategoryOffer.objects.all()
    user = UserSignUp.objects.get(id=uid)
    cart = Cart_view.objects.filter(uid_id=user.id).count()
    user.logstatus = True
    context = {
            'prod': prod, 
        'user':user,
        'cart':cart,
        'rel_prod':related_prod,
        'cate':cate,
    }
    return render(request, 'store_temp/detail.html',context)


def add_cart(request, id, pid):
    user = UserSignUp.objects.get(id=id)
    prod = Product.objects.get(id=pid)
    cart_check = Cart_view.objects.filter(uid_id=id,pid_id=pid)
    if cart_check:
        print(cart_check)
    else:
        cart = Cart_view()
        cart.qty = 1
        cart.pid_id = prod.id
        cart.uid_id = user.id
        cart.total_price = float(prod.price*cart.qty)
        cart.tot_amt = float(prod.price * cart.qty)
        cart.save()



    return redirect(cart_view)

def cart_view(request):
    if 'uname' in request.session:
        cart = Cart_view.objects.all().order_by('id')

        user_detail = request.session.get('uname')
        print(user_detail)
        user = UserSignUp.objects.get(email=user_detail)
        user_info = UserSignUp.objects.all()
        # Cart_view.objects.aggregate(Sum('total_price'))

        check = Cart_view.objects.filter(uid_id=user.id)
        print("helo",check)
        print(user.id)
        print(check is NULL)
        print(check)

        car = Cart_view.objects.filter(uid_id=user.id).aggregate(Sum('total_price'))
        return render(request, 'user_temp/cart_page.html', {'cart': check, 'user': user, 'user_info': user_info, 'car': car['total_price__sum']})
    else:
        return redirect(user_login)

def remove_cart(request, id):
    cart1 = Cart_view.objects.get(id=id)
    cart1.delete()
    return redirect(cart_view)

def cart_update(request):
   print('cart')
   body = json.loads(request.body)
   cart = Cart_view.objects.get(id=body['cart_id'])
   cart.qty = body['product_qty']
   cart.total_price = body['total']
   cart.save()
   print("cart_test",body)
   print("update cart")
   return redirect(cart_view)

    

import string    
import random
def profile(request,id):
    user_info = UserSignUp.objects.get(id=id)
    print(user_info.name)
    S=10
    if ReferralCode.objects.filter(user_id=id):
        pass
    else:
        refer = ReferralCode()   
        if refer.status == True:
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
            refer.refer_code = str(ran)
            refer.user = user_info
            refer.status=False
            refer.save()
    if request.method == 'POST':

            name = request.POST.get('name')
            email = request.POST.get('email')
            number = request.POST.get('number')
            print(len(number))
            if len(name) == 0 or name.startswith(' '):
                messages.warning(request,'Please enter a valid name')
            if len(number) != 10 :
                messages.warning(request,'Please enter a valid number')
            else:
                user_info.name = name
                user_info.email = email
                user_info.number = number
                user_info.save()
                messages.success(request,'Updated Successfully!!')
    refer_code = ReferralCode.objects.get(user_id=id)
    wallet = Wallet.objects.get(user_id=id)
    context = {
        'user_info': user_info,
    'refer_code':refer_code.refer_code,
    'wallet':wallet.money,
    }
    return render(request, 'user_temp/profile/profilebase.html', context)

def edit_profile(request, id):
    if 'uname' in request.session:
        user = UserSignUp.objects.get(id=id)
       

       
        return render(request, 'user_temp/profile/profile_Edit.html', {'user': user})
    return redirect(user_login)


def change_psw(request,id):
    if 'uname' in request.session:
        user = UserSignUp.objects.get(id=id)
        if request.method == "POST":

            cur_psw = request.POST.get('cur_psw')
            new_psw = request.POST.get('new_psw')
            con_psw = request.POST.get('con_psw')
            uname = request.session.get('uname')

            print('psw')
            if user.psw == cur_psw:
                if new_psw == con_psw:
                    if user.psw == new_psw:
                        messages.info(request,"Current password and New password are same!!")
                    else:
                        user.psw = new_psw
                        user.psw1 = new_psw
                        user.save()
                else:
                    messages.info(request,"  New Password and Confirm Password are not matching!!")

            else:
                messages.info(request,"Password doesn't matching!!")
        return render(request, 'user_temp/profile/change_psw.html', {'user': user})


def add_wishlist(request,pid,id):
    user = UserSignUp.objects.get(id=id)
    prod = Product.objects.get(id=pid)
    wish = Wish()

    wish.pid_id = prod.id
    wish.uid_id = user.id
    wish.total_price = prod.price
    wish.save()
    return redirect(view_wishlist)


def view_wishlist(request):
    wish = Wish.objects.all()
    user_detail = request.session.get('uname')
    print(user_detail)
    user = UserSignUp.objects.get(email=user_detail)
    user.logstatus = True
    user.save()
    return render(request, 'user_temp/wishlist.html', {'user': user, 'wish': wish})


def remove_wish(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect(view_wishlist)



def address_checkout(request,id):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        address = Address.objects.filter(user=id) 
        if Cart_view.objects.filter(uid_id=id):
            user_info = UserSignUp.objects.get(email=uname)
            wallet = Wallet.objects.get(user_id=user_info)
            cart = Cart_view.objects.filter(uid_id=user_info.id)
            if Cart_view.objects.filter(uid_id=id):

                user = UserSignUp.objects.get(id=id)
                
                amount = Cart_view.objects.filter(uid_id=id).aggregate(Sum('total_price'))
                amt = amount['total_price__sum']
                actual_amt = amt
                coupon = 0
                discount = 0
            if 'coupon_id' in request.session:
                    code_name = request.session.get('coupon_id')
                    print(code_name)
                    coupon = Coupon.objects.get(code=code_name)
                    if coupon:
                        if CouponApplied.objects.filter(coupon_id_id=coupon,user_id=user):
                            print('used once')
                            messages.warning(request,'Already Used :( ')
                        else:
                            discount = coupon.discount_amount
                            amt = amt-coupon.discount_amount
                            print(amt)
                            
                        # if CouponApplied.objects.filter(coupon_id_id=coupon,user_id=user,status=False):
                        #     apply = CouponApplied.objects.get(coupon_id_id=coupon)
                        #     amt=amt-coupon.discount_amount
                        #     apply.status = True
                        #     apply.save()
            

           
            if request.method == 'POST':
                pay_method = request.POST.get('payment')
               
                address = request.POST.get('address')
                print(address)
                print(type(address))
                add=int(address)
                
                pay = Payment()
                pay.user = user
                pay.save()
                if Wallet.objects.filter(user_id=user_info):
                    if request.POST.get('wallet'):
                        amt -= wallet.money
                        wallet.money = 0
                        wallet.save()
                        print(amt)
                        
                if request.POST.get('payment'):     
                    if pay_method == 'COD':
                        
                        pay.payment_method = pay_method
                        pay.status = 'pending'
                        if 'coupon_id' in request.session:
                            if CouponApplied.objects.filter(coupon_id_id=coupon,user_id=user):
                                pass
                            else:
                                applied = CouponApplied()
                                applied.coupon_id = coupon
                                applied.user = user
                                applied.save()
                                del request.session['coupon_id']
                    if pay_method == 'Paypal':
                        if 'coupon_id' in request.session:
                            if CouponApplied.objects.filter(coupon_id_id=coupon,user_id=user):
                                pass
                            else:
                                applied = CouponApplied()
                                applied.coupon_id = coupon
                                applied.user = user
                                applied.save()
                                del request.session['coupon_id']
                        return redirect('payment_methods',pay.pk,amt,add)
               
               
                order = Order()
                order.user = user
                order.payment = pay
                print(amt)
                pay.amount_paid = amt
                pay.save()
                
                address_check = Address.objects.get(id=add)
                order.address_line_1 = address_check.address_line_1
                order.address_line_2 = address_check.address_line_1
                order.first_name = address_check.first_name
                order.last_name = address_check.last_name
                order.phone = address_check.phone
                order.email = address_check.email
                order.country = address_check.country
                order.city = address_check.city
                order.state = address_check.state
                order.zip_code = address_check.zip
                if pay_method == 'rayzorpay':
                    order.is_ordered = True


                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr, mt, dt)
                current_date = d.strftime("%Y%m%d")  # 20210305


                total_amt = Cart_view.objects.filter(uid_id=user_info.id).aggregate(Sum('total_price'))
                order.order_total = total_amt['total_price__sum']
                order.order_number = current_date + str(order.id)
                order.save()
               
                for i in cart:
                    order_prod = OrderProduct()
                    order_prod.order = order
                    order_prod.payment = pay
                    order_prod.user = user
                    if pay_method == 'rayzorpay':
                        order_prod.ordered = False
                    order_prod.product = Product.objects.get(id=i.pid.id)
                    order_prod.quantity = i.qty
                    order_prod.product_price = i.pid.price
                    order_prod.save()
                    product = Product.objects.get(id=i.pid_id)
                    if int(product.stock) < 1:
                        print(product.stock)
                    else:
                        product.stock = int(product.stock)-int(order_prod.quantity)
                    product.save()
                
                if pay_method == 'rayzorpay':
                    
                    return redirect('payment_method_razor',pay.pk,add)   
               
                
                
                cart.delete()
                return redirect(order_complete) 
                 
                
            return render(request, 'store_temp/checkout_address.html', {'cart': cart, 'user': user,'address':address, 'amt': amt,'wallet':wallet,'actual_amt':actual_amt,'coupon':coupon,'discount':discount})
        else:
            print("nothing in cart")
            return render(request, 'user_temp/cart_page.html', {'message': 'Nothing in cart'})

def apply_coupon(request):
    if 'uname' in request.session:
        if request.method == 'POST':
            code = request.POST.get('code')
            uname = request.session.get('uname')
            user = UserSignUp.objects.get(email=uname)
            if Coupon.objects.filter(code=code):
                request.session['coupon_id'] = code
                return redirect('address_checkout',user.id)
                
            else:
                messages.warning(request,'Please enter a valid code')
               

        return render(request,'store_temp/coupon_apply.html')
from django.conf import settings
def payment_method_razor(request,id,add):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        cart = Cart_view.objects.filter(uid_id=user.id)
        sum = Cart_view.objects.filter(uid_id=user.id).aggregate(Sum('total_price'))
        sum_int = int(sum['total_price__sum'])
        print(int(sum['total_price__sum']))
        client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
        payment = client.order.create({'amount':sum_int* 100,'currency':'INR','payment_capture':1})
        address = Address.objects.get(id=add)
        context = {
            'id':id,
            'payment': payment,
            'cart':cart,
            'Grand_total':sum_int,
            'address':address,
            }
        request.session['payment']=payment
    return render(request,'store_temp/payment_razor.html',context)

def payment_methods(request,id,amt,add):
    print(id)
    if 'uname' in request.session:
        # order_prod = OrderProduct.objects.filter(payment_id=id)
        # order = Order.objects.get(payment_id=id)
        # context = {
        # 'order_prod':order_prod,'order':order
        # }
        uname = request.session.get('uname')
        user_info = UserSignUp.objects.get(email=uname)
        cart = Cart_view.objects.filter(uid_id=user_info.id)
        pay = Payment.objects.get(id=id)
        dolor = float(amt)//78
        address = Address.objects.get(id=add)

        
        
        print(dolor)
        context = {
        'pay':pay,
        'amt': amt,
        'cart':cart,
        'add':add,
        'dolor':dolor,
        'address':address,

       }

    return render(request,'store_temp/payment.html',context)

from django.http import JsonResponse
def payment_complete_razor(request,id):
    if 'payment' in request.session:
        payment=request.session.get("payment")


        order = Order.objects.get(payment_id=id)
        order_prod = OrderProduct.objects.filter(order_id=order)
        uname=request.session.get('uname')
        user=UserSignUp.objects.get(email=uname)
        payment=request.session.get("payment")
        pay = Payment.objects.get(id=id)
        pay.payment_method = 'razorpay'
        pay.status = payment['status']
        pay.payment_id = payment['id']
        pay.user = user
        actual_amount=payment['amount']
        actual_amount=actual_amount/100
        pay.amount_paid = actual_amount
        pay.save()
        if pay.status == 'created':
            order.is_ordered = False
            for i in order_prod:
                i.ordered = True
                i.save()
            order.save()
        Cart_view.objects.filter(uid_id=user.id).delete()
        del request.session['payment']
    return render(request,'user_temp/payment_complete.html',{'message': 'Payment Successful!!'})

def payment_confirm(request,id,add,amt):
    if 'uname' in request.session:
        print(id)
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        
        # order = Order.objects.get(payment_id=id)
        body = json.loads(request.body)
        # cart = Cart_view.objects.get(uid=user.id)
        print("hello",body)
        print(body['transId'])
        pay = Payment.objects.get(id=id)
        pay.payment_id = body['transId']
        pay.payment_method = 'Paypal'
        pay.status = body['status']
        pay.amount_paid = amt
        pay.user = user
        pay.save()
        order = Order()
        order.user = user
        order.payment = pay
        address_check = Address.objects.get(id=add)
        order.address_line_1 = address_check.address_line_1
        order.address_line_2 = address_check.address_line_1
        order.first_name = address_check.first_name
        order.last_name = address_check.last_name
        order.phone = address_check.phone
        order.email = address_check.email
        order.country = address_check.country
        order.city = address_check.city
        order.state = address_check.state
        order.zip_code = address_check.zip

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305


        total_amt = Cart_view.objects.filter(uid_id=user.id).aggregate(Sum('total_price'))
        order.order_total = total_amt['total_price__sum']
        order.order_number = current_date + str(order.id)
        order.save()
        cart = Cart_view.objects.filter(uid_id=user.id)
        for i in cart:
            order_prod = OrderProduct()
            order_prod.order = order
            order_prod.payment = pay
            order_prod.user = user

            order_prod.product = Product.objects.get(id=i.pid.id)
            order_prod.quantity = i.qty
            order_prod.product_price = i.pid.price
            order_prod.save()
            product = Product.objects.get(id=i.pid_id)
            product.stock = int(product.stock)-int(order_prod.quantity)
            product.save()
        
        cart.delete()

        data={
            'transId': pay.payment_id,
        }
        return JsonResponse(data)


     
def order_complete(request):

     return render(request,'user_temp/payment_complete.html',{'message': 'Ordered Successful!!'})

def payment_complete(request):

     return render(request,'user_temp/payment_complete.html',{'message': 'payment Successful!!'})
###################################################################################################


def order_view(request):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user_info = UserSignUp.objects.get(email=uname)
        order = Order.objects.filter(user_id=user_info.id,is_ordered=False).order_by('-created_at')
        if request.method == 'POST':
            sel = request.POST['select']
            if sel == 'Cancelled':
                order = Order.objects.filter(user_id=user_info.id, status=sel)
        
            elif sel == 'Confirmed':
                order = Order.objects.filter(user_id=user_info.id, status=sel)
            elif sel == 'Shipped':
                order = Order.objects.filter(user_id=user_info.id, status=sel)
            elif sel == 'Out for Delivery':
                order = Order.objects.filter(user_id=user_info.id, status=sel)
            else:
                order = Order.objects.filter(user_id=user_info.id)
           
        p = Paginator(order, 5)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)   
        return render(request, 'user_temp/profile/orderprofile.html', {'order': page, 'user_info': user_info})

def view_order_detail(request,id):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user_info = UserSignUp.objects.get(email=uname)
        order_prod = OrderProduct.objects.filter(order_id=id)
        order = Order.objects.get(id=id)
        total = 0
        for i in order_prod:
            total += i.quantity*i.product_price

        context = {
            'order_prod':order_prod,
            'total':total,
            'user_info': user_info,
            'order':order,
        }
        return render(request,'user_temp/profile/order_view_product.html', context)




def sort_price(request,name):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        category = Category.objects.all()
        brand = Product.objects.distinct('product_name')
        if request.method == "POST":
            search = request.POST['search']
            if len(search) > 0:
                
                # if Product.objects.filter(product_name__icontains=search):
                #     prod = Product.objects.filter(product_name__icontains=search)
                #     p = Paginator(prod, 6)
                #     page_num = request.GET.get('page', 1)
                #     try:
                #         page = p.page(page_num)
                #     except EmptyPage:
                #         page = p.page(1)
                #     context = {
                #         'items': page,
                #         'user': user,
                #         'category': category,
                #         'prod':prod,
                #         'brand': brand,
                #         }
                #     return render(request, 'store_temp/filter_prod_view.html', context)
                if Product.objects.filter(series__icontains=search):
                    prod = Product.objects.filter(series__icontains=search)
                    p = Paginator(prod, 6)
                    page_num = request.GET.get('page', 1)
                    try:
                        page = p.page(page_num)
                    except EmptyPage:
                        page = p.page(1)
                    context = {
                        'items': page,
                        'user': user,
                        'category': category,
                        'prod':prod,
                        'brand': brand,
                        }
                    
                    return render(request, 'store_temp/filter_prod_view.html', context)
        
        if name == 'low_to_high':
            prod = Product.objects.order_by('price')
        else:
            prod = Product.objects.order_by('-price')
        print(prod)
        p = Paginator(prod, 6)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context = {
            'items': page,
            'user': user,
            'category': category,
                }
        
        return render(request, 'store_temp/filter_prod_view.html', context)


        

def user_index(request):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        cart = Cart_view.objects.filter(uid_id=user.id).count()
        prod = Product.objects.all().order_by('-id')[:9]
        cate = Category.objects.all().order_by('id')
        apply_ban = BannerApplied.objects.all()
        apply_subban = SubBannerApplied.objects.all()
        if CategoryOffer.objects.filter(status=True):
            cate_off = CategoryOffer.objects.get(status=True)
            context = {'user': user,
            'cart':cart,
            'prod':prod,
            'banner':apply_ban,
            'apply_subban':apply_subban,
            'cate':cate,
            'cate_off':cate_off,
            }
            print(prod)
            return render(request, 'store_temp/home_page.html', context)

        context = {'user': user,
        'cart':cart,
        'prod':prod,
        'banner':apply_ban,
        'apply_subban':apply_subban,
        'cate':cate,
        }
        print(prod)
        return render(request, 'store_temp/home_page.html', context)


def user_order_cancel(request,id):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user_info = UserSignUp.objects.get(email=uname)
        order_check = Order.objects.get(id=id)
        
        if order_check.status != 'Cancelled':
            order_check.status = 'Cancelled'
            order_prod = OrderProduct.objects.filter(order_id=id)
            for j in order_prod:
            
                
                prod = Product.objects.get(id=j.product_id)
            
                prod.stock = int(prod.stock) + int(j.quantity)
                
                j.status = 'Cancelled'
                j.save()
                prod.save()
                
            order_check.save()
                

        order_product_view = OrderProduct.objects.filter(user_id=user_info.id)
        total=0
        for i in order_product_view:
            total = total+i.quantity*i.product_price

        return redirect(order_view)

def user_order_returned(request,id):
    if 'uname' in request.session:
        order= Order.objects.get(id=id)
        order.status = 'Returned'
        order.save()
    return redirect(order_view)

def user_product_cancel(request,id):
    if 'uname' in request.session:
        order_prod = OrderProduct.objects.get(id=id)
        
        order_prod.status = 'Cancelled'
        order_prod.save()
    return redirect(order_view)


###################################################################################
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download(request,id):
    v=OrderProduct.objects.get(id=id)
    mydict={
        
        'customerName':v.order.first_name,
        'customerEmail':v.user.email,
        'customerMobile':v.user.number,
        'shipmentAddress':v.order.address_line_1,
        'orderStatus':v.status,
        'productimage':v.product.image,
         'productQuantity':v.quantity,
        'productName':v.product.cid.cate_name,
         'productseries':v.product.series,
        'productPrice':v.product.price,
        'productDescription':v.product.descrip,


    }
    return render_to_pdf('store_temp/download.html',mydict)
##################################################################################

def add_address(request):
    if 'uname' in request.session:
        if request.method == 'POST':
            uname = request.session.get('uname')
            user = UserSignUp.objects.get(email=uname)

            address = Address()
            address.user = user
            address.first_name = request.POST.get('fname')
            address.last_name = request.POST.get('lname')
            address.country = request.POST.get('country')
            address.address_line_1 = request.POST.get('address')
            address.address_line_2 = request.POST.get('address1')
            address.city = request.POST.get('city')
            address.state = request.POST.get('state')
            address.phone = request.POST.get('phone')
            address.zip = request.POST.get('zip')
            address.email = request.POST.get('email')
            address.save()
            

    return render(request,'user_temp/profile/address.html')

def view_address(request):
    if 'uname' in request.session:
        uname = request.session.get('uname')
        user = UserSignUp.objects.get(email=uname)
        address =Address.objects.filter(user=user.id)
        context = {
            'user_info': user,
            'address': address,
        }
    return render(request,'user_temp/profile/view_address.html',context)

def address_chose(request):
    uname = request.session.get('uname')
    user = UserSignUp.objects.get(email=uname)
    address = Address.objects.filter(id=user.id)
    for i in address:
        print(i.first_name)
    context = {
        'address': address,
    }
    return render(request,'store_temp/modal.html',context)