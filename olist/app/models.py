from django.db import models

class product_category_name_translation(models.Model):
    product_category_name = models.CharField(max_length=200, primary_key=True)
    product_category_name_english = models.CharField(max_length=200)
    product_category_name_french = models.CharField(max_length=200)

    class Meta:
        db_table = 'product_category_name_translation'
    def __str__(self):
        return self.product_category_name
