from typetrainer import settings


def open_local_file(filename: str):
    try:
        with open(filename, encoding=settings.FILE_ENCODING) as file:
            data = file.read()
            texts = data.split('\n\n')
            return texts
    except FileNotFoundError:
        return
