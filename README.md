# Windows 实用工具使用指南（Simplified Chinese）


![Logo](images/logo.png)

## 开发者工具使用指南

### 检测网络连接状态

点击按钮，输入网址**（注：网址带“HTTPS://”或者“HTTP://”）**。

点击确定之后会为您检测网络的连接状态，并且返回一个状态码。

*示例：*

- *200：连接成功（Success）*
- *404：网址不存在（Not Found）*
- *500：连接失败（Bad Request）*

*在 V1.1.1 加入*

### 翻译器

点击按钮，如果暂未输入百度AppID和秘钥，将提示输入。**（在[百度翻译开放平台](https://fanyi-api.baidu.com/)获取）**然后输入文本，选择目标语言，将自动识别原语言来翻译。

<del>您可能会问目标语言列表的单词是什么，它们其实是各种代表语言的单词的缩写，具体在[百度翻译开放平台文档](https://fanyi-api.baidu.com/doc/21)中查看。</del>

**V 1.4.2 更新 （2024/3/31）：已经优化，显示各种语言的中文名称，并增加到28种语言！**

您可以调整它们的顺序。具体在 data/translator.languages.json

您可以在“data/translator.appid.json”内更改您的AppID和秘钥，也可以在当天的日志中查看参数（高级）。

*“AppID”绝对不是“Apple ID”！（开玩笑的）*

*在 V 1.3.1 加入*

### Password Creator

一个帮助您生成强密码的工具，可选择插入符号、数字或者大写字母。生成后，可一键复制到剪贴板！

> [!NOTE]
>
> 文件位置：./src/passwordCreator/main.py

### 文件工具

> [!IMPORTANT]
>
> 此工具集成在主界面的一个菜单按钮里！

#### JSON转XML

在main.py内置的程序，可帮助您从JSON文件轻松转到XML文件！

#### XML转JSON

在main.py内置的程序，可帮助您从XML文件轻松转到JSON文件！

#### 文件差异对比

比较两个文件，并将差异保存到HTML文件。

### Licence 创造器

能够帮您创造GitHub许可证的工具，只需填入一些信息，即可创造您的LICENCE文件！

### IP工具

#### 获取IP地址

输入主机名或者输入“@default”获取IP地址

#### 解析IP地址

输入IP地址来获得主机名



## 绘画工具使用指南

### 字符画

首先，准备一张 JPG/JPEG/PNG/GIF/BMP 格式图片。

然后按下按钮，浏览到这张图片。

如果文件符合格式标准，将在和图片同一级目录之下生成一个HTML文件。里面就是一幅字符画。

*题外话，这张字符画由字符 “M”、“N”、“H”、“Q”、“$”、“O”、“C”、“?”、“7”、“>”、“!”、“:”、“-”、“;”、“.” 组成。*

*在 V 1.2.1 加入*

### Bing每日一图

从Bing上获取每日一图，然后保存到您的计算机上！

*在 V 1.13.1 加入*

## 其他工具使用指南

### 计算器

Windows 自带程序 “calc.exe”。请不要在macOS上运行。

*在 V 1.7.2 中添加*

### 二维码工具

#### 生成二维码

一个可以帮助您生成二维码的工具。

#### 解析二维码

一个可以帮助您解析二维码的工具。

*在 V 1.14.1 中添加*



## 系统工具

### Theme Switcher

每次加载程序都会优先加载这个json文件（data/theme.json），读取里面的内容（theme键），使用theme键下的值当做主题。

**只能是ttkbootstrap主题！不能把此文件或者此键值删除！**

> [!WARNING]
>
> **这个方法不安全，已经废弃**

> [!NOTE]
>
> 文件位置：./data/theme.json

*在 V 1.7.3 添加*

### Theme Switcher GUI Program

基于theme.json开发，可预览效果的程序。**并且实时提供预览，更加安全！**

> [!NOTE]
>
> 文件位置：./tools/configurator.py

*在 V 1.8.1 添加*

### Theme Switcher CUI Program

一个命令行工具，和Theme Switcher GUI Program使用相同的核心代码

> 用法:
>
> python / py configurator.py /theme [theme_name]
>
> theme_name: 主题名称，{themes}的任意一个，必须和/theme参数并用

> [!NOTE]
>
> 文件位置：./tools/cmd/configurator.py


*在 V 1.9.1 添加*

### Clear CUI Program

一个命令行工具，用来清理缓存以及日志

> 用法:
>
> python / py clear.py [/l] [/c] [/p] [/?]
>
> /l : 清除所有日志
>
> /c : 清除所有缓存
>
> /p : 清除所有配置文件
>
> ---
>
> /l /c /p : 清除所有
>
> /? : 显示帮助信息

> [!NOTE]
>
> 文件位置：./tools/clear.py


*在 V 1.9.1 添加*

### Clear GUI Program

和cmd/clear.py一样的核心代码，只是拥有了GUI。

> [!NOTE]
>
> 文件位置：./tools/cmd/clear.py

*在 V 1.9.1 添加*

### MD5 Checker CUI Program

> 校验文件的MD5值，使用针对大文件的“open(rb)”方法
>
> 使用:
>
> python / py md5.py [filename] [--check [value]]
>
> filename : 文件名，比如"1.py"、"HelloWorld.java"等等
>
> --check : 检查文件MD5值，比如"--check 1234567890abcdef"
>
>   ​	value : 原文件MD5值，比如"1234567890abcdef"(一般来源于提供文件的网站或者人)

*在 V 1.9.5 添加*

# Windows Utilities（English）

## Developer Tools User Guide

### Detecting network connection status

Click the button and enter the website address **(Note: the website address is marked with "HTTPS://" or "HTTP://")** . 

After clicking OK, the network connection status will be checked for you and a status code will be returned.
*Example:*

* *200: Connection successful (Success)*
* *404: Website does not exist (Not Found)*
* *500: Connection failed (Bad Request)*

*Added in V 1.1.1*

### Translator

Click the button, if you have not yet entered the Baidu AppID and secret key, you will be prompted to enter they.**(You can obtain it from [Baidu Translate Open Platform](https://fanyi-api.baidu.com/ ).)**Then enter the text, select the target language, and the original language will be automatically recognized for translation.
<del>You may ask what the words in the target language list are, and they are actually abbreviations of various words representing languages, as shown in [Baidu Translate Open Platform Document](https://fanyi-api.baidu.com/doc/21) View in.</del>

**Update V 1.4.2 (March 31, 2024): Optimized to display Chinese names in various languages and added to 28 languages!**

You can add more languages to the list or adjust their order. Specifically, in main.py (Line 222, Col 63)
You can change your AppID and secret key in "logs/appid. json", or view the parameters in the daily logs (advanced).

*"AppID" absolutely not "Apple ID"! (Joking)*

*Added in V 1.3.1*

### Password Creator

A tool that helps you generate strong passwords, with the option to insert symbols, numbers, or uppercase letters. After generation, it can be copied to the clipboard with just one click!

> [!NOTE]
>
> File location: ./src/passwordCreator/main.py
>

### File tools

> [!IMPORTANT]
>
> This tool is integrated into a menu button on the main interface!

#### JSON to XML conversion

The built-in program in main.py can help you easily transfer from JSON files to XML files!

#### XML to JSON conversion

The built-in program in main.py can help you easily transfer from XML files to JSON files!

#### Comparison of file differences

Compare two files and save the differences to an HTML file.



### Licence Creator

A tool that can help you create GitHub licenses, just fill in some information and create your License file!

### IP Tools

#### Get IP Address

Input domain name or input "@default" to get IP address.

#### Resolve Domain

Input IP address to get domain name.




## Drawing Tools User Guide

### Character drawing

Firstly, prepare a JPG/JPEG/PNG/GIF/BMP format image. 

Then press the button to browse to this picture. 

If the file meets the formatting standards, an HTML file will be generated in the same level directory as the image. Inside is a character drawing.
*As a side note, this character drawing consists of characters "M", "N", "H", "Q", "$", "O", "C", "?", "7", ">", "!", ":", "-", ";", and ".".*

*Added in V 1.2.1*

### Bing Picture

Get a daily chart from Bing and save it to your computer!

*Added in V 1.12.1*

## Guidelines for using other tools

### Calculator

Windows built-in program "calc. exe".Please do not run this program on macOS.

*Added in V 1.7.2*

### QR Code Tools

#### QR Code Generator

A tool that can help you generate QR codes.

#### QR Code Parser

A tool that can help you parse QR codes.

*Added in V 1.14.1*

## System Tools
### Theme Switcher

Every time the program is loaded, the JSON file (data\theme. json) will be loaded first, and the content inside will be read (theme key), using the value under the theme key as the theme.
**It can only be a ttkbootstrap theme! This file or key cannot be deleted!**

> [!WARNING]
> 
> **This method is not safe and has been abandoned**

> [!NOTE]
>
> File location: ./data/theme.json
>

*Added in V 1.7.3*

### Theme Switcher GUI Program

A program developed based on "theme. json", that allows for preview effects. **And provide real-time preview, more secure!**

> [!NOTE]
>
> File location: ./tools/configurator.py

*Added in V 1.8.1*

### Theme Switcher CUI Program

A command-line tool that uses the same core code as the Theme Switcher GUI Program

>Usage:
>
>python / py configurator. py /theme [theme name]
>
>Theme name: Any one of all ttkbootstrap themes, must be used in conjunction with the /theme parameter

> [!NOTE]
>
> File location: /tools/cmd/configurator.py


*Added in V 1.9.1*

### Clear CUI Program

A command-line tool used to clean cache and logs

>Usage:
>
>Python/py clear.py [/l] [/c] [/p] [/?]
>
>/l: Clear all logs
>
>/c: Clear all caches
>
>/p: Clear all configuration files
>
>---
>
>/l /c /p: Clear all
>
>/?: display help information

> [!NOTE]
>
> File location: /tools/clear.py

*Added in V 1.9.1*

### Clear GUI Program

The same core code as cmd/clear.py, but with a GUI.

> [!NOTE]
>
> File location:/ Tools/cmd/clear. py

*Added in V 1.9.1*

### MD5 Checker CUI Program

Verify the MD5 value of the file and use the "open (rb)" method for large files

> Usage:
>
> Python/py md5. py [file name] [-- check [value]]
>
> File name: The file name, such as "1. py", "HelloWorld. java", and so on
>
> --Check: Check the MD5 value of the file, such as "-- check 1234567890abcdef"
>
> ​	Value: MD5 value of the original file, such as "1234567890abcdef" (usually sourced from the website or person providing the file)
>

*Added in V 1.9.5*



# 如何安装需要的Python包 / How to install the required Python package

``` cmd
pip install -r requirements.txt
```



**由GitHub用户@wangzixin1940编写**

**Written by GitHub user @wangzixin1940**

*希望给一个Star~* <br />
*Give me a star, please~*

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wangzixin1940/Windows-Utilities&type=Date)](https://star-history.com/#wangzixin1940/Windows-Utilities&Date)