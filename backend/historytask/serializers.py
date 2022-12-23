from .models import KeyInfoModel
from dvadmin.utils.serializers import CustomModelSerializer


class KeyInfoSerializers(CustomModelSerializer):
    class Meta:
        model=KeyInfoModel
        fields=['id_number','car_id','name','car_color','address','time']


class KeyInfoCreateSerializers(CustomModelSerializer):
    class Meta:
        model=KeyInfoModel
        fields=['id_number','car_id','name','car_color','address','time']

    def create(self, validated_data):

        return super(KeyInfoCreateSerializers, self).create(validated_data=validated_data)