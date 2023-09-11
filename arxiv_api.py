# Description: This file contains the ArxivAPI class which is used to query the arXiv API.
# Author: Shibo Li, MiQroEra Inc.
# Date: 2023-09-02
# Version: 1.0

import arxiv
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArxivAPI:
    """
    This class is used to query the arXiv API.
    """

    def __init__(self):
        self.client = arxiv.Client(
            page_size=100, delay_seconds=3, num_retries=3)

    def query_by_id_list(self, id_list, max_results=1):
        """
        Query arXiv by id list.
        :param id_list: List of IDs to query.
        :param max_results: Maximum number of results.
        :return: A list of arXiv results.
        """
        if isinstance(id_list, str):
            id_list = [id_list]
        return self.execute_query(None, max_results, id_list=id_list)

    def combined_query(self, queries_dict, max_results=1):
        """
        Query arXiv by combining multiple queries.
        :param queries_dict: A dictionary of queries.
        :param max_results: Maximum number of results.
        :return: A list of arXiv results.
        """
        query = " AND ".join(
            [f"{key}:{value}" for key, value in queries_dict.items()])
        return self.execute_query(query, max_results)

    def execute_query(self, query, max_results, id_list=None):
        """
        Execute the query.
        :param query: Query string.
        :param max_results: Maximum number of results.
        :param id_list: A list of arXiv IDs for querying by ID list (optional).
        :return: A list of arXiv results.
        """
        try:
            if id_list is not None:
                search = arxiv.Search(
                    id_list=id_list,
                    max_results=max_results,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
            else:
                search = arxiv.Search(
                    query=query,
                    max_results=max_results,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
            results = [item for item in search.results()]
            return results
        except Exception as e:
            logger.error(f"An error occurred while executing the query: {e}")
            return []