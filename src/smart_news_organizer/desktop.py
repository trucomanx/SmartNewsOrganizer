import os
import smart_news_organizer.about as about
import subprocess


def update_desktop_database(desktop_path):
    applications_dir = os.path.expanduser(desktop_path)
    try:
        subprocess.run(
            ["update-desktop-database", applications_dir],
            check=True
        )
        print("Shortcut database updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating the database: {e}")
    except FileNotFoundError:
        print("The command 'update-desktop-database' was not found. Verify that the package 'desktop-file-utils' is installed.")

def create_desktop_file(desktop_path, overwrite=False):
    base_dir_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')

    script_path = os.path.expanduser(f"~/.local/bin/{about.__program_name__}")

    desktop_entry = f"""[Desktop Entry]
Name={about.__program_name__}
Comment={about.__description__}
Exec={script_path}
Terminal=false
Type=Application
Icon={icon_path}
StartupNotify=true
Categories=Education;
Keywords=organizer;python;
Encoding=UTF-8
StartupWMClass={about.__package__}
"""
    path = os.path.expanduser(os.path.join(desktop_path,f"{about.__program_name__}.desktop"))
    
    if not os.path.exists(path) or overwrite == True: 
        with open(path, "w") as f:
            f.write(desktop_entry)
        os.chmod(path, 0o755)
        print(f"File {about.__program_name__}.desktop created in {path}")
        update_desktop_database(desktop_path)
    
if __name__ == '__main__':
    create_desktop_file()
