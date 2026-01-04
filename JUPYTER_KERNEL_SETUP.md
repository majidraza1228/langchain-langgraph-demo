# Jupyter Kernel Setup - Fixing Missing Module Errors

## Problem
When starting a Jupyter notebook kernel, you may encounter errors like:
```
The kernel failed to start due to the missing module 'pygments'.
Consider installing this module.
```

## Root Cause
The Jupyter kernel uses a specific Python version that may not have all required packages installed. In this case, the `langchain-demo` kernel uses `/usr/bin/python3` (Python 3.9), but the missing module is only installed in other Python environments.

## Solution - Installing Modules from zsh Command Prompt

### Step 1: Identify Which Python Your Kernel Uses

```zsh
# List all available Jupyter kernels
jupyter kernelspec list

# Check the kernel configuration (replace 'langchain-demo' with your kernel name)
cat ~/Library/Jupyter/kernels/langchain-demo/kernel.json
```

Look for the `argv` field to see which Python executable is being used. For example:
```json
"argv": [
  "/usr/bin/python3",
  "-m",
  "ipykernel_launcher",
  ...
]
```

### Step 2: Verify the Python Version

```zsh
# Check which Python version the kernel uses
/usr/bin/python3 --version
```

### Step 3: Install the Missing Module

Use the **exact Python executable** that your kernel uses:

```zsh
# Install pygments (or any other missing module)
/usr/bin/python3 -m pip install pygments

# For other common modules:
/usr/bin/python3 -m pip install ipykernel
/usr/bin/python3 -m pip install ipython
```

### Step 4: Restart the Kernel

In VSCode or Jupyter:
1. Stop the current kernel
2. Restart the kernel
3. The module should now be available

## Common Scenarios

### Scenario 1: Module Already Installed But Not in Kernel's Python

If you see "Requirement already satisfied" but the kernel still fails:

```zsh
# Check where the module is installed
pip show pygments

# Install it for the specific Python version
/usr/bin/python3 -m pip install pygments
```

### Scenario 2: Multiple Python Versions on System

```zsh
# List all Python installations
which -a python3

# Install for each Python version if needed
python3.9 -m pip install pygments
python3.11 -m pip install pygments
```

### Scenario 3: Permission Issues

If you get permission errors:

```zsh
# Install in user directory (recommended)
/usr/bin/python3 -m pip install --user pygments

# OR use sudo (not recommended for user packages)
sudo /usr/bin/python3 -m pip install pygments
```

## Installing Multiple Modules at Once

```zsh
# Install all required modules for the kernel
/usr/bin/python3 -m pip install pygments ipykernel ipython jupyter
```

## Verifying Installation

```zsh
# Check if the module is installed for the correct Python
/usr/bin/python3 -c "import pygments; print(pygments.__version__)"

# List all installed packages for that Python
/usr/bin/python3 -m pip list
```

## Creating a New Kernel with Correct Dependencies

If you want to create a fresh kernel with all dependencies:

```zsh
# 1. Create a virtual environment (recommended)
python3 -m venv ~/venvs/langchain-env

# 2. Activate the environment
source ~/venvs/langchain-env/bin/activate

# 3. Install required packages
pip install ipykernel pygments langchain langgraph

# 4. Create a Jupyter kernel from this environment
python -m ipykernel install --user --name=langchain-new --display-name="LangChain New"

# 5. Deactivate when done
deactivate
```

Now you can select "LangChain New" as your kernel in Jupyter/VSCode.

## Troubleshooting

### Check Kernel Logs

```zsh
# View Jupyter logs for detailed error messages
jupyter --paths
# Look for logs in the runtime directory
```

### Remove and Reinstall Kernel

```zsh
# Remove the problematic kernel
jupyter kernelspec uninstall langchain-demo

# Reinstall it
/usr/bin/python3 -m ipykernel install --user --name=langchain-demo --display-name="LangChain Demo"
```

### Check PYTHONPATH

If the kernel has a custom `PYTHONPATH` in its config:

```zsh
# View the kernel config
cat ~/Library/Jupyter/kernels/langchain-demo/kernel.json

# Install modules in that specific path if needed
/usr/bin/python3 -m pip install --target=/Users/syedraza/Library/Python/3.9/lib/python/site-packages pygments
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `jupyter kernelspec list` | List all kernels |
| `cat ~/Library/Jupyter/kernels/KERNEL_NAME/kernel.json` | View kernel config |
| `/PATH/TO/python3 -m pip install MODULE` | Install module for specific Python |
| `/PATH/TO/python3 -c "import MODULE"` | Verify module installation |
| `jupyter kernelspec uninstall KERNEL_NAME` | Remove a kernel |

## Setting Up Environment Variables (API Keys)

If you're getting OpenAI API key errors even though you have a `.env` file, it's because Jupyter kernels don't automatically load `.env` files. You have two options:

### Option 1: Add Variables to Kernel Configuration (Recommended)

Edit your kernel's `kernel.json` file to include environment variables:

```zsh
# 1. Find your kernel configuration
jupyter kernelspec list

# 2. Edit the kernel.json file
# For the langchain-demo kernel:
nano ~/Library/Jupyter/kernels/langchain-demo/kernel.json
```

Add your environment variables to the `"env"` section:

```json
{
  "argv": [...],
  "display_name": "LangChain Demo",
  "language": "python",
  "metadata": {
    "debugger": true
  },
  "env": {
    "PYTHONPATH": "/Users/syedraza/Library/Python/3.9/lib/python/site-packages",
    "OPENAI_API_KEY": "your-api-key-here",
    "LANGSMITH_API_KEY": "your-langsmith-key-here",
    "LANGSMITH_TRACING": "true",
    "LANGSMITH_PROJECT": "your-project-name"
  }
}
```

After editing, restart your kernel in VSCode/Jupyter.

### Option 2: Load .env File in Notebook

Make sure you run the `load_dotenv()` cell **before** any cells that use the API:

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify it loaded
print("API Key loaded:", "OPENAI_API_KEY" in os.environ)
```

**Important**: You must run this cell before running any cells that initialize the LLM or make API calls.

### Quick Script to Auto-Update Kernel Config

```zsh
# Navigate to your project directory
cd ~/langchain/langchain-langgraph-demo

# Run this Python script to update kernel config
/usr/bin/python3 << 'EOF'
import json
from dotenv import dotenv_values
from pathlib import Path

# Load .env file
env_vars = dotenv_values('.env')

# Read kernel config
kernel_path = Path.home() / 'Library/Jupyter/kernels/langchain-demo/kernel.json'
with open(kernel_path, 'r') as f:
    config = json.load(f)

# Update env section
if 'env' not in config:
    config['env'] = {}

# Add environment variables (excluding comments)
for key, value in env_vars.items():
    if value and not value.startswith('#'):
        config['env'][key] = value

# Write back
with open(kernel_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Kernel configuration updated with environment variables")
EOF
```

## Additional Resources

- [Jupyter Kernels Documentation](https://jupyter.readthedocs.io/en/latest/projects/kernels.html)
- [IPython Kernel Installation](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
- [Managing Python Environments](https://docs.python.org/3/tutorial/venv.html)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
