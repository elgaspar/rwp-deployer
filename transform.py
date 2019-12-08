from pathlib import Path
import os
import shutil


def tranform_zip_file(zipfile, tmp_dir):
    __extract_archive(zipfile, tmp_dir)
    __remove_file(zipfile)
    repo_name = Path(zipfile).stem
    __rename_dir(repo_name, tmp_dir)
    __create_archive(zipfile, tmp_dir)
    __remove_dir(tmp_dir)


def __extract_archive(zipfile, output_dir):
    print('Extracting...')
    try:
        shutil.unpack_archive(zipfile, output_dir)
    except Exception:
        print("ERROR on extracting archive")
        exit()


def __rename_dir(repo_name, tmp_dir):
    new_name = tmp_dir + "/" + repo_name
    old_name = new_name + "-master"
    os.rename(old_name, new_name)


def __create_archive(new_archive_file, dir_with_content):
    print('Creating zip archive...')
    try:
        filepath = __trim_extension(new_archive_file)
        shutil.make_archive(filepath, 'zip', dir_with_content)
    except Exception:
        print("ERROR on creating archive")
        exit()


def __trim_extension(filepath):
    return os.path.splitext(filepath)[0]


def __remove_file(filepath):
    os.remove(filepath)


def __remove_dir(dirpath):
    print('Removing temporary files...')
    shutil.rmtree(dirpath)
