import re
import requests
import difflib
import collections
import collections.abc
from urllib.parse import quote
from lxml import etree
from bs4 import BeautifulSoup as bSoup
import logging

if not hasattr(collections, "Callable"):
    collections.Callable = collections.abc.Callable

class Recon:

    def __init__(self, score):
        """Turns the raw lists of scores and term-id pairs into objects"""
        self.score = score[0]
        self.header = score[1][0]
        self.uri = score[1][1]
        self.id = self.uri.split("/")[-1]

    def __str__(self):
        return str(self.header) + " (" + str(self.score) + ")"

    @staticmethod
    def reconcile(original, term_pairs, sort=False, limit=20):
        """appends a reconciliation score to each term-identifier pair"""
        recon_scores = []
        for tp in term_pairs:
            # NOTE: assumes 0th element of tuple == term
            term = tp[0].lower().replace("&amp;", "&")
            if term.endswith("."):
                term = term[:-1]
            sim_ratio = str(round(float(difflib.SequenceMatcher(
                None, original.lower(), term).ratio()), 3))
            recon_scores.append([sim_ratio, tp])
        if sort:
            return sorted(recon_scores,
                          key=lambda x: x[0],
                          reverse=True)[:limit]
        return recon_scores[:limit]


class SearchLoC:

    logging.basicConfig(level=logging.INFO)
    LOGGER = logging.getLogger(__name__)

    def __init__(self, term, term_type=''):
        self._term_type = term_type
        self.term = term
        self.suggest_uri = "https://id.loc.gov/authorities" + self.term_type + "/suggest/?q="
        self.__raw_uri_start = "https://id.loc.gov/search/?q="
        self.__raw_uri_end = "&q=cs%3Ahttps%3A%2F%2Fid.loc.gov%2Fauthorities%2F" + self.term_type[1:]

    def __str__(self):
        return str(self.search_terms())

    @property
    def _term_type(self):
        return self.term_type

    @_term_type.setter
    def _term_type(self, val):
        valid = ['', 'all', 'names', '/names', 'subjects', '/subjects']
        if val in valid:
            if val == 'all' or val == '':
                self.term_type = ''
            else:
                if not val.startswith('/'):
                    self.term_type = '/' + val
                else:
                    self.term_type = val
        else:
            self.term_type = ''

    def search_terms(self):
        """Looks for a term using the suggest API"""
        self.LOGGER.debug("HTTPS request on Suggest API for {}".format(self.term))
        response = requests.get(self.suggest_uri + quote(self.term))
        result = response.json()
        return self.__process_results(result)
        
    def search_terms_v2(self):
        """Search LoC Suggest Service 2.0."""
        suggest2_uri = (
            "https://id.loc.gov/authorities"
            + self.term_type
            + "/suggest2?q="
            + quote(self.term)
            + "&count=25"
        )

        self.LOGGER.debug(
            "HTTP request on Suggest 2 API for %s",
            self.term
        )

        try:
            response = requests.get(suggest2_uri, timeout=15)
            response.raise_for_status()
            result = response.json()
        except (requests.RequestException, ValueError) as error:
            self.LOGGER.warning(
                "Suggest 2 failed for %s: %s",
                self.term,
                error
            )
            return []

        id_pairs = []

        for hit in result.get("hits", []):
            term_name = hit.get("suggestLabel")
            term_uri = hit.get("uri")

            if term_name and term_uri:
                id_pairs.append((term_name, term_uri))

        return id_pairs

    @staticmethod
    def __process_results(results):
        """parse web results into term-id pairs"""
        id_pairs = []
        for i, _ in enumerate(results[1]):
            term_name = results[1][i]
            term_id = results[3][i]
            if term_id and term_name:
                id_pairs.append((term_name, term_id))
        return id_pairs

    def did_you_mean(self):
        dym_base = "https://id.loc.gov/authorities" + self.term_type + "/didyoumean/?label="
        dym_url = dym_base + quote(self.term)
        self.LOGGER.debug("querying didyoumean with URL {}".format(str(dym_url)))

        try:
            response = requests.get(dym_url, timeout=15)
            response.raise_for_status()
            tree = etree.fromstring(response.content)
        except (requests.RequestException, etree.XMLSyntaxError) as error:
            self.LOGGER.warning(
                "didyoumean failed for %s: %s",
                self.term,
                error
            )
            return []

        return [
            (child.text, child.attrib.get("uri"))
            for child in iter(tree)
            if child.attrib.get("uri")
        ]

    def search_terms_raw(self):
        """Switches to looking for a term by scraping the first web page of search results"""
        self.LOGGER.debug("Web scraping page 1 of web results...".format(self.term))
        search_uri = self.__raw_uri_start + quote(self.term) + self.__raw_uri_end
        response = requests.get(search_uri)
        parser = bSoup(response.text, 'html.parser')
        pattern = re.compile("<td><a href=\"/authorities" + self.term_type + ".+</a></td>")
        search_results = re.findall(pattern, str(parser))
        return self.__process_results_raw(search_results)

    def __process_results_raw(self, results):
        id_pairs = []
        for r in results:
            heading = re.search("\">(.+)</a></td>", r).group(1)
            term_id = re.search("<td><a href=\"/authorities" + self.term_type + "/(.+)\">", r).group(1)
            term_id = self.get_term_uri(term_id)
            if term_id and heading:
                id_pairs.append((heading, term_id))
        return id_pairs

    def full_search(self, suggest=True, didyoumean=True, scrape=True):
        """Run all enabled search methods, combine results, and remove duplicates."""
        combined_results = []
        seen_uris = set()

        suggest2_results = self.search_terms_v2() if suggest else []
        suggest_results = self.search_terms() if suggest else []
        didyoumean_results = self.did_you_mean() if didyoumean else []
        scrape_results = self.search_terms_raw() if scrape else []

        def add_results(results):
            if not results:
                return

            for term_name, term_uri in results:
                if not term_uri:
                    continue

                normalized_uri = term_uri.replace(
                    "https://id.loc.gov/",
                    "http://id.loc.gov/",
                    1
                )

                if normalized_uri not in seen_uris:
                    combined_results.append((term_name, term_uri))
                    seen_uris.add(normalized_uri)

        add_results(suggest2_results)
        add_results(suggest_results)
        add_results(didyoumean_results)
        add_results(scrape_results)

        return combined_results

    def get_term_uri(self, term_id, extension="html", include_ext=False):
        """return the URI of a term, given its identifier."""
        term_uri = "https://id.loc.gov/authorities" + self.term_type + "/" + term_id
        if include_ext:
            return term_uri + "." + extension
        return term_uri


if __name__ == "__main__":
    # for testing
    term_in = input("search term: ")
    res = SearchLoC(term=term_in, term_type='/names').full_search()
    print(res)
    recon_ = Recon.reconcile(term_in, res, sort=True, limit=1)
    for ro in recon_:
        print(Recon(ro))
