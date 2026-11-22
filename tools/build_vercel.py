#!/usr/bin/env python3
"""Generate and validate static HTML for a Vercel domain root."""
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
origin = os.environ.get('SITE_ORIGIN')
if not origin:
    domain = os.environ.get('VERCEL_PROJECT_PRODUCTION_URL') or os.environ.get('VERCEL_URL')
    if not domain:
        raise SystemExit('Set SITE_ORIGIN (https://your-domain) for local builds, or enable Vercel system environment variables.')
    origin = 'https://' + domain
origin = origin.rstrip('/')
parsed = urlsplit(origin)
if parsed.scheme != 'https' or not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
    raise SystemExit('SITE_ORIGIN must be an HTTPS origin without a path, query or fragment.')
options = ['--base', '', '--origin', origin]
subprocess.run([sys.executable, 'tools/build.py', *options, '--hosting', 'vercel'], cwd=ROOT, check=True)
subprocess.run([sys.executable, 'tools/check.py', *options], cwd=ROOT, check=True)
