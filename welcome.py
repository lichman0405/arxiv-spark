# This module is used to print the welcome page.
# Author: Shibo, MiQroEra
# Version: v1.0


import art


def welcome_page():
    """
    The function is used to print the welcome page.
    :return: None
    """
    print(art.text2art("Welcome to PDF-SparkCHAT!"))
    print("--------A Demo of PDF-CHAT with SparkAI--------")
    print("Warning: Due to the limitation of LLMs, answers may not be accurate.")
    print("Hence, it is a just assistant but not a replacement of human experts.")
    print("Version Clarification: For my weak 'arxiv query design', searching by keywords may not find the right papers.")
    print("Please use the 'id_list' option to search for papers, and searching by keywords will be well-supported in the future.")
    print("\n")
    print("Author: Shibo, MiQroEra")
    print("Version: v1.0")
    print("\n")