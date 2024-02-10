import platform
import subprocess

# Get the current operating system
current_os = platform.system()

# Define requirements file paths for different operating systems
requirements_files = {
    'Windows': 'requirements/windows.txt',
    'Linux': 'requirements/linux.txt',
    'Darwin': 'requirements/macos.txt'  # macOS
}

# Check if the current OS is in the requirements_files dictionary
if current_os in requirements_files:
    requirements_file = requirements_files[current_os]
else:
    # Default to a generic requirements file if OS is not recognized
    requirements_file = 'requirements.txt'

# Install requirements using pip
subprocess.call(['pip', 'install', '-r', requirements_file])