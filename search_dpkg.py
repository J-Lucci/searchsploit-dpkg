import subprocess
import sys
from pprint import pprint

def parse_dpkg_output(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    # Extract package names, skipping headers and strip whitespace
    packages = [line.split()[1].strip() for line in lines[5:]]
    return packages

def search_exploits(package):
    try:
        output = subprocess.check_output(['searchsploit', package]).decode('utf-8')
        # Only print if actual results are found
        if "Exploits: No Results" not in output or "Shellcodes: No Results" not in output:
            print(f"Results for {package}:")
            print(output)
            print("-" * 50)  # Separator line for better readability
    except subprocess.CalledProcessError:
        pass

def display_progress_bar(iteration, total, bar_length=50):
    progress = (iteration / total)
    arrow = '-' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\rProgress: [{arrow + spaces}] {int(progress * 100)}%')
    sys.stdout.flush()

def main(dpkg_file):
    # List of common terms to skip
    blacklist = [
        "file", "hostname", "sed", "bash", "ls", "cat", "more", "less",
        "grep", "awk", "find", "dir", "echo", "nano", "vim", "vi"
    ]

    installed_packages = parse_dpkg_output(dpkg_file)
    # Filter out blacklisted terms
    installed_packages = [pkg for pkg in installed_packages if pkg.lower() not in blacklist]

    total_packages = len(installed_packages)
    for idx, pkg in enumerate(installed_packages, 1):
        search_exploits(pkg)
        display_progress_bar(idx, total_packages)
    print("\nDone!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <dpkg_output_file>")
        sys.exit(1)

    dpkg_file = sys.argv[1]
    main(dpkg_file)
