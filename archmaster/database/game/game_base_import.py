import os
import re
import tempfile
import zlib
from datetime import datetime
from pathlib import Path

import patoolib
from sqlalchemy.orm import Session

from archmaster.exceptions import ImportUserException
from archmaster.gui import Progress
from archmaster.translations import gettext as _

HEADER_REGEX = re.compile(r'\[(\w+)\s+"(.*)"\]')


def parse_int(v):
    if not v:
        return None
    try:
        return int(v)
    except Exception:
        return None


def parse_result(v):
    if not v:
        return -1
    if v == '1/2-1/2':
        return 0
    if v == '1-0':
        return 1
    if v == '0-1':
        return 2
    return -1


def parse_date(v):
    if not v:
        return None
    try:
        return datetime.strptime(v, '%Y.%m.%d').date()
    except Exception:
        return None


class GameBaseImport:
    def __init__(self, session: Session, progress: Progress):
        self.session = session
        self.progress = progress

    def add_game(self, headers, pgn):
        from .game_base import Game
        self.session.add(Game(
            event=headers.get('Event') or '',
            site=headers.get('Site') or '',
            date_at=parse_date(headers.get('Date')),
            round=parse_int(headers.get('Round')),
            white=headers.get('White') or '',
            black=headers.get('Black') or '',
            result=parse_result(headers.get('Result')),
            white_elo=parse_int(headers.get('WhiteElo')),
            black_elo=parse_int(headers.get('BlackElo')),
            white_title=headers.get('WhiteTitle') or '',
            black_title=headers.get('BlackTitle') or '',
            eco=headers.get('ECO') or '',
            time_control=headers.get('TimeControl') or '',
            source=headers.get('Source') or '',
            pgn=zlib.compress(pgn.encode('utf-8')),
        ))

    def parse_pgn(self, lines):
        headers = {}
        pgn_lines = []
        move_lines = []

        def flush():
            nonlocal headers, pgn_lines, move_lines

            if move_lines:
                pgn_lines.extend(('', ' '.join(move_lines)))
                self.add_game(headers, '\n'.join(pgn_lines))

            headers = {}
            pgn_lines = []
            move_lines = []

        for line in lines:
            if not line:
                continue

            match = HEADER_REGEX.match(line)
            if match:
                if move_lines:
                    flush()

                key, value = match.groups()
                headers[key] = value
                pgn_lines.append(line)
            else:
                move_lines.append(line)
        flush()

    def walk_pgn_file(self, path):
        size = os.path.getsize(path)

        if self.progress.step_weights is None:
            self.progress.step_weights = [1.]
        self.progress.next_step(_("Import file {file}.").format(
            file=Path(path).name))

        with open(path, 'rb') as file:
            for line in file:
                self.progress.update_value(
                    file.tell() / size if size > 0 else 0)

                yield line.decode('utf-8').strip()

    def import_file(self, path):
        try:
            if str(path).endswith('.pgn'):
                self.parse_pgn(self.walk_pgn_file(path))
            elif patoolib.is_archive(path):
                with tempfile.TemporaryDirectory() as tmp:
                    patoolib.extract_archive(path, outdir=tmp)
                    files = list(Path(tmp).rglob('*.pgn'))
                    sizes = [os.path.getsize(f) for f in files]
                    total = sum(sizes)
                    self.progress.step_weights = [s / total for s in sizes]
                    for file in files:
                        self.parse_pgn(self.walk_pgn_file(file))
            else:
                raise Exception("Invalid file format.")
        except Exception:
            raise ImportUserException(_(
                "File {file} cannot be read.").format(file=path))
