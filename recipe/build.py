import os
import platform
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import sys


def _determine_filename():
   print(f"Platform: {platform.uname()}")

   if platform.uname().system == "Darwin":
      return "darwin-universal.cli.package.zip"  
   if platform.uname().system == "Windows":
      return "windows-amd64.cli.package.zip"
   return "linux-amd64.cli.package.zip"

def _files(zipfile):
   if zipfile.startswith("windows"):
       return ["dataformat.exe", "datasets.exe"]
   return ["dataformat", "datasets"]


# Setup
PREFIX=os.environ['PREFIX']

BIN_DIR='{}/bin/'.format(PREFIX)
if not os.path.exists(BIN_DIR):
    os.mkdir(BIN_DIR)

if len(sys.argv) != 2:
   raise Exception("Must pass one argument, the version string, to this script")
version = sys.argv[1]
filename = _determine_filename()

url = f"https://github.com/ncbi/datasets/releases/download/v{version}/{filename}"
print(f"URL: {url}")

resp = urlopen(url)
myzip = ZipFile(BytesIO(resp.read()))


for file in _files(filename):
   output = f"{BIN_DIR}/{file}"
   print(f"Writing {output}")
   with open(output, "wb") as fh:
      for line in myzip.open(file).readlines():
         fh.write(line)
   os.chmod(output, 0o755)

