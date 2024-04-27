import hashlib
import os
import sys
import time

os.chdir(os.path.dirname(__file__))

def get_file_md5(fname):
    m = hashlib.md5()   #创建md5对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #更新md5对象
    return m.hexdigest() #返回md5对象

def get_file_sha256(fname):
    m = hashlib.sha256()   #创建sha256对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #更新sha256对象
    return m.hexdigest() #返回sha256对象

def get_file_sha1(fname):
    m = hashlib.sha1()   #创建sha1对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #更新sha1对象
    return m.hexdigest() #返回sha1对象

def main():
    argvs = sys.argv
    if len(argvs) > 4 or len(argvs) < 2:
        print("""使用:
python / py md5.py [filename] [--check [value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5值，比如"--check 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)

错误：参数过多或者过少。

""")
        return 1
    filename = argvs[1].strip("\"")
    if not os.path.isfile(filename):
        print("错误！文件不存在，请检查文件名和路径！")
        return 2
    if "--check" in argvs and len(argvs) == 4:
        value = argvs[3]
        if get_file_md5(filename) == value:
            print("文件MD5值正确！")
        else:
            print("文件MD5值错误！")
        return 0
    elif "--check" in argvs and len(argvs) == 3:
        print("""使用:
python / py md5.py [filename] [--check [value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5值，比如"--check 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)

错误：缺少必须参数"value"。

""")
        return 3
    elif len(argvs) == 2:
        print("文件名：",filename)
        print("文件大小：",os.path.getsize(filename),"字节")
        print("文件类型：",os.path.splitext(filename)[1])
        print("文件最后修改时间：",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(filename))))
        print("文件MD5值：",get_file_md5(filename))
        print("文件SHA256值：",get_file_sha256(filename))
        print("文件SHA1值：",get_file_sha1(filename))
        return 0
    else :
        print("""使用:
python / py md5.py [filename] [--check [value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5值，比如"--check 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)

错误：未知错误或者无效参数

""")
        return 4

if __name__ == "__main__":
    sys.exit(main())