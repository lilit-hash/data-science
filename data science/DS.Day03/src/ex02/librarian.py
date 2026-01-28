#!/usr/bin/env python3
import os
import subprocess
import sys

def check_virtual_env():
    env_path = os.environ.get('VIRTUAL_ENV')
    if not env_path or 'hunnimod' not in env_path:
        raise Exception("Activate the hunnimod virtual environment first")

def main():
    try:
        check_virtual_env()
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, check=True)
        print("Installation completed successfully!")
        print("\nAll installed libraries:")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'freeze'
        ], capture_output=True, text=True, check=True)
        
        print(result.stdout)
        with open('requirements.txt', 'w') as f:
            f.write(result.stdout)
        print("Requirements saved to requirements.txt")
    except subprocess.CalledProcessError as e:
        print(f"Installation error: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
