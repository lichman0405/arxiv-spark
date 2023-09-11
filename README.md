# PDF-SparkCHAT

Shibo Li, MiQroEra Inc.

## 描述

PDF-SparkCHAT是一个用于提取PDF文件内容并与SparkAI进行交互的应用程序。用户可以通过Arxiv ID或关键词查询来获取相关论文的PDF，并与SparkAI进行语义搜索和对话。

## 作者

Shibo Li, MiQroEra Inc.

## 版本

1.0

## 日期

2023-09-02

## 安装

如果您使用的是pypi的官方源，那么安装会非常简单。
建议您仍然使用python虚拟环境管理工具，比如：conda。
您可以在这里看到如何在您使用的系统下，下载[Anaconda](https://www.anaconda.com/download)。这个网页提供了完整且相近的**Anaconda**使用说明和安装说明。

本项目使用了以下pypi的第三方库：

1. art - 用于生成艺术字体文本，主要用于欢迎页面。
2. os - 用于与操作系统交互，实现文件和目录操作。
3. PySparkAI - 用于与SparkAI进行交互和对话。这个也是我对讯飞星火LLM的api做的高级封装的库，已经打包上传至pypi官方源。您可以在[xunfeispark](https://pypi.org/project/xunfeispark/)找到下载链接。或者直接使用下列命令进行安装。

```bash
pip install xunleispark
```

但需要注意的是，如果你使用的国内的pypi源镜像，很有可能xunleispark库没有被及时同步。在这种情况下，您仍需要手工下载安装。您也可以直接访问[xunfeispark](https://github.com/lichman0405/xunfeispark)的github来查看更详细的使用方法。

4. tensorflow-hub - 用于调用`universal-sentence-encoder`对切片论文进行编码。一般来说，访问这个服务您并不需要特殊的网络通道。如果需要，请您自行查找使用方法。
5. pymupdf - 用于解析PDF。PyMuPDF是MuPDF的增强型Python绑定，MuPDF是一个轻量级PDF、XPS和电子书查看器、渲染器和工具包，由Artifex Software, Inc维护和开发。

您可以依次手动使用`pip install`命令进行安装：

```bash
pip install art xunleispark tensorflow-hub pymupdf scikit-learn
```

目前没有绝对的版本依赖限制，安装最新版本就好。

## 文件说明

1. arxiv_api.py - 包含ArxivAPI类，用于通过ArXiv API进行论文查询。
2. arxiv_result_parser.py - 包含ArxivResultParser类，用于解析ArXiv API的查询结果。
3. pdf_semantic_search.py - 包含SemanticSearch类和其他函数，用于处理PDF文本并执行语义搜索。
4. pdftotext.py - 包含PDFTextExtractor类，用于从PDF文件中提取文本。
5. welcome.py - 包含一个函数，用于打印欢迎页面。
6. main.py - 主脚本，用于协调所有其他模块和类，提供用户交互界面。

## 如何使用

- 首先您需要拥有一个[讯飞开放平台](https://www.xfyun.cn/)的账户，并且完成个人实名认证。

- 然后您需要申请**API使用权限**，您可以访问[这里](https://xinghuo.xfyun.cn/)。

- 目前，讯飞提供v1.5版本和v2.0版本的Web API访问接口，目前也提供一次性的免费的基于个人账户的Token套餐。

- 同时，您需要在讯飞开放平台中建立一个APP，然后将讯飞开放平台的不同服务接入这个APP，并最终获取如下信息并妥善保存。

  - APP_ID
  - APP_KEY
  - APP_SECRET
  - SPARK_URL
  - DOMAIN

  详细使用方法您可以[参阅](https://www.xfyun.cn/doc/spark/Web.html)。但事实上，您并不需要完全学会如何通过代码调用讯飞星火API。`xunfeispark`这个库已经高度封装了调用方法，您只需要按照[xunfeispark](https://pypi.org/project/xunfeispark/)中README.md提供的使用方法，就可以方便使用。当然，由于pypi上项目名称的限制，实际使用xunfeispark时，您需要通过如下方法导入：

  ```python
  from pysparkai import PySparkAI
  ```

- 运行main.py脚本来启动应用程序。

- 程序运行时需要您在terminal中首先输入arxiv的检索方法。本项目提供两种检索方法：

  - 基于关键词的检索。如果你选择keywords，那么程序在要求您输入您的检索时，您的输入需要包含如下两个部分：

    ```python
    au: 作者姓名, ti: 论文题目
    ```

    这种检索方法目前由于本项目涉及的原因，很有可能会出现无法精确查找到您想要的论文。这种检索方法更适合追踪`作者`最新的研究成果。

  - 基于id的检索。如果你选择id_list，那么程序会要求您输入论文在arxiv上的entry_id。这样能够直接命中论文，是一种更加建议的选择。

  - 程序要求您输入`max_results`，此处建议输入1。后续会进行批量论文功能的开发，敬请期待。

- 接下来，需要用户输入之前讯飞开放平台所提供的用户个人信息。

- 一切流程结束之后，您就可以通过SparkAI进行语义搜索和对话。

- *如果您的访问地址是在中国大陆，那么很有可能在下载论文PDF时会耗费您不少时间，请您耐心等待。程序在论文下载完成的时候，会告知您。*

## 注意事项

由于LLMs的限制，生成的答案可能不是很准确。这个工具仅作为辅助工具使用，不能替代人类专家。

您也可以修改`pdf_semantic_search.py`中，`generate_prompt`方法中的prompt。这里需要鸣谢[Bhaskar Tripathi](https://github.com/bhaskatripathi)所提供的项目[PDFGPT](https://github.com/bhaskatripathi/pdfGPT)，尤其是其中的prompt。