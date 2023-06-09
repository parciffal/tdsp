from django.conf import settings
from django.core.management.base import BaseCommand

import pandas as pd
import os

from ...models import Category

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'Content-Taxonomy-1.0.xlsx')
        data = pd.read_excel(file_path).to_dict()
        dataframe = pd.DataFrame(data, columns=['IAB Code', 'Tier', 'IAB Category'])
        for i in dataframe.values.tolist():
            if i[1] == 'Tier 1':
                try:
                    Category.objects.create(code=i[0],
                                            name=i[2])
                except:
                    pass      
        for i in dataframe.values.tolist():
            if i[1] == 'Tier 2':
                try:
                    kl = str(i[0]).split('-')
                    categ = Category.objects.get(code=kl[0])
                    Category.objects.create(code=i[0], 
                                            name=i[2],
                                            super_category=categ)
                except: 
                    pass
