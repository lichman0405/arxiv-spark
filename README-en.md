# PDF-SparkCHAT

Shibo Li, MiQroEra Inc.

## Description

PDF-SparkCHAT is an application designed for extracting content from PDF files and interacting with SparkAI. Users can obtain PDFs of relevant papers through Arxiv ID or keyword queries and engage in semantic searches and dialogues with SparkAI.

## Author

Shibo Li, MiQroEra Inc.

## Version

1.0

## Date

2023-09-02

## Installation

If you are using the official source of pypi, the installation process will be very straightforward. It is recommended to still use a python virtual environment management tool, such as: conda. You can see here how to download [Anaconda](https://www.anaconda.com/download). This webpage provides comprehensive and recent instructions on how to use and install **Anaconda**.

This project utilizes the following third-party libraries from pypi:

1. `art` - For generating art font text, mainly used for the welcome page.
2. `os` - For interacting with the operating system, enabling file and directory operations.
3. `PySparkAI` - For interaction and dialogue with SparkAI. This is also a high-level encapsulation of the API for iFlytek Spark LLM, which has been packaged and uploaded to the official pypi source. You can find the download link [here](https://pypi.org/project/xunfeispark/) or directly install it using the following command:

```bash
pip install xunleispark
```

However, it should be noted that if you are using a domestic pypi mirror source, it is very likely that the xunleispark library has not been synchronized in time. In this case, you still need to manually download and install it. You can also visit the [xunfeispark GitHub page](https://github.com/lichman0405/xunfeispark) for more detailed usage instructions.

1. `tensorflow-hub` - Used to invoke the `universal-sentence-encoder` to encode sliced papers. Generally speaking, you do not need a special network channel to access this service. If necessary, please find out how to use it yourself.
2. `pymupdf` - Used for parsing PDFs. PyMuPDF is an enhanced Python binding of MuPDF, a lightweight PDF, XPS, and eBook viewer, renderer, and toolkit maintained and developed by Artifex Software, Inc.

You can manually install these libraries in sequence using the `pip install` command:

```bash
pip install art xunleispark tensorflow-hub pymupdf scikit-learn
```

Currently, there are no strict version dependency restrictions, just install the latest versions.

## File Descriptions

1. `arxiv_api.py` - Contains the `ArxivAPI` class, used for paper queries through the `ArXiv API`.
2. `arxiv_result_parser.py` - Contains the `ArxivResultParser` class, used to parse the query results from the ArXiv API.
3. `pdf_semantic_search.py` - Contains the `SemanticSearch` class and other functions, used for processing PDF text and performing semantic searches.
4. `pdftotext.py` - Contains the `PDFTextExtractor` class, used for extracting text from PDF files.
5. `welcome.py` - Contains a function used for printing the welcome page.
6. `main.py` - The main script, used to coordinate all other modules and classes, providing a user interface.

## How to Use

- Firstly, you need to have an account with the [iFlytek Open Platform](https://www.xfyun.cn/), and complete personal real-name verification.

- Then you need to apply for **API usage permissions**, which you can do [here](https://xinghuo.xfyun.cn/).

- Currently, iFlytek provides v1.5 and v2.0 versions of the Web API access interface, and now offers a one-time free personal account Token package. 

- At the same time, you need to create an APP in the iFlytek open platform, integrate various services of the iFlytek open platform into this APP, and finally obtain and securely save the following information:

  - APP_ID
  - APP_KEY
  - APP_SECRET
  - SPARK_URL
  - DOMAIN

  For detailed usage methods, you can [refer here](https://www.xfyun.cn/doc/spark/Web.html). But in fact, you don't need to fully learn how to call the iFlytek Spark API through code. The `xunfeispark` library has already highly encapsulated the calling method. You only need to follow the usage method provided in the README.md in [xunfeispark](https://pypi.org/project/xunfeispark/), and it can be used conveniently. Of course, due to project name restrictions on pypi, you need to import xunfeispark as follows during actual use:

  ```python
  from pysparkai import PySparkAI
  ```

- Run the `main.py` script to start the application.

- During program operation, you need to first input the arxiv retrieval method in the terminal. This project provides two retrieval methods:

  - Keyword-based retrieval. If you choose keywords, when the program asks you to enter your retrieval, your input needs to include the following two parts:

    ```txt
    au: Author name, ti: Paper title
    ```

    This retrieval method, due to reasons involved in this project, is very likely to be unable to accurately find the paper you want. This retrieval method is more suitable for tracking the latest research results of the `author`.

  - ID-based retrieval. If you choose id_list, the program will ask you to enter the paper's entry_id on arxiv. This can directly target the paper and is a more recommended choice.

  - The program asks you to enter `max_results`, where it is recommended to enter 1. Development of batch paper features will be coming soon, so stay tuned.

- Next, the user needs to enter the personal information provided by the iFlytek open platform earlier.

- Once all processes are finished, you can conduct semantic searches and dialogues through SparkAI.

- *If your access location is in mainland China, it is very likely that downloading the paper PDF will take up a lot of your time, please be patient. The program will notify you when the paper download is complete.*

## Precautions

Due to the limitations of LLMs, the generated answers may not be very accurate. This tool is to be used as an auxiliary tool and cannot replace human experts.

You can also modify the `generate_prompt` method in `pdf_semantic_search.py`, especially the prompt. Special thanks to the project [PDFGPT](https://github.com/bhaskatripathi/pdfGPT) provided by [Bhaskar Tripathi](https://github.com/bhaskatripathi), especially for its prompt.