# Upload to Hugging Face Spaces Using Git Commands

## Prerequisites

1. Create a Hugging Face account at <https://huggingface.co/join>
2. Get your Hugging Face API token:
   - Go to <https://huggingface.co/settings/tokens>
   - Create a **write-access** token
   - Copy the token (you'll need it)

## Step 1: Install Git LFS (Optional but Recommended)

```bash
# For Windows, install from https://git-lfs.com or use:
choco install git-lfs
# or
winget install GitHub.GitLFS
```

## Step 2: Create Hugging Face Space

Create an empty Space repository at <https://huggingface.co/spaces/new>:
- **Owner**: Your username
- **Space name**: `email-triage-rl-demo`
- **License**: `MIT`
- **Space SDK**: `Streamlit`
- **Visibility**: `Public`
- **Initialize with README**: `No`

Copy the Space URL (you'll see it after creation).

## Step 3: Add Hugging Face Remote and Push

Run these commands:

```bash
# Navigate to your project
cd c:\Users\DELL\Downloads\hackathon

# Add Hugging Face as a remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/email-triage-rl-demo.git

# Rename files for Streamlit
Copy-Item demo.py streamlit_app.py
Copy-Item requirements-hf.txt requirements.txt

# Add and commit the renamed files
git add streamlit_app.py requirements.txt
git commit -m "Add Streamlit app and requirements for HF Spaces"

# Push to Hugging Face
git push huggingface main
```

Replace `YOUR_USERNAME` with your actual Hugging Face username.

## Step 4: Verify Deployment

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/email-triage-rl-demo`
2. Check the **Logs** tab to see deployment status
3. Wait for the app to build and start (usually 2-3 minutes)
4. Your Space will be live!

## File Structure Expected in HF Spaces

```
email-triage-rl-demo/
├── streamlit_app.py
├── requirements.txt
└── email_triage_env/
    ├── __init__.py
    ├── environment.py
    ├── models.py
    └── tasks.py
```

## Troubleshooting

### If push fails with "not found"

Make sure the Space URL is correct:
```bash
git remote -v
# Should show your huggingface remote
```

### If app doesn't start

Check the logs in your Space UI and verify:
- `streamlit_app.py` exists (not `demo.py`)
- `requirements.txt` exists (not `requirements-hf.txt`)
- `email_triage_env/` folder has all 4 files

### Update after changes

If you make changes locally and want to update HF Spaces:

```bash
git add .
git commit -m "Update description here"
git push huggingface main
```

## Advanced: Use HF CLI (Alternative Method)

```bash
# Install huggingface_hub
pip install huggingface_hub

# Login
huggingface-cli login

# Upload specific files
huggingface-cli upload YOUR_USERNAME/email-triage-rl-demo streamlit_app.py --repo-type=space
huggingface-cli upload YOUR_USERNAME/email-triage-rl-demo requirements.txt --repo-type=space
huggingface-cli upload YOUR_USERNAME/email-triage-rl-demo email_triage_env --repo-type=space
```

## Next Steps

After deployment:
- Visit your Space URL
- Test the interactive demo
- Share the link with others!
- Monitor the Logs for any issues
