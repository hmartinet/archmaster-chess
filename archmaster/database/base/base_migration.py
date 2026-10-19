
from archmaster.exceptions import MigrationUserException
from archmaster.translations import gettext as _


class BaseMigration:
    _version = 1

    def check_version(self, version):
        if version > self._version:
            raise MigrationUserException(_(
                "Database version {file_version} is newer than "
                "supported version {supported_version}.").format(
                    file_version=version,
                    supported_version=self._version
                )
            )
        if version < self._version:
            self.migrate_from(version)

    def migrate_from(self, version):
        for v in range(version + 1, self._version + 1):
            func = getattr(self, f'migrate_v{v}')
            if func and callable(func):
                func()
            else:
                raise MigrationUserException(_(
                    "No migration process found "
                    "for version {version}.").format(
                        version=version
                    )
                )
