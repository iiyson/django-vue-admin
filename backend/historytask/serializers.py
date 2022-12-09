from .models import KeyInfoModel
from dvadmin.utils.serializers import CustomModelSerializer


class KeyInfoSerializers(CustomModelSerializer):
    class Meta:
        model=KeyInfoModel
        fields='__all__'
