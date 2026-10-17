import gettext as gettext_module
from pathlib import Path

from .resources import Resources


class Translations:
    def __init__(self):
        self.locales_dir = Path(__file__).parent / "locales"
        self.set_language(Resources().config.lang)

    def set_language(self, language):
        self.translator = gettext_module.translation(
            "messages",
            localedir=self.locales_dir,
            languages=[language],
            fallback=True,
        )


translations = Translations()
gettext = translations.translator.gettext
ngettext = translations.translator.ngettext
npgettext = translations.translator.npgettext
