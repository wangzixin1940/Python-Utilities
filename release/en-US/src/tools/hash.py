import hashlib
import os
import sys
import time

os.chdir(os.path.dirname(__file__))

def get_file_md5(fname):
    m = hashlib.md5()   # Create md5 object
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) # Update md5 object
    return m.hexdigest() # Return md5 object

def get_file_sha256(fname):
    m = hashlib.sha256()   # Create sha256 object
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) # Update sha256 object
    return m.hexdigest() # Return sha256 object

def get_file_sha1(fname):
    m = hashlib.sha1()   # Create sha1 object
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) # Update sha1 object
    return m.hexdigest() # Return sha1 object

def get_file_sha224(fname):
    m = hashlib.sha224()   # Create sha224 object
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) # Update sha224 object
    return m.hexdigest() # Return sha224 object

def main():
    argvs = sys.argv
    if len(argvs) > 5 or len(argvs) < 2:
        print("""Usage:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : Name of file, eg. "1.py"、"HelloWorld.java"

--check : Check file MD5、SHA256、SHA1 value, eg. "--check -md5 1234567890abcdef"
    value : The md5 value of the original file, eg. "1234567890abcdef"(it usually comes from the website or person that provided the document)
    -md5 : Verify the MD5 value of the file
    -sha256 : Verify the SHA256 value of the file
    -sha1 : Verify the SHA1 value of the file
    Note: -md5, -sha256, -sha1, -sha224 cannot be used at the same time.

ERROR: too many or too few parameters

""")
        return 1
    filename = argvs[1].strip()
    if not os.path.isfile(filename):
        print("ERROR! File Not Found, please check the file name!")
        return 2
    if "--check" in argvs and len(argvs) == 5:
        if "-md5" == argvs[3]:
            value = argvs[3]
            if get_file_md5(filename) == value:
                print("File md5 values is correct.")
                print("File md5 value: ",get_file_md5(filename))
            else:
                print("File md5 value is wrong!")
                print("File md5 value: ",get_file_md5(filename))
            return 0
        elif "-sha256" == argvs[3]:
            value = argvs[3]
            if get_file_sha256(filename) == value:
                print("File sha256 values is correct.")
                print("File sha256 value: ",get_file_sha256(filename))
            else:
                print("File sha256 values is wrong!")
                print("File sha256 value: ",get_file_sha256(filename))
            return 0
        elif "-sha1" == argvs[3]:
            value = argvs[3]
            if get_file_sha1(filename) == value:
                print("File sha1 values is correct.")
                print("File sha1 value: ",get_file_sha1(filename))
            else:
                print("File sha1 values is wrong!")
                print("File sha1 value: ",get_file_sha1(filename))
            return 0
        elif "-sha224" == argvs[3]:
            value = argvs[4]
            if get_file_sha224(filename) == value:
                print("File sha224 values is correct.")
                print("File sha224 value: ",get_file_sha224(filename))
            else:
                print("File sha224 values is wrong!")
                print("File sha224 value: ",get_file_sha224(filename))
            return 0
        else:
            print("""Usage:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : Name of file, eg. "1.py"、"HelloWorld.java"

--check : Check file MD5、SHA256、SHA1 value, eg. "--check -md5 1234567890abcdef"
    value : The md5 value of the original file, eg. "1234567890abcdef"(it usually comes from the website or person that provided the document)
    -md5 : Verify the MD5 value of the file
    -sha256 : Verify the SHA256 value of the file
    -sha1 : Verify the SHA1 value of the file
    Note: -md5, -sha256, -sha1, -sha224 cannot be used at the same time.

ERROR: invalid parameters

""")
    elif "--check" in argvs and len(argvs) == 3:
        print("""Usage:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : Name of file, eg. "1.py"、"HelloWorld.java"

--check : Check file MD5、SHA256、SHA1 value, eg. "--check -md5 1234567890abcdef"
    value : The md5 value of the original file, eg. "1234567890abcdef"(it usually comes from the website or person that provided the document)
    -md5 : Verify the MD5 value of the file
    -sha256 : Verify the SHA256 value of the file
    -sha1 : Verify the SHA1 value of the file
    Note: -md5, -sha256, -sha1, sha224 cannot be used at the same time.

ERROR: missing parameters

""")
        return 3
    elif len(argvs) > 5:
        print("""Usage:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : Name of file, eg. "1.py"、"HelloWorld.java"

--check : Check file MD5、SHA256、SHA1 value, eg. "--check -md5 1234567890abcdef"
    value : The md5 value of the original file, eg. "1234567890abcdef"(it usually comes from the website or person that provided the document)
    -md5 : Verify the MD5 value of the file
    -sha256 : Verify the SHA256 value of the file
    -sha1 : Verify the SHA1 value of the file
    Note: -md5, -sha256, -sha1, -sha224 cannot be used at the same time.

ERROR: too many parameters

""")
        return 5
    elif len(argvs) == 2:
        print("File name: ",filename)
        print("File size: ",os.path.getsize(filename)," bytes")
        print("File type: ",os.path.splitext(filename)[1])
        print("File last modified time: ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(filename))))
        print("File MD5 value: ",get_file_md5(filename))
        print("File SHA256 value: ",get_file_sha256(filename))
        print("File SHA1 value: ",get_file_sha1(filename))
        print("File SHA224 value: ",get_file_sha224(filename))
        return 0
    else :
        print("""Usage:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : Name of file, eg. "1.py"、"HelloWorld.java"

--check : Check file MD5、SHA256、SHA1 value, eg. "--check -md5 1234567890abcdef"
    value : The md5 value of the original file, eg. "1234567890abcdef"(it usually comes from the website or person that provided the document)
    -md5 : Verify the MD5 value of the file
    -sha256 : Verify the SHA256 value of the file
    -sha1 : Verify the SHA1 value of the file
    Note: -md5, -sha256, -sha1, -sha224 cannot be used at the same time.

ERROR: an unknown error or invalid parameter

""")
        return 4

if __name__ == "__main__":
    sys.exit(main())