# Running this project

Everything about how the starter works and how to use it.

---

## Before your first class

Setup happens **before class**, not during it. The
[environment setup page](../pages/ide_setup) has the per-operating-system
commands, the exact versions, and where to get your API key.

The short version, from inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py