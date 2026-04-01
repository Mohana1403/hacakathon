from typing import Dict, Tuple, Any
from .models import Observation, Action, Reward
from .tasks import Task, EasyTask, MediumTask, HardTask

class EmailTriageEnv:
    def __init__(self, task: str = "easy"):
        self.tasks = {
            "easy": EasyTask(),
            "medium": MediumTask(),
            "hard": HardTask()
        }
        self.current_task: Task = self.tasks[task]
        self.current_index = 0
        self.classifications: Dict[int, str] = {}
        self.priorities: Dict[int, int] = {}
        self.done = False

    def reset(self) -> Observation:
        self.current_index = 0
        self.classifications = {}
        self.priorities = {}
        self.done = False
        return self._get_observation()

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        reward_value = 0.0
        reason = ""
        
        if self.done:
            return self._get_observation(), Reward(value=0.0, reason="Episode already done"), True, {}
        
        current_email = self.current_task.emails[self.current_index]
        
        if action.action_type == "classify":
            if action.category:
                self.classifications[current_email.id] = action.category
                if action.category == current_email.category:
                    reward_value += 1.0
                    reason = "Correct classification"
                else:
                    reward_value -= 1.0
                    reason = "Incorrect classification"
            else:
                reward_value -= 0.5
                reason = "Invalid classification action"
        
        elif action.action_type == "prioritize" and self.current_task.name == "hard":
            if action.priority is not None and current_email.priority is not None:
                self.priorities[current_email.id] = action.priority
                # Reward based on how close to correct priority
                correct_priority = current_email.priority
                diff = abs(action.priority - correct_priority)
                reward_value += max(0, 1.0 - diff / 20.0)  # Assuming priorities 1-20
                reason = f"Priority set, closeness: {1.0 - diff / 20.0}"
            else:
                reward_value -= 0.5
                reason = "Invalid prioritize action"
        
        elif action.action_type == "next":
            self.current_index += 1
            if self.current_index >= len(self.current_task.emails):
                self.done = True
                # Final reward based on overall performance
                score = self.current_task.grade(self.classifications, self.priorities)
                reward_value += score * 10  # Bonus for completion
                reason = f"Task completed with score {score}"
            else:
                reward_value += 0.1  # Small reward for progressing
                reason = "Moved to next email"
        else:
            reward_value -= 0.5
            reason = "Invalid action type"
        
        obs = self._get_observation()
        reward = Reward(value=reward_value, reason=reason)
        info = {"current_index": self.current_index, "total_emails": len(self.current_task.emails)}
        
        return obs, reward, self.done, info

    def state(self) -> Dict[str, Any]:
        return {
            "task": self.current_task.name,
            "current_index": self.current_index,
            "classifications": self.classifications,
            "priorities": self.priorities,
            "done": self.done
        }

    def _get_observation(self) -> Observation:
        if self.current_index < len(self.current_task.emails):
            current_email = self.current_task.emails[self.current_index]
        else:
            current_email = None
        return Observation(
            current_email=current_email,
            emails_processed=self.current_index,
            total_emails=len(self.current_task.emails),
            task_description=self.current_task.description
        )