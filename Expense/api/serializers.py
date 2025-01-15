from rest_framework import serializers
from api.models import *
from django.contrib.auth import authenticate



from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    image_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Customuser
        fields = ['username', 'password', 'email', 'phone', 'image', 'image_absolute_url']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_image_absolute_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        phone = validated_data.pop('phone', None)
        user = Customuser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        if image:
            user.image = image
            user.save()
        
        if phone:
            user.phone = phone
            user.save()

        return user

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        phone = validated_data.pop('phone', None)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image is not None:
            instance.image = image
        
        if phone is not None:
            instance.phone = phone
        
        instance.save()
        return instance


class WalletSerializer(serializers.ModelSerializer):
    user=serializers.SlugRelatedField(queryset=Customuser.objects.all(), slug_field='username')
    image_absolute_url = serializers.SerializerMethodField() 
    class Meta:
        model=Wallet
        fields=['id','name','created_at','balance','user','image','image_absolute_url']
        
    def get_image_absolute_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
        

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransactionType
        fields="__all__"
        

class TransactionCategorySerializer(serializers.ModelSerializer):
    transaction_type=serializers.SlugRelatedField(queryset=TransactionType.objects.all(),slug_field='name')
    class Meta:
        model=TransactionCategory
        fields=['id','name','transaction_type']
        
        
class TransactionSerializer(serializers.ModelSerializer):
    transaction_type=serializers.SlugRelatedField(queryset=TransactionType.objects.all(),slug_field='name')
    transaction_category=serializers.SlugRelatedField(queryset=TransactionCategory.objects.all(),slug_field='name')
    wallet=serializers.SlugRelatedField(queryset=Wallet.objects.all(),slug_field='name')
    user=serializers.SlugRelatedField(queryset=Customuser.objects.all(),slug_field='username')
    
    
    class Meta:
        model=Transaction
        fields=["id",'transaction_category','transaction_type','amount','wallet','date','description','user']
        

        
    