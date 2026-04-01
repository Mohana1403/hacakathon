from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Email(BaseModel):
    id: int
    subject: str
    body: str
    sender: str
    category: Optional[str] = None  # For ground truth
    priority: Optional[int] = None  # For hard task

class Observation(BaseModel):
    current_email: Optional[Email] = None
    emails_processed: int
    total_emails: int
    task_description: str

class Action(BaseModel):
    action_type: str  # 'classify', 'prioritize', 'next'
    category: Optional[str] = None  # for classify
    priority: Optional[int] = None  # for prioritize

class Reward(BaseModel):
    value: float
    reason: str