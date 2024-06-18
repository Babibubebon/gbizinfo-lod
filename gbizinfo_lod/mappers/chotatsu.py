from rdflib import URIRef

from ..namespace import *
from . import _TripleMapType
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoChotatsuMapper(GbizInfoKatsudoMapper):
    """調達情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/chotatsu")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = GbizInfoKatsudoMapper.map_to_triples(row)
        triples.extend(
            [
                (ss, RDF.type, HJ.調達型),
            ]
        )
        return triples


__all__ = ["GbizInfoChotatsuMapper"]
