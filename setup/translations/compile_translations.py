import os
import subprocess
import polib


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
SUPPORTED_LANGUAGES = ['en', 'ru', 'uz']
LOCALE_DIR = os.path.join(PROJECT_ROOT, "locale")
TRANSLATION_POT_FILE = os.path.join(LOCALE_DIR, "strings.pot")


def compile_po_to_mo(language: str):
    """
    Compiles .po file to .mo file for the given language.
    """
    po_file = os.path.join(LOCALE_DIR, language, "LC_MESSAGES", "messages.po")
    mo_file = os.path.join(LOCALE_DIR, language, "LC_MESSAGES", 'messages.mo')
    try:
        os.makedirs(os.path.dirname(mo_file), exist_ok=True)
        subprocess.run(['msgfmt', '-o', mo_file, po_file], check=True)
        print(f"Compiled {po_file} to {mo_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {po_file}: {e}")
    except FileNotFoundError:
        print(f"PO file not found: {po_file}")


def update_po_files():
    """
    Updates existing .po files with new strings from .pot file
    """
    if not os.path.exists(TRANSLATION_POT_FILE):
        print(f"Error: POT file not found at {TRANSLATION_POT_FILE}")
        return

    pot = polib.pofile(TRANSLATION_POT_FILE)

    for lang in SUPPORTED_LANGUAGES:
        po_file_path = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES",
                                    "messages.po")

        # Если .po файла нет, создаем его
        if not os.path.exists(po_file_path):
            print(f"Creating {po_file_path} from {TRANSLATION_POT_FILE}")
            try:
                subprocess.run([
                    'msginit', '--input', TRANSLATION_POT_FILE, '--locale',
                    lang, '--output-file', po_file_path
                ], check=True)
                continue
            except subprocess.CalledProcessError as e:
                print(f"Error creating PO file for {lang}: {e}")
                continue

        # Загружаем существующий .po файл
        po = polib.pofile(po_file_path)

        # Флаг для отслеживания изменений
        changes_made = False

        # Проходим по всем строкам в .pot файле
        for potentry in pot:
            # Ищем соответствующую строку в .po файле
            existing_entry = po.find(potentry.msgid)

            # Если строки нет в .po файле, добавляем
            if not existing_entry:
                new_entry = polib.POEntry(
                    msgid=potentry.msgid,
                    msgstr='',  # Пустой перевод
                    comment=potentry.comment
                )
                po.append(new_entry)
                changes_made = True
                print(f"Added new string to {lang} PO: {potentry.msgid}")

        # Сохраняем .po файл, если были изменения
        if changes_made:
            po.save(po_file_path)
            print(f"Updated PO file for {lang}")


def generate_po_files():
    """
    Generates .po files from the pot file if they don't exist.
    """
    if not os.path.exists(TRANSLATION_POT_FILE):
        print(f"Error: POT file not found at {TRANSLATION_POT_FILE}")
        return

    for lang in SUPPORTED_LANGUAGES:
        po_file = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES", "messages.po")
        os.makedirs(os.path.dirname(po_file), exist_ok=True)

        if not os.path.exists(po_file):
            print(f"Creating {po_file} from {TRANSLATION_POT_FILE}")
            try:
                subprocess.run([
                    'msginit', '--input', TRANSLATION_POT_FILE, '--locale',
                    lang, '--output-file', po_file
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error creating PO file for {lang}: {e}")


def main():
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Locale Directory: {LOCALE_DIR}")
    print(f"POT File: {TRANSLATION_POT_FILE}")

    print("Updating .po files with new strings...")
    update_po_files()

    print("Compiling .mo files...")
    for lang in SUPPORTED_LANGUAGES:
        compile_po_to_mo(lang)


if __name__ == "__main__":
    main()
