from rest_framework.serializers import ModelSerializer
from action import models

# foreign serializers
pass


# tags serializers
class TagsSerializer(ModelSerializer):
    
    class Meta:
        model = models.Tags
        fields = '__all__'
