import importlib
import os
import codecs

class Kyrie():

    strings = "abcdefghijklmnopqrstuvwxyz0123456789"

    def decrypt(e: str, key: str):
        text = Kyrie._decrypt(e, key)
        return Kyrie._dkyrie(text)

    def _dkyrie(text: str):
        r = ""
        for a in text:
            if a in Kyrie.strings:
                i = Kyrie.strings.index(a)+1
                if i >= len(Kyrie.strings):
                    i = 0
                a = Kyrie.strings[i]
            r += a
        return r

    def _decrypt(text: str, key: str = None):
        t = [chr(ord(t)-key) if t != "ζ" else "\n" for t in text]
        return "".join(t)

file_name = input("Fichier à deob: ")

with open(file_name) as file:
    code = "mdr=" + file.read()[4:]
with open("to_deob.py", "w") as file:
    file.write(code)

from to_deob import mdr as code

loader = importlib.machinery.SourceFileLoader('<py_compile>', file_name)
source_bytes = loader.get_data(file_name)
source_hash = importlib.util.source_hash(source_bytes)
bytecode = importlib._bootstrap_external._code_to_hash_pyc(code, source_hash)

with open(file_name[:-3] + ".pyc", "wb") as file:
    file.write(bytecode)

os.system(f"pycdas {file_name[:-3]}.pyc > result.txt")

with open("result.txt") as file:
    lines = file.read().splitlines()
    code = "".join(lines[30].split()).replace("'", "")
    code = codecs.decode(code, "unicode-escape").encode('latin1').decode('utf-8')

code_deob = Kyrie.decrypt(code, 49348)
with open("deob.py", "w", errors="ignore") as file:
    file.write(code_deob)

os.remove(f"{file_name[:-3]}.pyc")
os.remove("result.txt")
os.remove("to_deob.py")
