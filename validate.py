#!/usr/bin/env python3
"""
OpenEnv validation script
"""

from email_triage_env import EmailTriageEnv, Action, Observation, Reward

def validate_env():
    # Test each task
    tasks = ["easy", "medium", "hard"]
    
    for task in tasks:
        print(f"Validating {task} task...")
        env = EmailTriageEnv(task=task)
        
        # Test reset
        obs = env.reset()
        assert isinstance(obs, Observation)
        assert obs.emails_processed == 0
        assert obs.total_emails == len(env.current_task.emails)
        
        # Test state
        state = env.state()
        assert "task" in state
        assert "current_index" in state
        assert "done" in state
        
        # Test step
        action = Action(action_type="next")
        obs, reward, done, info = env.step(action)
        assert isinstance(obs, Observation)
        assert isinstance(reward, Reward)
        assert isinstance(done, bool)
        assert isinstance(info, dict)
        
        print(f"{task} task validation passed.")
    
    print("All validations passed!")

if __name__ == "__main__":
    validate_env()