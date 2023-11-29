from concurrent.futures import ThreadPoolExecutor
import sys
from pathlib import Path
import shutil

all_folders = ["images", "video", "documents", "audio", "archives", "unknown"]
images = []
video = []
documents = []
audio = []
archives = []
unknown = []
# this is our dictionary, we`ll use it to find all extensions we need
extensions_we_sort = {
    "images": ["jpeg", "png", "jpg", "svg"],
    "video": ["avi", "mp4", "mov", "mkv"],
    "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx"],
    "audio": ["mp3", "ogg", "wav", "amr"],
    "archives": ["zip", "gz", "tar"],
}


KYRILLIC_SYMBOLS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюяыъэё"  # ah, of course, we create dictionary to transliterate names
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "je",
    "zh",
    "z",
    "y",
    "i",
    "ji",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "ju",
    "ja",
    "y",
    "i",
    "yo",
)

TRANS = {}
for key, value in zip(KYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(
    file_name,
):  # don`t worry, buddy, this will change scary files` names into readable ones
    new_file_name = str(file_name).translate(TRANS)
    other_file_name = ""
    for i in new_file_name:
        if i.isalnum() or i == ".":
            other_file_name += i
        else:
            i = "_"
            other_file_name += i
    return other_file_name


def deleter(path):  # Deletes empty folders
    p = Path(path)
    for folder in p.iterdir():
        if folder.name not in all_folders:
            if folder.is_dir():
                deleter(folder)
                if not any(folder.iterdir()):
                    folder.rmdir()


def create_folders(path: Path):  # Create new folders for sorting
    for folder in all_folders:
        folder_path = path.joinpath(folder)
        if not folder_path.exists():
            folder_path.mkdir()


def dearchivate(file_name, path: Path):  # To unpack archives
    path_to_unpack = path.joinpath("archives")
    folder_path = Path(path_to_unpack) / Path(file_name).name.replace(
        Path(file_name).suffix, ""
    )
    folder_path.mkdir(exist_ok=True)
    if file_name.suffix == ".zip":
        shutil.unpack_archive(file_name, folder_path, format="zip")
    elif file_name.suffix == ".tar":
        shutil.unpack_archive(file_name, folder_path, format="tar")
    elif file_name.suffix == ".gz":
        shutil.unpack_archive(file_name, folder_path, format="gz")


def sorter(file_name):  # This one sorts files into directories
    new_name = file_name.name
    suffix = file_name.suffix.replace(".", "")

    for key in extensions_we_sort:
        if suffix in extensions_we_sort[key]:
            key.append(new_name)
            target_folder = global_path.joinpath(key)
            try:
                new_path = target_folder.joinpath(normalize(new_name))
                shutil.move(str(file_name), str(new_path))
            except PermissionError:
                print(f"The file may be open now. Please, close it.")
        else:
            unknown.append(new_name)
            its_folder = global_path.joinpath("unknown")
            new_path = its_folder.joinpath(normalize(new_name))
            shutil.move(str(file_name), str(new_path))


def parser_func(path):
    all_files = []
    all_dirs = []
    for items in path.iterdir():
        if items.name in all_folders:
            continue
        if items.is_dir():
            all_dirs.append(items)
            with ThreadPoolExecutor(
                max_workers=2
            ) as executer:  # Pool executor for sorting directories
                executer.map(parser_func, all_dirs)
        elif items.is_file():
            all_files.append(items)
            with ThreadPoolExecutor(max_workers=2) as executer:
                executer.map(sorter, all_files)
        print(items.name)


global_path = Path(sys.argv[1])


def main():  # Осноаная функция
    if len(sys.argv) < 2:
        print("Usage: python module_name.py <path_t_directory>")
        sys.exit(1)

    deleter(global_path)
    create_folders(global_path)
    parser_func(global_path)
    print(f"\nImages: {images}\n")
    print(f"\nAudio: {audio}\n")
    print(f"\nVideo: {video}\n")
    print(f"\nDocuments: {documents}\n")
    print(f"\nArchives: {archives}\n")
    print(f"\nUnknown: {unknown}\n")


if __name__ == "__main__":
    main()
