
from ast import main
from datetime import datetime
from math import prod
from django.shortcuts import render, redirect
from .models import *
from user_app.models import *
import os
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import *
from django.contrib import messages
# Create your views here.

@never_cache
def add_cate(request):
    if request.method == 'POST':

        cate_name = request.POST['cate_name']
        cate = Category.objects.create(cate_name=cate_name)
        cate.save()
    return render(request, 'admin_temp/cate_form.html')

def remove_cate(request,id):
    if 'email' in request.session:
        cate = Category.objects.get(id=id)
        cate.delete()
        return redirect(cate_display)

@never_cache
def cate_display(request):
    if 'email' in request.session:

        cate = Category.objects.all()
        return render(request, 'admin_temp/cate_display.html', {'cate': cate})
    return redirect(admin_login)

@never_cache
def user_manage(request):
    if 'email' in request.session:

        m_user = UserSignUp.objects.all().order_by('id')
        return render(request, 'admin_temp/usermange.html', {'m_user': m_user})
    return redirect(admin_login)

@never_cache
def user_block(request, id):

    block_user = UserSignUp.objects.get(id=id)
    if block_user.status is True:
        block_user.status = False
    else:
        block_user.status = True
    block_user.save()
    return redirect(user_manage)

@never_cache
def add_product(request):


    cate_select = Category.objects.all()
    if request.method == 'POST':

        cate_name = request.POST['sel_opt']
        cate = Category.objects.get(cate_name=cate_name)
        prod = Product()
        # prod.product_name = request.POST.get('brand')
        prod.cid = cate
        prod.series = request.POST.get('series')
        prod.price = request.POST.get('price')
        prod.price_actual = request.POST.get('price')
        prod.stock = request.POST.get('stock')
        prod.descrip = request.POST.get('desc')
        prod.p_brand = request.POST.get('pbrand')
        prod.p_name = request.POST.get('pname')
        prod.ssd = request.POST.get('ssd')
        prod.mem = request.POST.get('mem')
        prod.ram = request.POST.get('ram')
        prod.os = request.POST.get('os')
        prod.is_offer_apply = False
        if len(request.FILES) != 0:
            prod.image = request.FILES.get('image')
            prod.image1 = request.FILES.get('image1')
            prod.image2 = request.FILES.get('image2')
            prod.image3 = request.FILES.get('image3')
        prod.save()
        
        messages.info(request,"Product added successfully!!")

        #prod = ProductView()
        # prod.product_name =
        
        print(cate.id)
        
        

    return render(request, 'admin_temp/addproduct.html', {'cate_select': cate_select})

@never_cache
def update_prod(request, id):
    cate_select = Category.objects.all()
    prod = Product.objects.get(id=id)
    if request.method == 'POST':
        cate_name = request.POST['sel_opt']
        cate = Category.objects.get(cate_name=cate_name)
        if len(request.FILES) != 0:
            if len(prod.image) > 0:
                os.remove(prod.image.path)
            prod.image = request.FILES['image']


            # prod.image1 = request.FILES['image1']
            # prod.image2 = request.FILES['image2']

        prod.product_name = request.POST.get('brand')
        prod.descrip = request.POST.get('desc')
        prod.series = request.POST.get('series')
        prod.stock = request.POST.get('stock')
        prod.ssd = request.POST.get('ssd')
        prod.os = request.POST.get('os')
        prod.p_brand = request.POST.get('pbrand')
        prod.p_name = request.POST.get('pname')
        prod.ram = request.POST.get('ram')
        prod.price = request.POST.get('price')
        prod.mem = request.POST.get('mem')
        prod.cid = cate
        prod.save()
        messages.info(request,'updated successfully!!')
        return redirect(product_page)
    return render(request, 'admin_temp/updateproduct.html', {'prod': prod, 'cate_select': cate_select})
@never_cache
def delete_prod(request, id):


    prod = Product.objects.get(id=id)
    if len(prod.image) > 0:
        os.remove(prod.image.path)
    prod.delete()

    return redirect(product_page)
@never_cache
def product_page(request):

    prod = Product.objects.all().order_by('id')
    p = Paginator(prod, 2)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    return render(request, 'admin_temp/product.html', {'prod': page})



@never_cache
def admin_login(request):
    if 'email' in request.session:
        return redirect('user_manage')
    if request.method == 'POST':
        email = request.POST['email']
        psw = request.POST['psw']
        ad = AdminDetail.objects.filter(email=email, psw=psw)
        if ad:
            request.session['email'] = email
            return redirect(user_manage)
    return render(request, 'admin_temp/admin_login.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        a=request.session.get('email')
        print("hello",a)
    return redirect(admin_login)


def order_view_admin(request):
    if 'email' in request.session:
        order = Order.objects.all().order_by('id')
        p = Paginator(order, 5)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        return render(request, 'admin_temp/orderview.html', {'order': page})

def order_detail(request,id):
    if 'email' in request.session:
        order_product = OrderProduct.objects.filter(order_id=id)
        if request.method == 'POST':
            status = request.POST['status']
            order = Order.objects.get(id=id)
            order.status = status
            order.save()
            for i in order_product:
                i.status = status
                i.save()
        order = Order.objects.get(id=id)
        
        
        p = Paginator(order_product, 1)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        return render(request, 'admin_temp/order_detailview.html', {'order_product': page, 'order': order})


def order_cancel(request,id):
    if 'email' in request.session:
        order_check = Order.objects.get(id=id)
        order_check_prod = OrderProduct.objects.filter(order_id=id)
        if order_check.is_ordered is False:
            order_check.is_ordered = True
            for i in order_check_prod:
                i.ordered = True
                i.save()
            order_check.status = 'Cancelled'
            order_check.save()
        if order_check.status == 'Cancelled':
            for i in order_check_prod:
                i.status = 'Cancelled'
                i.save()
        
        
        return redirect(order_view_admin)

def order_product_detail(request,id):
    if 'email' in request.session:
        order_prod = OrderProduct.objects.get(id=id)
        if request.method == 'POST':
            order_prod.status = request.POST.get('status')
            order_prod.save()
        return render(request,'admin_temp/product_order_detail.html',{'order_prod': order_prod})

def order_cancel_product(request,id):
    if 'email' in request.session:
        
        
        order_check_prod = OrderProduct.objects.get(id=id)
        if order_check_prod.status != 'Cancelled':
            order_check_prod.status = 'Cancelled'
            order_check_prod.save()
        return render(request, 'admin_temp/order_detailview.html')

def homepage_admin(request):
    prod = Product.objects.all()
    order_count = []
    for i in prod:
        count = OrderProduct.objects.filter(product_id=i.id).count()
        order_count.append(count)
    print(order_count)
    user = UserSignUp.objects.all().count()
    order = Order.objects.all().count()
    total=0
    for i in prod:
        total=total+int(i.stock)
    cate = Category.objects.all()
    cate_count = []
    for i in cate:
        count_cate = Product.objects.filter(cid_id=i.id).count()
        cate_count.append(count_cate)
    print(cate_count)
    context = {
        'prod':prod,
    'order_count':order_count,
    'user':user,
   'order':order,
   'total':total,
   'cate':cate,
   'cate_count':cate_count,
    }
   
    
    return render(request,'admin_temp/dashboard.html',context)

#########coupon managment##############

def coupon_add(request):
    if 'email' in request.session:
        if request.method == 'POST':
            cname = request.POST.get('cname')
            ccode = request.POST.get('ccode')
            camount = request.POST.get('camount')
            cpercentage = request.POST.get('cpercentage')
            cdescription = request.POST.get('cdescription')
            valid = request.POST.get('valid')
            if Coupon.objects.filter(name=cname):
                info = 'Already Exist!!'
                context={
               'info':info,
            }
                return render(request,'admin_temp/couponadd.html',context)
            if Coupon.objects.filter(code=ccode):
                info1 = 'Already Exist!!'
                context={
               'info1':info1,
            }
                return render(request,'admin_temp/couponadd.html',context)
            else:
                coupon = Coupon()
                coupon.name = cname
                coupon.code = ccode
                coupon.discount_amount = camount
                coupon.discountpercentage = cpercentage
                coupon.description = cdescription
                coupon.valid_till = valid
                coupon.save()
                messages.success(request,'Successfully Added!!')
            
        return render(request,'admin_temp/couponadd.html')

def coupon(request):
    if 'email' in request.session:
        coupon = Coupon.objects.all()
        context = {
            'coupon':coupon,
        }
        
        return render(request,'admin_temp/coupon_view.html',context)
def del_coupon(request,id):
    if 'email' in request.session:
        print(id)
        coupon_element = Coupon.objects.get(id=id)

        coupon_element.delete()
        messages.success(request,'Deleted Successfully')
        return redirect(coupon)

 ############offermanagement############# 

def offer_add(request):
    if 'email' in request.session:
         cate = Category.objects.all()
         context = {
                'cate':cate,
            }
         if request.method == "POST":
            cate_id= request.POST.get('cate')
            cate_name = Category.objects.get(id=cate_id)
            name = request.POST.get('Oname')
            if CategoryOffer.objects.filter(Name=name):
                info='Already Exist!!'
                context = {
                'cate':cate,
                'info':info,
            }
                return render(request,'admin_temp/offer_cate.html',context)
                
            else:
                cate_off = CategoryOffer()
                cate_off.cid=cate_name
                
                cate_off.Name = name
                cate_off.valid_till = request.POST.get('valid')
                cate_off.percentage = request.POST.get('Opercentage')
                cate_off.description = request.POST.get('Odescription')
                cate_off.save()
                messages.success(request,'Added Successfully!!')
            
         return render(request,'admin_temp/offer_cate.html',context)


def offer_view(request):
    if 'email' in request.session:
        cate_off = CategoryOffer.objects.all().order_by('id')
        context = {
          "cate_off":cate_off,
        }
        return render(request,'admin_temp/offer_view.html',context)
def offer_del(request,id):
    if 'email' in request.session:
        cate_off = CategoryOffer.objects.get(id=id)
        if cate_off.status == True:
            cate_off.status = False
        else:
            cate_off.status = True
        cate_off.save()
        return redirect(offer_view)

def offer_delete(request,id):
    if 'email' in request.session:
        cate_off = CategoryOffer.objects.get(id=id)
        cate_off.delete()
        return redirect(offer_view)

def offer_edit(request,id):
    if 'email' in request.session:
        cate_off = CategoryOffer.objects.get(id=id)
        if request.method =='POST':
            cate_off.Name = request.POST.get('Oname')
            cate_off.percentage = request.POST.get('Opercentage')
            cate_off.valid_till = request.POST.get('valid')
            cate_off.save()
            messages.success(request,'Updated Successfully!!')
            return redirect(offer_view)
    context = {
        'cate_off':cate_off
    }
    return render(request,'admin_temp/edit_cateoffer.html',context)
def product_offer(request):
    if 'email' in request.session:
        prod_off = ProductOffer.objects.all()
        context = {
           'prod_off':prod_off,
        }
        return render(request,'admin_temp/product_offer.html',context)
def product_offer_add(request):
    if 'email' in request.session:
        prod = Product.objects.all()
        context = {
            'prod':prod,
        }
        if request.method == "POST":
            prod_id= request.POST.get('prod')
            prod_name = Product.objects.get(id=prod_id)
            name = request.POST.get('Oname')
            if ProductOffer.objects.filter(Name=name):
                info='Already Exist!!'
                context = {
                'prod_name':prod_name,
                'info':info,
            }
                return render(request,'admin_temp/add_product_offer.html',context)
                
            else:
                prod_off = ProductOffer()
                prod_off.pid=prod_name
                
                prod_off.Name = name
                prod_off.valid_till = request.POST.get('valid')
                prod_off.percentage = request.POST.get('Opercentage')
                prod_off.description = request.POST.get('Odescription')
                prod_off.save()
                messages.success(request,'Added Successfully!!')
    return render(request,'admin_temp/add_product_offer.html',context)
def product_offer_delete(request,id):
    if 'email' in request.session:
        prod_off = ProductOffer.objects.get(id=id)
        prod_off.delete()
        prod_off.save()
        return redirect(product_offer)
    
def product_offer_cancel(request,id):
    if 'email' in request.session:
        prod_off = ProductOffer.objects.get(id=id)
        if prod_off.status == True:
            prod_off.status = False
        else:
            prod_off.status = True
        prod_off.save()
        return redirect(product_offer)

def main_banner_add(request):
    if 'email' in request.session:
        if request.method == "POST":
            main_ban = FrontBanner()
            main_ban.head = request.POST.get('head')
            main_ban.description = request.POST.get('desc')
            if len(request.FILES) != 0:
                main_ban.banner1 = request.FILES.get('image1')
                main_ban.banner2 = request.FILES.get('image2')
                main_ban.banner3 = request.FILES.get('image3')
            main_ban.save()
    return render(request,'admin_temp/main_banner_add.html')
def banner_view(request):
    if 'email' in request.session:
        main_ban = FrontBanner.objects.all().order_by('id')
        context = {
            'banner':main_ban,
        }
    return render(request,'admin_temp/banner_view.html',context)
def main_banner_select(request,id):
    if 'email' in request.session:
        main_ban = FrontBanner.objects.get(id=id)
        ban = BannerApplied.objects.all()
        print(ban is True)
        for i in ban:
            print(i.id)
        print('ban',ban)
        if ban:
            clr_ban = BannerApplied.objects.all()
            print(clr_ban)
            clr_ban.delete()
            app_ban = BannerApplied()
            app_ban.banner = main_ban
            app_ban.save()
        else:
            print('ban')
            app_ban = BannerApplied()
            app_ban.banner = main_ban
            app_ban.save()
        # if main_ban.select == False:
        #     main_ban.select = True
            
        #     main_ban.save()
        #     ban_hide = FrontBanner.objects.all()
        #     for i in ban_hide:
        #         print('i',i)
        #         if i.select == False:
        #             i.status = True
        #             i.save()
        
        return redirect(banner_view)

def sub_banner_view(request):  
    if 'email' in request.session:
        sub_banner = SubBanner.objects.all()
        context = {
            'banner' : sub_banner,
        }
    return render(request,'admin_temp/sub_banner_view.html',context)

def sub_banner_add(request):
    if 'email' in request.session:
        if request.method == "POST":
            sub_banner = SubBanner()
            sub_banner.head1 = request.POST.get('title1')
            sub_banner.head2 = request.POST.get('title2')
            sub_banner.head3 = request.POST.get('title3')
            if len(request.FILES) != 0:
                sub_banner.banner1 = request.FILES.get('image1')
                sub_banner.banner2 = request.FILES.get('image2')
                sub_banner.banner3 = request.FILES.get('image3')
            sub_banner.save()
            pass
    return render(request,'admin_temp/sub_banner_add.html')

def sub_banner_select(request,id):
    if 'email' in request.session:
        sub_banner = SubBanner.objects.get(id=id)
        ban = SubBannerApplied.objects.all()
        # print(ban is True)
        # for i in ban:
        #     print(i.id)
        # print('ban',ban)
        if ban:
            clr_ban = SubBannerApplied.objects.all()
            print(clr_ban)
            clr_ban.delete()
            app_ban = SubBannerApplied()
            app_ban.subbanner = sub_banner
            app_ban.save()
        else:
            print('ban')
            app_ban = SubBannerApplied()
            app_ban.subbanner = sub_banner
            app_ban.save()
        # if main_ban.select == False:
        #     main_ban.select = True
            
        #     main_ban.save()
        #     ban_hide = FrontBanner.objects.all()
        #     for i in ban_hide:
        #         print('i',i)
        #         if i.select == False:
        #             i.status = True
        #             i.save()
        
        return redirect(sub_banner_view)
###############sales report#########################
def sales_report_date(request):
    if 'email' in request.session:
        data = OrderProduct.objects.all()
        if request.method == 'POST':
            if request.POST.get('month'):
                month = request.POST.get('month')
                print(month)
                data = OrderProduct.objects.filter(created_at__icontains=month)
                
                if data:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                        for i in data:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                    else:
                        for i in data:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                else:
                    messages.warning(request,"Nothing Found!!")
            if request.POST.get('date'):
                date = request.POST.get('date')
                print(date)
                
                date_check = OrderProduct.objects.filter(created_at=date)
                print(date_check)
                if date_check:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                
                        for i in date_check:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                    else:
                        for i in date_check:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                else:
                    messages.warning(request,"Nothing Found!!")
            if request.POST.get('date1'):
                date1 = request.POST.get('date1')
                date2 = request.POST.get('date2')
                data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
                if data_range:
                    if SalesReport.objects.all():
                        SalesReport.objects.all().delete()
                
                        for i in data_range:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                    else:
                        for i in data_range:
                            sales = SalesReport()
                            sales.productName = i.product.series
                            sales.categoryName = i.product.cid.cate_name
                            sales.date = i.created_at
                            sales.quantity = i.quantity
                            sales.productPrice = i.product_price
                            sales.save()
                        sales = SalesReport.objects.all()
                        total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                        context = { 'sales':sales,'total':total['productPrice__sum']}
                        return render(request,'admin_temp/sales_report_.html',context)
                else:
                    messages.warning(request,"Nothing Found!!")
        if data:
            if SalesReport.objects.all():
                SalesReport.objects.all().delete()
                for i in data:
                    sales = SalesReport()
                    sales.productName = i.product.series
                    sales.categoryName = i.product.cid.cate_name
                    sales.date = i.created_at
                    sales.quantity = i.quantity
                    sales.productPrice = i.product_price
                    sales.save()
                sales = SalesReport.objects.all()
                total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                context = { 'sales':sales,'total':total['productPrice__sum']}
                return render(request,'admin_temp/sales_report_.html',context)

            else:
                for i in data:
                    sales = SalesReport()
                    sales.productName = i.product.series
                    sales.categoryName = i.product.cid.cate_name
                    sales.date = i.created_at
                    sales.quantity = i.quantity
                    sales.productPrice = i.product_price
                    sales.save()
                sales = SalesReport.objects.all()
                total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                context = { 'sales':sales,'total':total['productPrice__sum']}
                return render(request,'admin_temp/sales_report_.html',context)
            
        else:
            messages.warning(request,"Nothing Found!!")
        
        return render(request,'admin_temp/sales_report_.html')

from django.db.models import Avg, Count, Min, Sum

# def sales_report_view(request):
#     if 'email' in request.session:
#         sales = SalesReport.objects.all()
#         total = SalesReport.objects.all().aggregate(Sum('productPrice'))
#         print(total)
        
#         context = {
#             'sales':sales,
#             'total':total['productPrice__sum'],
#         }
#     return render(request,'admin_temp/sales_report_view.html',context)
########################################################################
import xlwt
def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response


def export_to_pdf(request):
    prod = Product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sale_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response