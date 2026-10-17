# Archmaster Chess

Archmaster Chess is a desktop application for chess analysis, built with Python and PySide6.

## Development setup

### Requirements

- Python
- Git

### Linux + macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
python -m pip install -r requirements-dev.txt
```

### Windows

Run the following commands in PowerShell from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel setuptools
python -m pip install -r requirements-dev.txt
```

## Running the application

Run Archmaster Chess from the project root with the virtual environment activated.

```bash
python -m archmaster.archmaster
```

## Internationalization (i18n)

Archmaster Chess uses [Babel](https://babel.pocoo.org/) to extract translatable messages and manage translation catalogs, and Python's `gettext` module to load compiled translations.

The `messages.py` script provides a convenient interface for the translation workflow.

### Extract messages

Extract translatable strings from the source code and update the template:

```bash
python messages.py extract
```

This generates or updates `archmaster/locales/messages.pot`.

### Initialize a translation

Create a translation catalog for a new locale, replacing `<locale>` with the appropriate language code:

```bash
python messages.py init <locale>
```

For example, to initialize French:

```bash
python messages.py init fr
```

Translation catalogs are created under `archmaster/locales/`.

### Update existing translations

After adding or changing translatable strings, update the existing catalogs:

```bash
python messages.py update
```

Existing translations are preserved where possible, and new or changed messages are marked for review.

### Compile translations

After translating or updating a catalog, compile the translation files:

```bash
python messages.py compile
```

This generates the compiled `.mo` files required by `gettext` at runtime.

### Typical workflow

When developing new features:

1. Mark user-facing strings for translation using `_()`.
2. Run `python messages.py extract`.
3. Run `python messages.py update` for existing locales, or `python messages.py init <locale>` for a new locale.
4. Translate the messages in the relevant `.po` files.
5. Run `python messages.py compile`.
6. Run the application and verify the translations.

Example:

```python
from archmaster.translations import gettext as _

self.setWindowTitle(_("Chess analysis"))
```

Run all commands from the project root with the development virtual environment activated.
