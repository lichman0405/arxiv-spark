# Description: This file is main function of the application.
# Author: Shibo Li, MiQroEra Inc.
# Date: 2023-09-02
# Version: 1.0

from arxiv_api import ArxivAPI
from arxiv_result_parser import ArxivResultParser
from pdftotext import PDFTextExtractor
from pdf_semantic_search import SemanticSearch, get_credentials_from_user, generate_answer
from welcome import welcome_page
from pysparkai import PySparkAI
import os

class MainApplication:
    """
    This class is the main application of the project.
    """
    def __init__(self):
        """
        Constructor of the class.
        :param: None
        :return: None
        """
        self.arxiv_api = ArxivAPI()
        self.recommender = None
        self.credentials = None

    def transform_input(self, input_str):
        """
        Transform the input string into a dictionary.
        :param input_str: the input string
        :return: a dictionary
        """
        parts = input_str.split(", ")
        output = {}
        for part in parts:
            key, value = part.split(": ")
            output[key] = value
        return output

    def get_id_list_from_user(self):
        """
        Get the ID list from the user.
        :param: None
        :return: a list of IDs
        """
        print("Please input the Arxiv ID:")
        id_str = input()
        return [id_str]

    def start(self):
        """
        Start the application.
        :param: None
        :return: None
        """
        welcome_page()
        print("Would you like to query by keywords or by ID list? (type 'keywords' or 'id_list')")
        query_type = input().strip().lower()

        if query_type == 'keywords':
            query = self.transform_input(input("Please input your query: "))
            max_results = int(input("Please input the maximum number of results: "))
            query_result = self.arxiv_api.combined_query(query, max_results=max_results)
        elif query_type == 'id_list':
            id_list = self.get_id_list_from_user()
            max_results = int(input("Please input the maximum number of results: "))
            query_result = self.arxiv_api.query_by_id_list(id_list, max_results=max_results)
        else:
            print("Invalid input. Please start over.")
            return

        for result in query_result:
            self.process_result(result)

    def process_result(self, result):
        """
        Process the result.
        :param result: the result
        :return: None
        """
        parser = ArxivResultParser(result)
        print("The paper you are looking for is:")
        print(f"Title: {parser.get_title()}")
        pdf_url = parser.get_pdf_url()
        print(f'PDF URL: {pdf_url}')
        
        output_path = "download/" + os.path.basename(pdf_url)
        print(f'Output path: {output_path}\n')

        if not os.path.exists(output_path):
            output_path = parser.download_pdf(pdf_url, "download/")
            print(f"Downloaded PDF file to {output_path}.\n")
        else:
            print(f"File {output_path} already exists, skipping download.\n")

        if not self.credentials:
            self.credentials = get_credentials_from_user()
        
        ai = PySparkAI(
            app_id=self.credentials[0], 
            api_key=self.credentials[1],
            api_secret=self.credentials[2], 
            spark_url=self.credentials[3], 
            domain=self.credentials[4]
        )
        self.recommender = SemanticSearch()

        extractor = PDFTextExtractor(output_path)
        texts = extractor.pdf_to_text()
        chunks = extractor.text_to_chunks(texts)
        self.recommender.fit(chunks)

        self.start_conversation(ai)

    def start_conversation(self, ai):
        """
        Start the conversation.
        :param ai: the AI
        :return: None
        """
        while True:
            question = input("You can start to talk to Spark AI now. (type 'quit or exit' to finish the conversation)\n-----------------------------------\nPlease enter your question: ")
            if question.lower() in ['quit', 'exit']:
                break
            else:
                answer = generate_answer(question, ai, self.recommender)
                print(f"Answer: {answer}\n")

if __name__ == "__main__":
    app = MainApplication()
    app.start()