from django.db import models
from django.conf import settings

import pandas as pd

import os

class Category(models.Model):
    code = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            "code": self.code,
            "name": self.name,
        }
        return data
    
    def init_categorys(self):
        from time import time
        start_time = time()
        file_path = os.path.join(settings.BASE_DIR, 'Content-Taxonomy-1.0.xlsx')        
        data = pd.read_excel(file_path).to_dict()
        dataframe = pd.DataFrame(data, columns=['IAB Code', 'Tier', 'IAB Category'])
        f_data = dataframe.loc[dataframe['Tier'].isin(['Tier 1'])]
        for i in f_data.values.tolist():
            Category.objects.create(code=i[0],
                                    name=i[2])
        print(time() - start_time)
        

cate = Category()
cate.init_categorys()