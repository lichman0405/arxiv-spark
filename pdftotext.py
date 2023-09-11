# Description: This file contains the class used to extract text from PDF files.
# Author: Shibo Li, MiQroEra Inc.
# Date: 2023-09-02
# Version: 1.0


import re
import fitz
import os
import logging


class PDFTextExtractor:
    """
    The class is used to extract text from PDF files.
    """

    def __init__(self, pdf_path):
        """
        Initialize with a PDF file path.
        :param pdf_path: The path to the PDF file.
        """
        self._init_logger()
        if not os.path.exists(pdf_path):
            self.logger.error(f"The file '{pdf_path}' does not exist.")
            raise FileNotFoundError(f"The file '{pdf_path}' does not exist.")
        if not pdf_path.endswith('.pdf'):
            self.logger.error("The specified file is not a PDF.")
            raise ValueError("The specified file is not a PDF.")
        self.pdf_path = pdf_path

    def _init_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def preprocess(self, text):
        """
        Preprocess the text extracted from the PDF file.
        :param text: The text extracted from the PDF file.
        :return: The preprocessed text.
        """
        text = text.replace('\n', ' ')
        text = re.sub('\s+', ' ', text)
        return text

    def pdf_to_text(self, start_page=1, end_page=None):
        """
        Extract text from the PDF file.
        :param start_page: The start page number.
        :param end_page: The end page number.
        :return: A list of text.
        """
        with fitz.open(self.pdf_path, filetype="pdf") as doc:
            total_pages = doc.page_count

            if end_page is None:
                end_page = total_pages

            if not isinstance(start_page, int) or start_page < 1 or start_page > total_pages:
                raise ValueError(
                    "The 'start_page' parameter must be a positive integer and less than or equal to the total number of pages.")

            if not isinstance(end_page, int) or end_page < 1 or end_page > total_pages:
                raise ValueError(
                    "The 'end_page' parameter must be a positive integer and less than or equal to the total number of pages.")

            text_list = []

            for i in range(start_page - 1, end_page):
                text = doc.load_page(i).get_text("text")
                text = self.preprocess(text)
                text_list.append(text)

        return text_list

    def text_to_chunks(self, texts, word_length=150, start_page=1):
        """
        Split the text into chunks.
        :param texts: A list of text.
        :param word_length: The maximum number of words in each chunk.
        :param start_page: The start page number.
        :return: A list of chunks.
        """
        text_toks = [t.split(' ') for t in texts]
        chunks = []

        for idx, words in enumerate(text_toks):
            chunks += self._create_chunks(words, idx,
                                          word_length, start_page, text_toks)
        return chunks

    def _create_chunks(self, words, idx, word_length, start_page, text_toks):
        """
        Create chunks from the text.
        :param words: A list of words.
        :param idx: The index of the text.
        :param word_length: The maximum number of words in each chunk.
        :param start_page: The start page number.
        :param text_toks: A list of text.
        :return: A list of chunks.
        """
        chunks = []
        for i in range(0, len(words), word_length):
            chunk = words[i: i + word_length]
            if ((i + word_length) > len(words)) and (len(chunk) < word_length) and (len(text_toks) != (idx + 1)):
                text_toks[idx + 1] = chunk + text_toks[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'[Page no. {idx+start_page}]' + ' ' + '"' + chunk + '"'
            chunks.append(chunk)
        return chunks