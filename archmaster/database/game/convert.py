from .game_base import GameBaseSession
from .game_base_import import GameBaseImport, Progress

progress = Progress(None)


def log_progress():
    print(f"{progress.label}: {int(progress.value * 100)}%")


progress.value_changed.connect(log_progress)

with GameBaseSession('test.db') as session:
    game_import = GameBaseImport(session, progress)
    game_import.import_file("LumbrasGigabase_OTB_2025.7z")
