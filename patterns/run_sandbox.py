import argparse
import subprocess
import os
import sys

def run_in_sandbox(script_path, language="python"):
    """
    Executes a script inside a secure Docker container.
    """
    abs_path = os.path.abspath(script_path)
    file_name = os.path.basename(abs_path)
    dir_name = os.path.dirname(abs_path)
    
    print(f"--- Sentinel Sandbox ---")
    print(f"Execution Target: {file_name}")
    print(f"Hardening Level: High (Isolated Container)")
    
    docker_command = [
        "docker", "run", "--rm",
        "-v", f"{dir_name}:/sandbox:ro",
        "-w", "/sandbox",
        "sentinel-sandbox:v2",
    ]
    
    if language == "python":
        docker_command.extend(["python3", file_name])
    elif language == "bash":
        docker_command.extend(["bash", file_name])
    else:
        print(f"Error: Language {language} not supported.")
        return False

    try:
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
        print("\n--- Output ---")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("\n--- Sandbox Execution Failed ---")
        print(f"Exit Code: {e.returncode}")
        print(f"Error Log: {e.stderr}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentinel Secure Sandbox Execution")
    parser.add_argument("script", help="Path to the script to execute")
    parser.add_argument("--lang", default="python", choices=["python", "bash"], help="Script language")
    args = parser.parse_args()
    
    success = run_in_sandbox(args.script, args.lang)
    sys.exit(0 if success else 1)
