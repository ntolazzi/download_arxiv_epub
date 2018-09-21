import sys
import subprocess
import os
import urllib.request as req
import tarfile
import shutil
import glob


def read_cmd_line():
    try:
        arxiv_id = sys.argv[1]
    except IndexError:
        print("Must provide arXiv address or signature as parameter")
        sys.exit(1)
    return arxiv_id


def get_id(input_string):
    if "/" in input_string:
        input_string = input_string.strip("/").split("/")[-1]
    return input_string


def make_tmp_dir(arxiv_id):
    tempdir = "temp_%s" % arxiv_id
    try:
        os.makedirs(tempdir)
    except FileExistsError:
        print("Temporary dir %s already exists, deleting..." % tempdir)
        shutil.rmtree(tempdir)
        os.makedirs(tempdir)
    return tempdir


def download_from_arxiv(arxiv_id):
    download_url = "https://arxiv.org/e-print/%s" % arxiv_id
    req.urlretrieve(download_url, "%s.tar.gz" % arxiv_id)


def untar(filename):
    tar = tarfile.open(filename, "r:gz")
    tar.extractall()
    tar.close()


def convert_to_epub(tex_file):
    subprocess.run(["tex4ebook", tex_file])


if __name__ == "__main__":
    arxiv_string = read_cmd_line()
    arxiv_id = get_id(arxiv_string)
    tempdir = make_tmp_dir(arxiv_id)
    os.chdir(tempdir)
    download_from_arxiv(arxiv_id)
    untar("%s.tar.gz" % arxiv_id)
    convert_to_epub(glob.glob("*.tex")[0])
    epub_file = glob.glob("*.epub")[0]
    shutil.move(epub_file, os.path.join("..", epub_file))
    os.chdir("..")
    shutil.rmtree(tempdir)
    print("Converted and saved under %s" %epub_file)
