#!/usr/bin/env python3
"""
OpenEnv server entry point for Email Triage Environment
"""

import uvicorn
from api import app

def main():
    """Run the FastAPI server"""
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()