# Description: This file contains the class used to parse the results returned from the ArxivAPI query.
# Author: Shibo Li, MiQroEra Inc.
# Date: 2023-09-02
# Version: 1.0

import os
import urllib.request
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArxivResultParser:
    """
    This class is used to parse the results returned from the ArxivAPI query.
    """

    def __init__(self, result):
        """
        Initialize with a result object.
        :param result: A result object from arxiv API query.
        """
        self.result = result

    def get_entry_id(self):
        """Returns the entry ID of the result."""
        return self.result.entry_id

    def get_updated(self):
        """Returns the last updated time of the result."""
        return str(self.result.updated)

    def get_published(self):
        """Returns the published time of the result."""
        return str(self.result.published)

    def get_title(self):
        """Returns the title of the result."""
        return self.result.title

    def get_authors(self):
        """Returns the authors of the result as a list of names."""
        authors_names = [author.name for author in self.result.authors]
        return authors_names

    def get_summary(self):
        """Returns the summary of the result."""
        return self.result.summary

    def get_comment(self):
        """Returns the comment of the result."""
        return self.result.comment

    def get_journal_ref(self):
        """Returns the journal reference of the result."""
        return self.result.journal_ref

    def get_doi(self):
        """Returns the DOI of the result."""
        return self.result.doi

    def get_primary_category(self):
        """Returns the primary category of the result."""
        return self.result.primary_category

    def get_categories(self):
        """Returns all the categories of the result."""
        return self.result.categories

    def get_links(self):
        """Returns the links associated with the result."""
        return str(self.result.links)

    def get_pdf_url(self):
        """Returns the PDF URL of the result."""
        return self.result.pdf_url

    def download_pdf(self, url, output_path):
        """
        Download a PDF file from a URL.
        :param url: The URL of the PDF file.
        :param output_path: The path to save the downloaded PDF file.
        :return: None
        """
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            file_path = os.path.join(output_path, url.split('/')[-1]) + '.pdf'
            urllib.request.urlretrieve(url, file_path)
            print("PDF file downloaded successfully!"
                  f"File saved at {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"An error occurred while downloading the PDF: {e}")
            return None