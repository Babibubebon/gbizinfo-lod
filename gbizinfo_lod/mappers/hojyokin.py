from rdflib import URIRef

from ..namespace import *
from . import Literal, _TripleMapType, bpo
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoHojyokinMapper(GbizInfoKatsudoMapper):
    """補助金情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/hojyokin")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = GbizInfoKatsudoMapper.map_to_triples(row)
        triples.extend(
            [
                (ss, RDF.type, HJ.補助金型),
                # 49
                (
                    ss,
                    HJ.採択日,
                    bpo(
                        [
                            (RDF.type, IC.日付型),
                            (
                                IC.標準型日付,
                                Literal(row["補助金-採択日"], datatype=XSD.date),
                            ),
                        ]
                    ),
                ),
                # 50
                (
                    ss,
                    HJ.交付決定日,
                    bpo(
                        [
                            (RDF.type, IC.日付型),
                            (
                                IC.標準型日付,
                                Literal(row["補助金-交付決定日"], datatype=XSD.date),
                            ),
                        ]
                    ),
                ),
                # 51
                (ss, HJ.補助金財源, row["補助金-財源"]),
            ]
        )
        return triples


__all__ = ["GbizInfoHojyokinMapper"]
