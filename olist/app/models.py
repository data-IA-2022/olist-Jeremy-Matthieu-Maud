from django.db import models
from rest_framework import serializers
class product_category_name_translation(models.Model):
    product_category_name = models.CharField(max_length=200, primary_key=True)
    product_category_name_english = models.CharField(max_length=200)
    product_category_name_french = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_category_name_translation'
    def __str__(self):
        return self.product_category_name


class TraductionSerializer(serializers.ModelSerializer):
    product_category_name = serializers.CharField()
    product_category_name_english = serializers.CharField()
    product_category_name_french = serializers.CharField()

    class Meta:
        model = product_category_name_translation
        fields = ['product_category_name', 'product_category_name_english', 'product_category_name_french']
