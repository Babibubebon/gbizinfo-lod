from rdflib import URIRef

from ..namespace import *
from . import _TripleMapType
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoHyoshoMapper(GbizInfoKatsudoMapper):
    """表彰情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/hyosho")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = GbizInfoKatsudoMapper.map_to_triples(row)
        triples.extend(
            [
                (ss, RDF.type, HJ.表彰型),
            ]
        )
        return triples


__all__ = ["GbizInfoHyoshoMapper"]
