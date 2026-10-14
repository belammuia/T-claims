from django.conf import settings
from django.db import models



class Claim(models.Model):
    class Severity(models.TextChoices):
        MINOR = "minor", "Minor"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under Review"
        FLAGGED = "flagged", "Flagged for Audit"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    class Queue(models.TextChoices):
        FAST_TRACK = "fast_track", "Fast-Track"
        OFFICER = "officer", "Claims Officer"
        SENIOR = "senior", "Senior Claims Officer"
        AUDIT = "audit", "Fraud / Audit Review"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="claims")
    vehicle = models.ForeignKey("policies.Vehicle", on_delete=models.PROTECT, related_name="claims")
    claim_date = models.DateTimeField(auto_now_add=True)
    incident_date = models.DateField()
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=Severity.choices, blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.SUBMITTED)

    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2)
    vehicles_involved = models.PositiveSmallIntegerField(default=1)
    has_injury = models.BooleanField(default=False)
    third_party_involved = models.BooleanField(default=False)
    severe_structural_damage = models.BooleanField(default=False)
    queue = models.CharField(max_length=15, choices=Queue.choices, blank=True)
    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="assigned_claims",
    )
    multi_policy_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"Claim #{self.pk} ({self.status})"


class ClaimPolicy(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="claim_policies")
    policy = models.ForeignKey("policies.Policy", on_delete=models.PROTECT)
    vehicle = models.ForeignKey("policies.Vehicle", on_delete=models.PROTECT)

    class Meta:
        unique_together = ("claim", "policy")


class SupportingDocument(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50) 
    file = models.FileField(upload_to="claim_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)




class TriageRule(models.Model):
    rule_name = models.CharField(max_length=100)
    condition = models.JSONField()  
    severity_level = models.CharField(max_length=10, choices=Claim.Severity.choices)
    priority = models.CharField(max_length=10, choices=Claim.Priority.choices)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.rule_name