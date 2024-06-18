from rdflib import URIRef

from ..namespace import *
from . import _TripleMapType, bpo
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoTokkyoMapper(GbizInfoKatsudoMapper):
    """特許情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/tokkyo")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = GbizInfoKatsudoMapper.map_to_triples(row)
        triples.extend(
            [
                (ss, RDF.type, HJ.特許型),
                # 40
                (
                    ss,
                    HJ.認定番号,
                    bpo(
                        [
                            (RDF.type, IC.ID型),
                            (IC.識別値, row["法人活動-認定番号-識別値"]),
                        ]
                    ),
                ),
                # 41
                (
                    ss,
                    HJ.分類,
                    bpo(
                        [
                            (RDF.type, IC.表記),
                            (
                                IC.表記,
                                row["特許-分類1-表記"],
                            ),
                        ]
                    ),
                ),
                (
                    ss,
                    HJ.分類,
                    bpo(
                        [
                            (RDF.type, IC.表記),
                            (
                                IC.表記,
                                row["特許-分類2-表記"],
                            ),
                        ]
                    ),
                ),
            ]
        )
        return triples


__all__ = ["GbizInfoTokkyoMapper"]
