#!/usr/bin/env python3
"""
Backup script for Mode_0 Twitch Bot.
Creates a backup of the database and configuration files.
"""
import os
import sys
import shutil
import datetime
import argparse
import zipfile

def create_backup(output_dir=None, include_logs=False):
    """Create a backup of the bot data"""
    # Get timestamp for backup name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set default output directory if not specified
    if not output_dir:
        output_dir = "backups"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up backup filename
    backup_file = os.path.join(output_dir, f"mode_0_backup_{timestamp}.zip")
    
    # Files and directories to backup
    backup_items = [
        "mode_0/config/config.json",
        "mode_0/config/persona_config.json",
        "mode_0/config/responses.json",
        "data"
    ]
    
    # Add logs if requested
    if include_logs:
        backup_items.append("logs")
    
    # Create zip archive
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in backup_items:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zipf.write(item)
                    print(f"Added file: {item}")
                else:
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Added file: {file_path}")
    
    print(f"\nBackup created: {backup_file}")
    return backup_file

def restore_backup(backup_file, force=False):
    """Restore from a backup file"""
    if not os.path.exists(backup_file):
        print(f"Error: Backup file {backup_file} not found")
        return False
    
    # Check if current data exists and confirm overwrite
    if not force and (os.path.exists("data") or os.path.exists("mode_0/config/config.json")):
        response = input("Warning: This will overwrite existing data. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Restoration cancelled")
            return False
    
    # Create temporary extraction directory
    temp_dir = "temp_restore"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Extract backup
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Restore config files
        config_files = [
            "mode_0/config/config.json",
            "mode_0/config/persona_config.json",
            "mode_0/config/responses.json"
        ]
        
        for config_file in config_files:
            temp_config = os.path.join(temp_dir, config_file)
            if os.path.exists(temp_config):
                # Ensure directory exists
                os.makedirs(os.path.dirname(config_file), exist_ok=True)
                # Copy file
                shutil.copy2(temp_config, config_file)
                print(f"Restored: {config_file}")
        
        # Restore data directory
        temp_data = os.path.join(temp_dir, "data")
        if os.path.exists(temp_data):
            if os.path.exists("data"):
                shutil.rmtree("data")
            shutil.copytree(temp_data, "data")
            print("Restored: data directory")
        
        # Restore logs if they exist in backup
        temp_logs = os.path.join(temp_dir, "logs")
        if os.path.exists(temp_logs):
            if os.path.exists("logs"):
                shutil.rmtree("logs")
            shutil.copytree(temp_logs, "logs")
            print("Restored: logs directory")
        
        print("\nRestore completed successfully")
        return True
    
    except Exception as e:
        print(f"Error during restore: {e}")
        return False
    
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Backup and restore Mode_0 bot data")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup")
    backup_parser.add_argument("-o", "--output", help="Output directory for backup")
    backup_parser.add_argument("-l", "--logs", action="store_true", help="Include logs in backup")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from a backup")
    restore_parser.add_argument("file", help="Backup file to restore from")
    restore_parser.add_argument("-f", "--force", action="store_true", help="Force restore without confirmation")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument("-d", "--directory", default="backups", help="Directory containing backups")
    
    args = parser.parse_args()
    
    if args.command == "backup":
        create_backup(args.output, args.logs)
    
    elif args.command == "restore":
        restore_backup(args.file, args.force)
    
    elif args.command == "list":
        if not os.path.exists(args.directory):
            print(f"Backup directory {args.directory} not found")
            return
        
        backups = [f for f in os.listdir(args.directory) if f.startswith("mode_0_backup_") and f.endswith(".zip")]
        
        if not backups:
            print(f"No backups found in {args.directory}")
            return
        
        print(f"Available backups in {args.directory}:")
        for backup in sorted(backups):
            backup_path = os.path.join(args.directory, backup)
            size = os.path.getsize(backup_path) / (1024 * 1024)  # Convert to MB
            print(f"  {backup} ({size:.2f} MB)")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
