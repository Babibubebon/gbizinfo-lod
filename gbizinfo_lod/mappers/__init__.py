import csv
import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import IO, Iterator, Tuple, Union

from joblib import Parallel, delayed
from rdflib import BNode
from rdflib import Literal as LiteralRdflib
from rdflib import URIRef
from rdflib.graph import _ObjectType, _PredicateType, _SubjectType, _TripleType
from rdflib.namespace import RDF
from rdflib.plugins.serializers.nquads import _nq_row
from rdflib.plugins.serializers.nt import _nt_row

_TripleMapType = Tuple[
    _SubjectType, _PredicateType, Union[str, _ObjectType, "BlankPredicateObjectMap"]
]
_PredicateObjectType = Tuple[
    _PredicateType, Union[str, _ObjectType, "BlankPredicateObjectMap"]
]
RDFFormatType = Enum("RDFFormatType", ["nt", "nq"])


class Literal:
    def __new__(cls, value, *args, **kwargs) -> LiteralRdflib | None:
        if value is None:
            return None
        return LiteralRdflib(value, *args, **kwargs)


class BlankPredicateObjectMap:
    def __init__(self, predicate_objects: list[_PredicateObjectType]):
        self.subject = BNode()
        self.predicate_objects = predicate_objects


def bpo(predicate_objects: list[_PredicateObjectType]) -> BlankPredicateObjectMap:
    return BlankPredicateObjectMap(predicate_objects)


def normalize_triple(triple: _TripleType) -> _TripleMapType | None:
    if triple[2] is None:
        return None
    if isinstance(triple[2], Literal) and triple[2] is None:
        return None
    if type(triple[2]) is str:
        triple = (triple[0], triple[1], Literal(triple[2]))
    return triple


def flatten_triple_map(triple_map: _TripleMapType) -> list[_TripleType]:
    triples = []

    if isinstance(triple_map[2], BlankPredicateObjectMap):
        bnode = triple_map[2].subject
        b_triples = []
        for po in triple_map[2].predicate_objects:
            b_triples.extend(flatten_triple_map((bnode, po[0], po[1])))

        # Ignore statements if rdf:type only
        if len([t for t in b_triples if t[1] != RDF.type]) > 0:
            triples.append((triple_map[0], triple_map[1], bnode))
            triples.extend(b_triples)
    else:
        t = normalize_triple(triple_map)
        if t:
            triples.append(t)

    return triples


def serialize_triple(triple: _TripleMapType, graph: URIRef | None = None) -> str:
    return _nq_row(triple, graph) if graph else _nt_row(triple)


class CSV2RDFMapper(ABC):
    def __init__(self, csv_file: str):
        self.file = csv_file

    def iterator(self) -> Iterator[dict[str, str]]:
        with open(self.file, encoding="utf_8_sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def run(
        self,
        n_jobs: int = -1,
        output: IO[str] = sys.stdout,
        format: RDFFormatType = RDFFormatType.nq,
    ):
        def job(row: dict[str, str]) -> str:
            return "".join(
                [
                    serialize_triple(
                        triple,
                        graph=self.graph if format == RDFFormatType.nq else None,
                    )
                    for triple_map in self.map_to_triples(self.preprocess(row))
                    for triple in flatten_triple_map(triple_map)
                ]
            )

        res = Parallel(n_jobs=n_jobs, return_as="generator_unordered", verbose=1)(
            delayed(job)(row) for row in self.iterator()
        )
        for lines in res:
            output.write(lines)

    @staticmethod
    def preprocess(row: dict[str, str]) -> dict[str, str | None]:
        return {key: val if val != "" else None for key, val in row.items()}

    @property
    @abstractmethod
    def graph(self) -> URIRef:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        raise NotImplementedError


from .chotatsu import GbizInfoChotatsuMapper
from .hojin import GbizInfoHojinMapper
from .hojyokin import GbizInfoHojyokinMapper
from .hyosho import GbizInfoHyoshoMapper
from .shokuba import GbizInfoShokubaMapper
from .todokede import GbizInfoTodokedeMapper
from .tokkyo import GbizInfoTokkyoMapper
from .zaimu import GbizInfoZaimuMapper

__all__ = [
    "RDFFormatType",
    "GbizInfoHojinMapper",
    "GbizInfoHojyokinMapper",
    "GbizInfoChotatsuMapper",
    "GbizInfoHyoshoMapper",
    "GbizInfoTodokedeMapper",
    "GbizInfoTokkyoMapper",
    "GbizInfoShokubaMapper",
    "GbizInfoZaimuMapper",
]
