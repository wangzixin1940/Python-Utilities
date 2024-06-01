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

def get_file_sha224(fname):
    m = hashlib.sha224()   #创建sha224对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data) #更新sha224对象
    return m.hexdigest() #返回sha224对象

def main():
    argvs = sys.argv
    if len(argvs) > 5 or len(argvs) < 2:
        print("""使用:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5、SHA256、SHA1值，比如"--check -md5 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)
    -md5 : 校验文件MD5值
    -sha256 : 校验文件SHA256值
    -sha1 : 校验文件SHA1值
    注意：-md5、-sha256、-sha1、-sha224不可以同时使用。

错误：参数过多或者过少。

""")
        return 1
    filename = argvs[1].strip()
    if not os.path.isfile(filename):
        print("错误！文件不存在，请检查文件名和路径！")
        return 2
    if "--check" in argvs and len(argvs) == 5:
        if "-md5" == argvs[3]:
            value = argvs[4]
            if get_file_md5(filename) == value:
                print("文件MD5值正确！")
                print("文件MD5值：",get_file_md5(filename))
            else:
                print("文件MD5值错误！")
                print("文件MD5值：",get_file_md5(filename))
            return 0
        elif "-sha256" == argvs[3]:
            value = argvs[4]
            if get_file_sha256(filename) == value:
                print("文件SHA256值正确！")
                print("文件SHA256值：",get_file_sha256(filename))
            else:
                print("文件SHA256值错误！")
                print("文件SHA256值：",get_file_sha256(filename))
            return 0
        elif "-sha1" == argvs[3]:
            value = argvs[4]
            if get_file_sha1(filename) == value:
                print("文件SHA1值正确！")
                print("文件SHA1值：",get_file_sha1(filename))
            else:
                print("文件SHA1值错误！")
                print("文件SHA1值：",get_file_sha1(filename))
            return 0
        elif "-sha224" == argvs[3]:
            value = argvs[4]
            if get_file_sha224(filename) == value:
                print("文件SHA224值正确！")
                print("文件SHA224值：",get_file_sha224(filename))
            else:
                print("文件SHA224值错误！")
                print("文件SHA224值：",get_file_sha224(filename))
            return 0
        else:
            print("""使用:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5、SHA256、SHA1值，比如"--check -md5 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)
    -md5 : 校验文件MD5值
    -sha256 : 校验文件SHA256值
    -sha1 : 校验文件SHA1值
    注意：-md5、-sha256、-sha1、-sha224不可以同时使用。

错误：无效参数。

""")
    elif "--check" in argvs and len(argvs) in [3,4]:
        print("""使用:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5、SHA256、SHA1值，比如"--check -md5 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)
    -md5 : 校验文件MD5值
    -sha256 : 校验文件SHA256值
    -sha1 : 校验文件SHA1值
    注意：-md5、-sha256、-sha1、-sha224不可以同时使用。

错误：缺少必须参数。

""")
        return 3
    elif len(argvs) > 5:
        print("""使用:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5、SHA256、SHA1值，比如"--check -md5 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)
    -md5 : 校验文件MD5值
    -sha256 : 校验文件SHA256值
    -sha1 : 校验文件SHA1值
    注意：-md5、-sha256、-sha1、-sha224不可以同时使用。

错误：参数过多。

""")
        return 5
    elif len(argvs) == 2:
        print("文件名：",filename)
        print("文件大小：",os.path.getsize(filename),"字节")
        print("文件类型：",os.path.splitext(filename)[1])
        print("文件最后修改时间：",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(filename))))
        print("文件MD5值：",get_file_md5(filename))
        print("文件SHA256值：",get_file_sha256(filename))
        print("文件SHA1值：",get_file_sha1(filename))
        print("文件SHA224值：",get_file_sha224(filename))
        return 0
    else :
        print("""使用:
python / py md5.py [filename] [--check [-md5][-sha256][-sha1][-sha224][value]]

filename : 文件名，比如"1.py"、"HelloWorld.java"等等

--check : 检查文件MD5、SHA256、SHA1值，比如"--check -md5 1234567890abcdef"
    value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)
    -md5 : 校验文件MD5值
    -sha256 : 校验文件SHA256值
    -sha1 : 校验文件SHA1值
    注意：-md5、-sha256、-sha1、-sha224不可以同时使用。

错误：未知错误或者无效参数

""")
        return 4

if __name__ == "__main__":
    sys.exit(main())