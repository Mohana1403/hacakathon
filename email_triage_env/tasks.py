from typing import List, Dict, Optional
from .models import Email

class Task:
    def __init__(self, name: str, description: str, emails: List[Email], objective: str):
        self.name = name
        self.description = description
        self.emails = emails
        self.objective = objective

    def grade(self, classifications: Dict[int, str], priorities: Optional[Dict[int, int]] = None) -> float:
        """Return score between 0.0 and 1.0"""
        raise NotImplementedError

class EasyTask(Task):
    def __init__(self):
        emails = [
            Email(id=1, subject="Meeting tomorrow", body="Don't forget our meeting at 10am.", sender="boss@company.com", category="important"),
            Email(id=2, subject="Newsletter", body="Check out our latest products.", sender="newsletter@store.com", category="not_important"),
            Email(id=3, subject="Urgent: Server down", body="The main server is down!", sender="admin@company.com", category="important"),
            Email(id=4, subject="Social event", body="Join us for the company picnic.", sender="hr@company.com", category="not_important"),
            Email(id=5, subject="Project update", body="Here's the latest on project X.", sender="colleague@company.com", category="important"),
        ]
        super().__init__("easy", "Classify 5 emails into important or not_important", emails, "Classify all emails correctly")

    def grade(self, classifications: Dict[int, str], priorities: Optional[Dict[int, int]] = None) -> float:
        correct = 0
        for email in self.emails:
            if classifications.get(email.id) == email.category:
                correct += 1
        return correct / len(self.emails)

class MediumTask(Task):
    def __init__(self):
        emails = [
            Email(id=1, subject="Meeting tomorrow", body="Don't forget our meeting at 10am.", sender="boss@company.com", category="important"),
            Email(id=2, subject="Newsletter", body="Check out our latest products.", sender="newsletter@store.com", category="spam"),
            Email(id=3, subject="Urgent: Server down", body="The main server is down!", sender="admin@company.com", category="urgent"),
            Email(id=4, subject="Social event", body="Join us for the company picnic.", sender="hr@company.com", category="important"),
            Email(id=5, subject="Project update", body="Here's the latest on project X.", sender="colleague@company.com", category="important"),
            Email(id=6, subject="Ad spam", body="Buy now!", sender="spam@ads.com", category="spam"),
            Email(id=7, subject="Deadline approaching", body="Project deadline is tomorrow.", sender="manager@company.com", category="urgent"),
            Email(id=8, subject="Team lunch", body="Let's have lunch together.", sender="team@company.com", category="important"),
            Email(id=9, subject="Promotion", body="Congratulations on your promotion!", sender="hr@company.com", category="important"),
            Email(id=10, subject="Junk mail", body="Win a prize!", sender="junk@spam.com", category="spam"),
        ]
        super().__init__("medium", "Classify 10 emails into important, urgent, or spam", emails, "Classify all emails correctly")

    def grade(self, classifications: Dict[int, str], priorities: Optional[Dict[int, int]] = None) -> float:
        correct = 0
        for email in self.emails:
            if classifications.get(email.id) == email.category:
                correct += 1
        return correct / len(self.emails)

class HardTask(Task):
    def __init__(self):
        emails = [
            # 20 emails with categories and priorities
            Email(id=1, subject="Meeting tomorrow", body="Don't forget our meeting at 10am.", sender="boss@company.com", category="important", priority=1),
            Email(id=2, subject="Urgent: Server down", body="The main server is down!", sender="admin@company.com", category="urgent", priority=2),
            Email(id=3, subject="Deadline approaching", body="Project deadline is tomorrow.", sender="manager@company.com", category="urgent", priority=3),
            Email(id=4, subject="Project update", body="Here's the latest on project X.", sender="colleague@company.com", category="important", priority=4),
            Email(id=5, subject="Team lunch", body="Let's have lunch together.", sender="team@company.com", category="important", priority=5),
            Email(id=6, subject="Promotion", body="Congratulations on your promotion!", sender="hr@company.com", category="important", priority=6),
            Email(id=7, subject="Social event", body="Join us for the company picnic.", sender="hr@company.com", category="not_important", priority=7),
            Email(id=8, subject="Newsletter", body="Check out our latest products.", sender="newsletter@store.com", category="spam", priority=8),
            Email(id=9, subject="Ad spam", body="Buy now!", sender="spam@ads.com", category="spam", priority=9),
            Email(id=10, subject="Junk mail", body="Win a prize!", sender="junk@spam.com", category="spam", priority=10),
            # Add more emails similarly
            Email(id=11, subject="Client call", body="Schedule a call with client.", sender="sales@company.com", category="important", priority=11),
            Email(id=12, subject="System alert", body="Disk space low.", sender="alerts@company.com", category="urgent", priority=12),
            Email(id=13, subject="Weekly report", body="Submit your weekly report.", sender="manager@company.com", category="important", priority=13),
            Email(id=14, subject="Office party", body="RSVP for the party.", sender="events@company.com", category="not_important", priority=14),
            Email(id=15, subject="Security update", body="Update your password.", sender="security@company.com", category="urgent", priority=15),
            Email(id=16, subject="Colleague intro", body="Meet our new team member.", sender="hr@company.com", category="important", priority=16),
            Email(id=17, subject="Marketing email", body="New campaign launch.", sender="marketing@company.com", category="not_important", priority=17),
            Email(id=18, subject="Bug report", body="Found a critical bug.", sender="dev@company.com", category="urgent", priority=18),
            Email(id=19, subject="Invoice", body="Your invoice is attached.", sender="billing@company.com", category="important", priority=19),
            Email(id=20, subject="Spam offer", body="Exclusive deal!", sender="offers@spam.com", category="spam", priority=20),
        ]
        super().__init__("hard", "Prioritize and classify 20 emails", emails, "Correctly prioritize (order by priority) and classify all emails")

    def grade(self, classifications: Dict[int, str], priorities: Optional[Dict[int, int]] = None) -> float:
        if priorities is None:
            priorities = {}
        # Score classification accuracy
        class_correct = sum(1 for email in self.emails if classifications.get(email.id) == email.category)
        class_score = class_correct / len(self.emails)
        
        # Score priority ordering: check if the order matches the priority numbers
        sorted_by_priority = sorted(self.emails, key=lambda e: e.priority or 999)
        priority_order = [e.id for e in sorted_by_priority]
        agent_order = sorted(priorities.keys(), key=lambda id: priorities[id])
        if priority_order == agent_order:
            priority_score = 1.0
        else:
            # Partial score based on correct positions
            correct_positions = sum(1 for i, id in enumerate(agent_order) if id == priority_order[i])
            priority_score = correct_positions / len(self.emails)
        
        return (class_score + priority_score) / 2