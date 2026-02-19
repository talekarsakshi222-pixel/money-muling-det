"""Transaction data models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    """Transaction model matching CSV schema."""
    transaction_id: str
    sender_id: str
    receiver_id: str
    amount: float = Field(gt=0)
    timestamp: datetime

    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        """Parse timestamp from string format YYYY-MM-DD HH:MM:SS."""
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
        return v


class SuspiciousAccount(BaseModel):
    """Suspicious account with detection results."""
    account_id: str
    suspicion_score: float = Field(ge=0, le=100)
    detected_patterns: list[str]
    ring_id: Optional[str] = None


class FraudRing(BaseModel):
    """Fraud ring detection result."""
    ring_id: str
    member_accounts: list[str]
    pattern_type: str
    risk_score: float = Field(ge=0, le=100)


class DetectionSummary(BaseModel):
    """Summary statistics of detection results."""
    total_accounts_analyzed: int
    suspicious_accounts_flagged: int
    fraud_rings_detected: int
    processing_time_seconds: float


class DetectionResult(BaseModel):
    """Complete detection result matching output schema."""
    suspicious_accounts: list[SuspiciousAccount]
    fraud_rings: list[FraudRing]
    summary: DetectionSummary
