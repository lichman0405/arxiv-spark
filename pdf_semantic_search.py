# Description: This file contains the code for the semantic search model.
# Author: Shibo Li, MiQroEra Inc.
# Date: 2023-09-02
# Version: 1.0

import numpy as np
from sklearn.neighbors import NearestNeighbors
import tensorflow_hub as hub
from pdftotext import PDFTextExtractor
import os

recommender = None
credentials = None


class SemanticSearch:
    _instance = None
    """
    Semantic Search model for searching through text data.
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.use = hub.load(
            'https://tfhub.dev/google/universal-sentence-encoder/4')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        """
        Fit the model with the given data.

        :param data: List of text data.
        :param batch: Batch size for processing.
        :param n_neighbors: Number of neighbors to use for NearestNeighbors.
        """
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def search(self, text, return_data=True):
        """
        Search the fitted data for the nearest neighbors of the given text.

        :param text: Text to search for.
        :param return_data: Whether to return the data or just the indices.
        :return: List of nearest neighbors or their indices.
        """
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        """
        Get the text embeddings for the given texts.

        :param texts: List of texts.
        :param batch: Batch size for processing.
        :return: List of text embeddings.
        """
        embeddings = np.vstack([self.use(texts[i: i + batch])
                               for i in range(0, len(texts), batch)])
        return embeddings

    def load_recommender(self, path, start_page=1):
        """
        Load the recommender with data from the given PDF path.

        :param path: Path to the PDF.
        :param start_page: Start page for reading the PDF.
        :return: Message indicating the status of the loading process.
        """
        extractor = PDFTextExtractor(path)
        texts = extractor.pdf_to_text(start_page=start_page)
        chunks = extractor.text_to_chunks(texts, start_page=start_page)
        self.fit(chunks)
        return 'Corpus Loaded.'


def get_credentials_from_user():
    """
    Get the necessary credentials from the user or environment variables.

    :return: Tuple of credentials.
    """
    APP_ID = os.environ.get('APP_ID') or input("Please enter your APP_ID: ")
    API_KEY = os.environ.get('API_KEY') or input("Please enter your API_KEY: ")
    API_SECRET = os.environ.get('API_SECRET') or input(
        "Please enter your API_SECRET: ")
    SPARK_URL = os.environ.get('SPARK_URL') or input(
        "Please enter your SPARK_URL: ")
    DOMAIN = os.environ.get('DOMAIN') or input("Please enter your DOMAIN: ")

    return APP_ID, API_KEY, API_SECRET, SPARK_URL, DOMAIN


def generate_prompt(question, topn_chunks):
    """
    Generate a prompt for the AI to generate an answer.

    :param question: The query.
    :param topn_chunks: Top n chunks from the search.
    :return: Generated prompt.
    """
    prompt = 'search results:\n\n'
    for c in topn_chunks:
        prompt += c + '\n\n'
    # Add instructions to the prompt
    prompt += (
        "Instructions: Compose a comprehensive reply to the query using the search results given. "
        "Cite each reference using [ Page Number] notation (every result has this number at the beginning). "
        "Citation should be done at the end of each sentence. If the search results mention multiple subjects "
        "with the same name, create separate answers for each. Only include information found in the results and "
        "don't add any additional information. Make sure the answer is correct and don't output false content. "
        "If the text does not relate to the query, simply state 'Text Not Found in PDF'. Ignore outlier "
        "search results which has nothing to do with the question. Only answer what is asked. The "
        "answer should be short and concise. Answer step-by-step. \n\nQuery: {question}\nAnswer: "
    )

    return prompt


def generate_text(ai, prompt, max_tokens=4096, temperature=0.7):
    """
    Generate text based on the given prompt using the PySparkAI.

    :param ai: Instance of the PySparkAI.
    :param prompt: The prompt for generating the text.
    :param max_tokens: Maximum number of tokens to generate.
    :param temperature: Temperature parameter for generation.
    :return: Generated text.
    """
    try:
        messages = [{"content": prompt, "role": "user"}]
        completion = ai.chat(
            messages, temperature=temperature, max_tokens=max_tokens)
        message = completion['choices'][0]['message']
    except Exception as e:
        message = f'API Error: {str(e)}'
    return message


def generate_answer(question, ai, recommender):
    """
    Generate an answer to the given question using the semantic search and PySparkAI.

    :param question: The question to answer.
    :param ai: Instance of the PySparkAI.
    :param recommender: Instance of the SemanticSearch.
    :return: Generated answer.
    """
    topn_chunks = recommender.search(question)
    prompt = generate_prompt(question, topn_chunks)
    answer = generate_text(ai, prompt)
    return answer