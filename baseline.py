import os
from openai import OpenAI
from email_triage_env import EmailTriageEnv, Action

def run_baseline(task_name: str, model: str = "gpt-3.5-turbo") -> float:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it before running the baseline.")
    client = OpenAI(api_key=api_key)
    env = EmailTriageEnv(task=task_name)
    obs = env.reset()
    
    total_reward = 0.0
    steps = 0
    
    while not env.state()["done"]:
        # Create prompt for the model
        prompt = f"Task: {obs.task_description}\n"
        if obs.current_email:
            prompt += f"Current Email:\nSubject: {obs.current_email.subject}\nBody: {obs.current_email.body}\nSender: {obs.current_email.sender}\n"
        prompt += f"Emails processed: {obs.emails_processed}/{obs.total_emails}\n"
        prompt += "Available actions: classify (with category), prioritize (with priority number), next\n"
        if task_name == "easy":
            prompt += "Categories: important, not_important\n"
        elif task_name == "medium":
            prompt += "Categories: important, urgent, spam\n"
        else:  # hard
            prompt += "Categories: important, urgent, spam, not_important\nPriorities: 1-20 (1 highest priority)\n"
        prompt += "Respond with action in format: action_type:category or action_type:priority or next"
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        if content is None:
            action_text = "next"
        else:
            action_text = content.strip()
        
        # Parse action
        if ":" in action_text:
            action_type, param = action_text.split(":", 1)
            if action_type == "classify":
                action = Action(action_type="classify", category=param.strip())
            elif action_type == "prioritize":
                try:
                    priority = int(param.strip())
                    action = Action(action_type="prioritize", priority=priority)
                except ValueError:
                    action = Action(action_type="next")
            else:
                action = Action(action_type="next")
        else:
            action = Action(action_type="next")
        
        obs, reward, done, info = env.step(action)
        total_reward += reward.value
        steps += 1
        
        if steps > 100:  # Safety limit
            break
    
    # Final score
    final_score = env.current_task.grade(env.state()["classifications"], env.state()["priorities"])
    return final_score

if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]
    model = "gpt-3.5-turbo"  # or gpt-4
    
    print("Running baseline with", model)
    for task in tasks:
        score = run_baseline(task, model)
        print(f"{task.capitalize()} task score: {score:.2f}")