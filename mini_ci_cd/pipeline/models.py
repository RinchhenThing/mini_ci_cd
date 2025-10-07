from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=100)
    repo_url = models.URLField()
    branch = models.CharField(max_length=100, default="main")

    def __str__(self):
        return self.name

class Build(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commit_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    log = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repository.name} - {self.commit_id[:7]} - {self.status}"
