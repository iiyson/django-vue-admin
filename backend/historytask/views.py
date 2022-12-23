from django.http import QueryDict

from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.viewset import CustomModelViewSet
from .models import KeyInfoModel
from .serializers import KeyInfoSerializers,KeyInfoCreateSerializers
from application.dizhi1 import extract
# Create your views here.


class KeyInfoViewset(CustomModelViewSet):
    queryset = KeyInfoModel.objects.all()
    serializer_class = KeyInfoSerializers
    create_serializer_class = KeyInfoCreateSerializers
    filter_fields = ['id_number','car_id','name','car_color','address','time']
    search_fields = ['id_number','car_id','name','car_color','address','time']

    def create(self, request, *args, **kwargs):
        # 初始化新的querydict
        q=QueryDict('txt')


        txt_data=extract(request)
        txt_data.get('name',request.data.get('name'))
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")