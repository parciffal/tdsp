from django.db import models


class History(models.Model):
    
    class Meta:
        verbose_name_plural = "History"

    def __str__(self) -> str:
        return self.name

    def as_json(self):
        data = {
            "id": self.id,
            
        }
        return data