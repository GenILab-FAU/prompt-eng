Here’s a simplified `README.md`:

```markdown
# Environment Setup Guide

This project uses a Python virtual environment named `PROMPTLABENV`.  
The `setup_env.sh` script will handle everything for you.

### How to Run:

1. Open a terminal in the project directory.

2. Run this command:  
   ```bash
   ./setup_env.sh
   ```

### What It Does:

- Creates the virtual environment if it doesn’t exist.  
- Activates the environment.  
- Installs all dependencies from `requirements.txt` using:  
  ```bash
  python -m pip install --break-system-packages -r requirements.txt
  ```

### Notes:

- Make sure Python version 3.10 > 3.12 is installed.  
- If you get a permission error, run:  
  ```bash
  chmod +x setup_env.sh
  ```