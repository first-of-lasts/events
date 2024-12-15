import os
import sys
import subprocess


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def generate_translations():
    try:
        generate_script = os.path.join(
            "setup", "translations", "generate_gettext.py"
        )
        result = subprocess.run(
            [sys.executable, generate_script], capture_output=True, text=True
        )
        print("Translation generation output:")
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
    except Exception as e:
        print(f"Error generating translations: {e}")


def compile_translations():
    try:
        compile_script = os.path.join(
            "setup", "translations", "compile_translations.py"
        )
        result = subprocess.run(
            [sys.executable, compile_script], capture_output=True, text=True
        )
        print("Translation compilation output:")
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
    except Exception as e:
        print(f"Error compiling translations: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [generate_translations|compile_translations]")
        sys.exit(1)

    command = sys.argv[1]
    commands = {
        "generate_translations": generate_translations,
        "compile_translations": compile_translations,
    }
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        for cmd in commands:
            print(f"  - {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
