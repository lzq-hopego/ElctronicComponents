from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from ElctronicComponent.models import (Elctroniccomponents,ElctroniccomponentsLog)
from django.db.models import (Q,Sum,Count)
from django.db.models.functions import TruncDate
from django.utils import timezone
import datetime
import json

# Create your views here.


def home(request):
    return render(request,'index.html')




# 元器件序列化器
class ComponentsSerializers(serializers.ModelSerializer):
    # 元器件序列化器
    class Meta:
        model=Elctroniccomponents
        fields='__all__'
        read_only_fields = ['id']
# 元器件日志序列化器
class ComponentsLogSerializers(serializers.ModelSerializer):
    # 元器件序列化器
    class Meta:
        model=ElctroniccomponentsLog
        fields='__all__'
        read_only_fields = ['id']

## 添加日志
def addlog(request,msg):
    data=request.data
    data['uselog']=msg
    componentslog_ser=ComponentsLogSerializers(data=data)
    if not componentslog_ser.is_valid():
        print(componentslog_ser.errors)
        return Response({'error':{'code':'日志添加失败'}})
    componentslog_ser.save()

# 元器件列表
class components(APIView):
    authentication_classes=[]
    def get(self,request):

        page=request.query_params.get('page',1)
        name=request.query_params.get('name','')
        if page=='':
            page=1
        elif page==0:
            page=1
        page=int(page)-1
        # print(page)

        #准备搜索时需要用到的数据
        data_dict={}
        if name:
          data_dict["name__contains"]=name

        #   category

        # 处理从那个地方开始查询和结束
        page_size=6#定义每页的长度
        page_start=page*page_size
        page_end=(page+1)*page_size

        components_data=Elctroniccomponents.objects.filter(Q(Q(name__icontains=name)|Q(category__icontains=name))|Q(model__icontains=name)).all()
        # print(components_data.get('name'))
        components_ser=ComponentsSerializers(instance=components_data[page_start:page_end],many=True)

        # print(res)
        return Response({'totalItems':components_data.count(),'data':components_ser.data})


    def post(self,request):
        # print(request.data)
        
        return Response("ok")


# 日志列表
class componentslog(APIView):
    authentication_classes=[]
    def get(self,request):

        page=request.query_params.get('page',1)
        name=request.query_params.get('name','')
        if page=='':
            page=1
        page=int(page)-1
        # print(page)

        #准备搜索时需要用到的数据
        data_dict={}
        if name:
          data_dict["name__contains"]=name

        #   category

        # 处理从那个地方开始查询和结束
        page_size=6#定义每页的长度
        page_start=page*page_size
        page_end=(page+1)*page_size

        components_data=ElctroniccomponentsLog.objects.filter(Q(Q(name__icontains=name)|Q(category__icontains=name))|Q(model__icontains=name)).all()
        # print(components_data.get('name'))
        components_ser=ComponentsLogSerializers(instance=components_data[page_start:page_end],many=True)

        # print(res)
        return Response({'totalItems':components_data.count(),'data':components_ser.data})


    def post(self,request):
        # print(request.data)
        
        return Response("ok")

# 编辑元器件
class edit_components(APIView):
    def post(self,request):
        components_obj=Elctroniccomponents.objects.filter(id=request.data.get('id',None)).first()
        components_ser=ComponentsSerializers(data=request.data,instance=components_obj)

        if not components_ser.is_valid():
            print(components_ser.errors)
            return Response({'error':{'code':10008}})
        components_ser.save()

        addlog(request,'编辑元器件元器件')
        return Response("ok")

# 入库
class addnum_components(APIView):
    def get(self,request):
        id=request.query_params.get('id',None)
        num=request.query_params.get('num',0)
        try:
            num=int(num)
        except:
            return Response("error")
        components_obj=Elctroniccomponents.objects.filter(id=id)
        stock=components_obj.first().stock
        stock+=num
        components_obj.update(stock=stock)

        componentslog_ser=ComponentsSerializers(instance=components_obj.first())
        addlog(componentslog_ser,'入库'+str(num))
        return Response("ok")
    
# 出库
class removenum_components(APIView):
    def get(self,request):
        id=request.query_params.get('id',None)
        num=request.query_params.get('num',0)
        try:
            num=int(num)
        except:
            return Response("error")
        components_obj=Elctroniccomponents.objects.filter(id=id)
        stock=components_obj.first().stock
        stock-=num
        components_obj.update(stock=stock)

        componentslog_ser=ComponentsSerializers(instance=components_obj.first())
        addlog(componentslog_ser,'出库'+str(num))
        return Response("ok")
    

# 删除元器件
class delete_components(APIView):
    def get(self,request):
        # request_data=json.loads(request.body)
        id=request.query_params.get('id',None)
        components=Elctroniccomponents.objects.filter(id=id)
        componentslog_ser=ComponentsSerializers(instance=components.first())
        components.delete()
        addlog(componentslog_ser,'删除元器件')
        return Response("ok")

# 添加元器件
class records(APIView):
    authentication_classes=[]
    def get(self,request):
        return Response("ok")
    def post(self,request):
        # request_data=json.loads(request.body)
        # print(request.data)
        data=request.data
        components_obj=ComponentsSerializers(data=data)
        if not components_obj.is_valid():
            print(components_obj.errors)
            return Response({'error':{'code':10008}})
        components_obj.save()

        
        addlog(components_obj,'添加元器件')


        return Response({'id':components_obj.data.get("id")})

# 后端搜索接口
class search_components(APIView):
    def get(self,request):
        
        return Response("ok")


# 仪表盘数据
class get_sum_data(APIView):
    def get(self,request):
        # 获取当前日期
        today = datetime.datetime.now()
        # 获取本月的第一天
        this_month_start = today.replace(day=1)
        # 获取上个月的最后一天
        last_month_end = this_month_start - datetime.timedelta(days=1)
        # 获取上个月的第一天
        last_month_start = last_month_end.replace(day=1)
        # 查询本月的数据
        this_month_data = Elctroniccomponents.objects.filter(careate_time__gte=this_month_start, careate_time__lt=today)
        # 查询上个月的数据
        last_month_data = Elctroniccomponents.objects.filter(careate_time__gte=last_month_start, careate_time__lt=last_month_end)
        # 查询库存较低的
        this_month_low_stock=this_month_data.filter(stock__lt=3)
        last_month_low_stock=last_month_data.filter(stock__lt=3)
        # 计算本月库存总和
        this_month_stock_total = this_month_data.aggregate(Sum('stock'))['stock__sum'] or 0
        # 计算上个月库存总和
        last_month_stock_total = last_month_data.aggregate(Sum('stock'))['stock__sum'] or 0
        category_stocks=Elctroniccomponents.objects.values('category').annotate(total_stock=Sum('stock'))
        stats = Elctroniccomponents.objects.aggregate(
                total_items=Count('id'),  # 总条目数
                total_stock=Sum('stock')  # 库存总和
            )
        low_stock=Elctroniccomponents.objects.filter(stock__lt=3)
        ls=[]
        ls_stock=[]
        for item in category_stocks:
            # print(f"类别: {item['category']}, 总库存: {item['total_stock']}")
            ls.append(item['category'])
            ls_stock.append(item['total_stock'])

        today = timezone.now().date()
        one_month_ago = today - datetime.timedelta(days=29)
        
        daily_stocks = Elctroniccomponents.objects.filter(
            careate_time__date__range=[one_month_ago, today]
        ).annotate(
            date=TruncDate('careate_time')
        ).values(
            'date'
        ).annotate(
            total_stock=Sum('stock')
        ).order_by(
            'date'
        )
        formatted_data_date=[item['date'].strftime('%Y-%m-%d') for item in daily_stocks]
        formatted_data_stock=[item['total_stock'] or 0 for item in daily_stocks]


        today = timezone.now().date()
        yesterday = today - datetime.timedelta(days=1)
        
        today_count = ElctroniccomponentsLog.objects.filter(index_time__date=today).count()
        yesterday_count = ElctroniccomponentsLog.objects.filter(index_time__date=yesterday).count()

        # print(formatted_data)

        # print(f"本月库存总和: {this_month_stock_total},{this_month_data.count()}")
        # print(f"上个月库存总和: {last_month_stock_total},{last_month_data.count()}")
        # print(f"低库存:{this_month_low_stock.count()},{last_month_low_stock.count()}")

        return Response({'low_stock':low_stock.count(),'total_stock':stats['total_stock'],'total_items':stats['total_items'],\
                         'this_month_stock_total':this_month_stock_total,'last_month_stock_total':last_month_stock_total\
                         ,'this_month_data':this_month_data.count(),'last_month_data':last_month_data.count()\
                            ,'this_month_low_stock':this_month_low_stock.count(),'last_month_low_stock':last_month_low_stock.count(),\
                                'category_stock':{'name':ls,'stock':ls_stock},\
                                    'formatted_data':{'date':formatted_data_date,'total_stock':formatted_data_stock}\
                                        ,'today_count':today_count,'yesterday_count':yesterday_count})



