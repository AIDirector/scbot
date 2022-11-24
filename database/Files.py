from peewee import PrimaryKeyField, TextField, IntegerField

from . import BaseModel


class FilesTable(BaseModel):
    file_id = PrimaryKeyField(null=False)
    name = TextField(unique=True)
    telegram_id = TextField(unique=True)

    @staticmethod
    def get_file_by_filename_or_none(filename):
        return FilesTable.get_or_none(FilesTable.name == filename)

    @staticmethod
    async def do_action_with_file(filename, action):
        file = FilesTable.get_file_by_filename_or_none(filename)
        if file is not None:
            await action(file.telegram_id)
        else:
            with open(f"data/{filename}", 'rb') as photo:
                new_id = await action(photo)
                if new_id is not None:
                    FilesTable.create(name=filename, telegram_id=new_id)

    @staticmethod
    async def do_action_with_files(filenames, action):
        def get_file(filename):
            file = FilesTable.get_file_by_filename_or_none(filename)
            if file is not None:
                return file.telegram_id
            else:
                file = open(f"data/{filename}", 'rb')
                return file

        files = []
        try:
            for i in filenames:
                files.append(get_file(i))
            ids = await action(files)
        finally:
            for file in files:
                if not isinstance(file, str):
                    file.close()
