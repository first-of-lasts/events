import subprocess
import os


PROJECT_DIR = os.path.abspath('events/')
OUTPUT_FILE = os.path.abspath('locale/strings.pot')


def find_gettext_strings():
    """
    Finds all gettext strings in the project files and generates a strings.pot file.
    """
    try:
        # Print paths for debugging
        print(f"Project Directory: {PROJECT_DIR}")
        print(f"Output File: {OUTPUT_FILE}")

        # Check if directory exists and is readable
        if not os.path.exists(PROJECT_DIR):
            print(f"Error: Directory {PROJECT_DIR} does not exist")
            return

        if not os.access(PROJECT_DIR, os.R_OK):
            print(f"Error: No read permissions for {PROJECT_DIR}")
            return

        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        python_files = []
        for root, dirs, files in os.walk(PROJECT_DIR):
            python_files.extend(
                [os.path.join(root, f) for f in files if f.endswith('.py')]
            )
        subprocess.run(
            [
                'xgettext', '--language=python', '--keyword=_',
                '--output=' + OUTPUT_FILE,
                '--add-comments=TRANSLATORS', '--from-code=UTF-8'
            ] + python_files, check=True
        )
        print(f"Generated strings.pot at {OUTPUT_FILE}")

    except subprocess.CalledProcessError as e:
        print(f"Error generating strings.pot: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    find_gettext_strings()
