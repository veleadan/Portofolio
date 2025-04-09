from django.db import models
import json


class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    keyword_matches = models.TextField(blank=True)  # Store JSON as a string

    def save(self, *args, **kwargs):
        # Serialize `keyword_matches` to JSON string before saving
        self.keyword_matches = json.dumps(self.keyword_matches)
        super().save(*args, **kwargs)

    def get_keyword_matches(self):
        # Deserialize JSON string back to Python dictionary
        return json.loads(self.keyword_matches)

    def __str__(self):
        return f"Resume {self.id} - {self.file.name}"