# Hugging Face Spaces Deployment Guide

## Quick Deploy (No Local Setup Needed!)

### Option 1: Upload Files Directly (Easiest)

1. Go to https://huggingface.co/spaces and click **Create new Space**
2. Fill in details:
   - **Space name**: `email-triage-rl-demo`
   - **License**: `MIT`
   - **SDK**: `Streamlit`
   - **Visibility**: `Public`
3. Click **Create Space**

4. In the Space, upload these files with this exact structure:

```
your-space-name/
├── streamlit_app.py  ← Rename demo.py to this
├── requirements.txt  ← Use requirements-hf.txt (rename it)
└── email_triage_env/
    ├── __init__.py
    ├── environment.py
    ├── models.py
    ├── tasks.py
```

### Option 2: GitHub Sync (Automatic)

1. In Hugging Face Space settings, enable **GitHub Sync**
2. Connect to your repository: `https://github.com/Mohana1403/hacakathon.git`
3. Add a `streamlit_app.py` file at the root (rename from demo.py)
4. Rename `requirements-hf.txt` to `requirements.txt`
5. The Space will auto-sync and deploy!

## File Renaming

- `demo.py` → `streamlit_app.py`
- `requirements-hf.txt` → `requirements.txt`

## Testing Locally (Optional)

Don't worry about the disk space issue locally. Your code is ready for Hugging Face!

When you upload to Hugging Face Spaces, it will:
- Create a clean virtual environment
- Install dependencies automatically
- Run your Streamlit app
- Make it publicly accessible (no setup fees!)

## What Happens After Upload

1. HF Spaces detects `streamlit_app.py`
2. Installs packages from `requirements.txt`
3. Automatically runs `streamlit run streamlit_app.py`
4. App is live at `https://huggingface.co/spaces/YourUsername/email-triage-rl-demo`

**That's it! No more configuration needed.**

## Troubleshooting in HF Spaces

If there are issues:
1. Check the **App logs** tab in your Space
2. Make sure file structure matches above
3. Verify `requirements.txt` has the right packages

## Your Current Files Are Ready!

✅ `email_triage_env/` - Complete package
✅ `demo.py` - Streamlit app (just rename it)
✅ `requirements-hf.txt` - Dependencies (just rename it)
✅ `.gitignore` - Clean repository
✅ `mypy.ini` - Type checking config
