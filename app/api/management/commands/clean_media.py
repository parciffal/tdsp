from django.conf import settings
from django.core.management.base import BaseCommand

import shutil
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, 'creative')
        shutil.rmtree(file_path)
        os.mkdir(file_path)