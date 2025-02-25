#!/usr/bin/env python3
"""
Installation script for Mode_0 Twitch Bot.
"""
import os
import sys
import subprocess
import platform
import getpass

def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("Error: Python 3.11 or higher is required")
        sys.exit(1)
    print(f"Python version OK: {sys.version}")

def setup_venv():
    """Set up virtual environment"""
    print("Setting up virtual environment...")
    
    # Check if venv exists
    if os.path.exists("venv"):
        response = input("Virtual environment already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Using existing virtual environment")
            return
        
        # Remove existing venv
        if platform.system() == "Windows":
            os.system("rmdir /s /q venv")
        else:
            os.system("rm -rf venv")
    
    # Create new venv
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created")

def install_dependencies():
    """Install required packages"""
    print("Installing Python dependencies...")
    
    # Get path to pip in virtual environment
    if platform.system() == "Windows":
        python_path = os.path.join("venv", "Scripts", "python")
    else:
        python_path = os.path.join("venv", "bin", "python")
    
    # Upgrade pip properly
    subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install from requirements.txt
    subprocess.check_call([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("Dependencies installed successfully")

def setup_config():
    """Set up configuration file"""
    config_path = "mode_0/config/config.json"
    template_path = "mode_0/config/config.template.json"
    
    # Check if config already exists
    if os.path.exists(config_path):
        response = input("Configuration file already exists. Recreate? (y/n): ")
        if response.lower() != 'y':
            print("Using existing configuration")
            return
    
    # Copy template to config
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    
    # Get Twitch OAuth token
    print("\nTwitch OAuth Token")
    print("You can get a token from https://twitchtokengenerator.com/")
    oauth_token = getpass.getpass("Enter Twitch OAuth token: ")
    template = template.replace("YOUR_OAUTH_TOKEN", oauth_token)
    
    # Get channel name
    channel = input("Enter channel name (without @): ")
    template = template.replace("YOUR_CHANNEL_NAME", channel)
    
    # Get StreamElements JWT
    print("\nStreamElements JWT Token")
    print("You can get this from StreamElements dashboard > Bot > Show Secrets")
    se_jwt = getpass.getpass("Enter StreamElements JWT: ")
    template = template.replace("YOUR_STREAMELEMENTS_JWT", se_jwt)
    
    # Get StreamElements channel ID
    print("\nStreamElements Channel ID")
    print("This is found in the URL when you're on the StreamElements dashboard")
    se_channel_id = input("Enter StreamElements channel ID: ")
    template = template.replace("YOUR_STREAMELEMENTS_CHANNEL_ID", se_channel_id)
    
    # Get admin user ID
    admin_id = input("Enter your Twitch user ID for admin access: ")
    template = template.replace("YOUR_USER_ID", admin_id)
    
    # Write config file
    with open(config_path, 'w') as config_file:
        config_file.write(template)
    
    print(f"Configuration saved to {config_path}")

def setup_service():
    """Set up system service for bot"""
    if platform.system() == "Windows":
        setup_windows_service()
    else:
        setup_linux_service()

def setup_windows_service():
    """Set up Windows service"""
    print("Setting up Windows service...")
    
    # Create batch file
    with open("run_bot.bat", "w") as f:
        f.write(f"@echo off\n")
        f.write(f"cd {os.getcwd()}\n")
        f.write(f"venv\\Scripts\\python -m mode_0\n")
    
    print("\nTo set up as a service:")
    print("1. Open Task Scheduler")
    print("2. Create a new task")
    print("3. Set it to run at system startup")
    print("4. Add an action to start program: " + os.path.join(os.getcwd(), "run_bot.bat"))
    
    response = input("\nWould you like to try to set up the service automatically? (y/n): ")
    if response.lower() == 'y':
        try:
            # Use schtasks to create a scheduled task
            task_name = "Mode0Bot"
            batch_path = os.path.join(os.getcwd(), "run_bot.bat")
            
            cmd = f'schtasks /create /tn "{task_name}" /tr "{batch_path}" /sc onstart /ru System'
            subprocess.check_call(cmd, shell=True)
            
            print(f"Windows task '{task_name}' created successfully")
        except subprocess.CalledProcessError:
            print("Error creating Windows task. Please set up manually using the instructions above.")

def setup_linux_service():
    """Set up Linux systemd service"""
    print("Setting up Linux systemd service...")
    
    # Create service file
    service_content = f"""[Unit]
Description=Mode_0 Twitch Bot
After=network.target

[Service]
Type=simple
User={os.getlogin()}
WorkingDirectory={os.getcwd()}
ExecStart={os.getcwd()}/venv/bin/python -m mode_0
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
"""
    
    service_path = os.path.join(os.getcwd(), "mode_0.service")
    with open(service_path, "w") as f:
        f.write(service_content)
    
    print(f"Service file created at {service_path}")
    print("\nTo install the service:")
    print(f"sudo cp {service_path} /etc/systemd/system/")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable mode_0.service")
    print("sudo systemctl start mode_0.service")
    
    response = input("\nWould you like to try to install the service now? (requires sudo) (y/n): ")
    if response.lower() == 'y':
        try:
            subprocess.check_call(["sudo", "cp", service_path, "/etc/systemd/system/"])
            subprocess.check_call(["sudo", "systemctl", "daemon-reload"])
            subprocess.check_call(["sudo", "systemctl", "enable", "mode_0.service"])
            subprocess.check_call(["sudo", "systemctl", "start", "mode_0.service"])
            print("Service installed and started successfully")
        except subprocess.CalledProcessError:
            print("Error installing service. Please install manually using the instructions above.")
        except FileNotFoundError:
            print("Error: sudo command not found. Please install manually using the instructions above.")

def create_data_dirs():
    """Create necessary data directories"""
    dirs = ["data", "logs"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("Data directories created")

def main():
    """Main installation function"""
    print("Mode_0 Twitch Bot - Installation")
    print("===============================")
    
    # Check Python version
    check_python_version()
    
    # Setup venv
    setup_venv()
    
    # Install dependencies
    install_dependencies()
    
    # Create data directories
    create_data_dirs()
    
    # Setup configuration
    setup_config()
    
    # Setup service
    response = input("Would you like to set up the bot as a system service? (y/n): ")
    if response.lower() == 'y':
        setup_service()
    
    print("\nInstallation complete!")
    print("You can now run the bot with:")
    if platform.system() == "Windows":
        print("venv\\Scripts\\python -m mode_0")
    else:
        print("venv/bin/python -m mode_0")

if __name__ == "__main__":
    main()
