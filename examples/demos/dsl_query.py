# * coding:utf-8 *
from pprint import pprint

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import (
    Match,
    MatchAll,
    MoreLikeThis,
    MultiMatch,
    Q,
    Range,
)

from examples.prepare.client import Client
from examples.utils import boundary


class DslQuery(object):
    def __init__(self):
        self.client = Client().client

    def print_(self, t):
        """
        Common tools for print query result
        :param t:
        :return:
        """
        if t.get("hits", {}).get("total", {}).get("value", None):
            hits = t["hits"]["hits"]
            for hit in hits:
                pprint(hit.get("_source"))

    @boundary
    def find_all(self):
        s = Search(using=self.client, index="book-index").execute()
        pprint(s.to_dict())

    @boundary
    def match_by_q(self):
        q = Q("multi_match", query="python", fields=["title", "author"])
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "author"]).execute()
        self.print_(s.to_dict())

    @boundary
    def fuzzy_match_by_q(self):
        q = Q(
            "multi_match", query="pjthen", fields=["title", "author"], fuzziness="auto"
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "author"]).execute()
        self.print_(s.to_dict())

    @boundary
    def match_all(self):
        s = Search(using=self.client, index="book-index")
        r = MatchAll()
        s = s.query(r).source(["title", "publish_date"]).execute()
        self.print_(s.to_dict())

    @boundary
    def match(self):
        m = Match(title={"query": "python"})
        s = (
            Search(using=self.client, index="book-index")
            .query(m)
            .source(includes=["a*", "title"], excludes=["p*"])
            .execute()
        )
        self.print_(s.to_dict())

    @boundary
    def multi_math(self):
        m = MultiMatch(query="python", fields=["title", "author"])
        s = (
            Search(using=self.client, index="book-index")
            .query(m)
            .source(["title", "author"])
            .execute()
        )
        self.print_(s.to_dict())

    @boundary
    def range(self):
        s = Search(using=self.client, index="book-index")
        r = Range(publish_date={"gte": "2015-01-01", "lte": "2020-12-31"})
        s = s.query(r).source(["title", "publish_date", "abstract"]).execute()
        self.print_(s.to_dict())

    @boundary
    def more_like_this(self):
        s = Search(using=self.client, index="book-index")
        r = MoreLikeThis(
            like="where are my",
            fields=[
                "abstract",
            ],
        )
        s = s.query(r).source(["title", "abstract"]).execute()
        self.print_(s.to_dict())

    @boundary
    def bool_query(self):
        q = Q("match", title="python") | Q("match", title="java")
        q = q & Q("match", author="guido")
        q = ~Q("match", author="gosling") & q
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "author"]).execute()
        self.print_(s.to_dict())


    def filter_query(self):

        @boundary
        def range_query():
            s = Search(using=self.client, index="book-index")
            s = s.filter("range", publish_date={"gte": "2015-01-01", "lte": "2020-12-31"})
            s = s.source(["title", "publish_date", "comments", "fans"])
            s = s.execute()
            self.print_(s.to_dict())

        @boundary
        def exact_query():
            s = Search(using=self.client, index="book-index")
            s = s.filter("term", publication="wiley")
            s = s.source(["title", "publication"])
            s = s.execute()
            self.print_(s.to_dict())

        range_query()
        exact_query()

    @boundary
    def sort_and_pagination(self):
        s = Search(using=self.client, index="book-index")
        s = s.filter("range", publish_date={"gte": "2015-01-01", "lte": "2020-12-31"})
        s = s.source(["title", "publish_date", "comments", "fans"])
        s = s.sort("comments", "-fans")
        s = s[3:6]
        s = s.execute()
        self.print_(s.to_dict())

    @boundary
    def function_socre_field_value_factor(self):
        q = Q(
            "function_score",
            query=Q(
                "multi_match",
                query="guido",
                fields=["title", "author"],
                fuzziness="auto",
            ),
            field_value_factor={
                "field": "fans",
                "modifier": "log1p",
                "factor": 3,
                "missing": 1,
            },
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "fans", "author"]).execute()
        self.print_(s.to_dict())

    @boundary
    def function_score_painless_script_score(self):
        q = Q(
            "function_score",
            query=Q("multi_match", query="python", fields=["title", "author"]),
            boost_mode="replace",
            script_score={
                "script": {
                    "lang": "painless",
                    "params": {"x": 1, "y": 2},
                    "source": '_score + params.y * doc["fans"].value + params.x',
                }
            },
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "fans", "author"]).execute()
        self.print_(s.to_dict())

    @boundary
    def fucntion_score_random_score(self):
        q = Q(
            "function_score",
            query=Q("multi_match", query="python", fields=["title", "author"]),
            boost_mode="replace",
            random_score={"seed": 1, "field": "fans"},
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "fans", "author"]).execute()
        self.print_(s.to_dict())

    @boundary
    def function_score_function(self):
        q = Q(
            "function_score",
            query=Q("multi_match", query="python", fields=["title", "author"]),
            functions=[
                {"filter": {"term": {"publication": "harpercollins"}}, "weight": 10},
                {"filter": {"term": {"publication": "scholastic"}}, "weight": 20},
            ],
            boost=2,
            score_mode="max",
            boost_mode="replace",
            min_score=10,
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "author", "publication"]).execute()
        self.print_(s.to_dict())

    @boundary
    def fucntion_score_decay_function(self):
        q = Q(
            "function_score",
            query=Q("multi_match", query="python", fields=["title", "author"]),
            boost_mode="replace",
            functions=[
                {
                    "exp": {
                        "publish_date": {
                            "origin": "2018-09-15",
                            "offset": "15d",
                            "scale": "15d",
                            "decay": "0.3",
                        }
                    }
                }
            ],
        )
        s = Search(using=self.client, index="book-index")
        s = s.query(q).source(["title", "author", "publish_date"]).execute()
        self.print_(s.to_dict())


if __name__ == "__main__":
    d = DslQuery()
