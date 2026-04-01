# Email Triage Environment

A real-world task simulation for email triage using the OpenEnv framework.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running the Environment

```python
from email_triage_env import EmailTriageEnv, Action

env = EmailTriageEnv(task="easy")
obs = env.reset()

action = Action(action_type="classify", category="important")
obs, reward, done, info = env.step(action)
```

### Tasks

- **Easy**: Classify 5 emails into "important" or "not_important"
- **Medium**: Classify 10 emails into "important", "urgent", or "spam"
- **Hard**: Prioritize and classify 20 emails

### Validation

To validate the environment:

```bash
openenv validate
```

### Baseline

Set your OpenAI API key:

**Unix/Linux/macOS:**

```bash
export OPENAI_API_KEY=your_key_here
```

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY = "your_key_here"
```

Run the baseline:

```bash
python baseline.py
```

This will run GPT-3.5-turbo on all tasks and print the scores.