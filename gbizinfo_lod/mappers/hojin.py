from rdflib import URIRef

from ..namespace import *
from . import CSV2RDFMapper, Literal, _TripleMapType, bpo


class GbizInfoHojinMapper(CSV2RDFMapper):
    """法人情報・法人基本情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/hojin")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        s = HJ_DATA[row["ID-識別値"]]
        ss = HJ_BASIC[row["ID-識別値"]]

        triples = [
            (s, HJ.法人基本情報, ss),
            (s, RDF.type, HJ.法人情報型),
            (ss, RDF.type, HJ.法人基本情報型),
            # 1
            (
                ss,
                IC.ID,
                bpo(
                    [
                        (RDF.type, IC.ID型),
                        (IC.体系, IC_ID.corporateNumber),
                        (IC.識別値, row["ID-識別値"]),
                    ]
                ),
            ),
            # 2, 3
            (
                ss,
                IC.名称,
                bpo(
                    [
                        (RDF.type, IC.名称型),
                        (IC.種別, row["名称[日本語表記]-種別"]),
                        (IC.表記, row["名称[日本語表記]-表記"]),
                        (IC.カナ表記, row["名称[日本語表記]-カナ表記"]),
                    ]
                ),
            ),
            # 2, 3
            (
                ss,
                IC.名称,
                bpo(
                    [
                        (RDF.type, IC.名称型),
                        (IC.種別, row["名称[英語表記]-種別"]),
                        (IC.表記, row["名称[英語表記]-表記"]),
                        (IC.カナ表記, row["名称[英語表記]-カナ表記"]),
                    ]
                ),
            ),
            # 4, 5
            (
                ss,
                IC.活動状況,
                bpo(
                    [
                        (RDF.type, IC.状況型),
                        (
                            IC.発生日,
                            bpo(
                                [
                                    (RDF.type, IC.日時型),
                                    (
                                        IC.標準型日時,
                                        Literal(
                                            row["活動状況-発生日"],
                                            datatype=XSD.dateTime,
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        (IC.説明, row["活動状況-説明"]),
                    ]
                ),
            ),
            # 6, 7, 8, 9, 10, 11, 12, 13
            (
                ss,
                IC.住所,
                bpo(
                    [
                        (RDF.type, HJ.住所型),
                        (IC.種別, row["住所[日本語表記]-種別"]),
                        (IC.表記, row["住所[日本語表記]-表記"]),
                        (IC.郵便番号, row["住所[日本語表記]-郵便番号"]),
                        (IC.都道府県, row["住所[日本語表記]-都道府県"]),
                        (
                            IC.都道府県コード,
                            URIRef(
                                f"http://imi.go.jp/ns/code_id/code/jisx0401#{row['住所[日本語表記]-都道府県コード']}"
                            ),
                        ),
                        (IC.市区町村, row["住所[日本語表記]-市区町村"]),
                        (
                            IC.市区町村コード,
                            URIRef(
                                f"http://imi.go.jp/ns/code_id/code/jisx0402#{row['住所[日本語表記]-市区町村コード']}"
                            ),
                        ),
                        (HJ.町名番地等, row["住所[日本語表記]-町名番地等"]),
                    ]
                ),
            ),
            # 6, 7, 8, 9, 10, 11, 12, 13, 14
            (
                ss,
                IC.住所,
                bpo(
                    [
                        (RDF.type, HJ.住所型),
                        (IC.種別, row["住所[英語表記]-種別"]),
                        (IC.表記, row["住所[英語表記]-表記"]),
                        (IC.郵便番号, row["住所[英語表記]-郵便番号"]),
                        (IC.都道府県, row["住所[英語表記]-都道府県"]),
                        (
                            IC.都道府県コード,
                            URIRef(
                                f"http://imi.go.jp/ns/code_id/code/jisx0401#{row['住所[英語表記]-都道府県コード']}"
                            ),
                        ),
                        (IC.市区町村, row["住所[英語表記]-市区町村"]),
                        (
                            IC.市区町村コード,
                            URIRef(
                                f"http://imi.go.jp/ns/code_id/code/jisx0402#{row['住所[英語表記]-市区町村コード']}"
                            ),
                        ),
                        (HJ.町名番地等, row["住所[英語表記]-町名番地等"]),
                        (
                            HJ.市区町村町名番地等,
                            row["住所[英語表記]-市区町村町名番地以下"],
                        ),
                    ]
                ),
            ),
            # 15
            (
                ss,
                IC.組織種別,
                URIRef(f"http://imi.go.jp/ns/code_id/code/kind#{row['組織種別']}"),
            ),
            # 16
            (
                ss,
                HJ.更新日時,
                bpo(
                    [
                        (RDF.type, IC.日時型),
                        (
                            IC.標準型日時,
                            Literal(
                                (
                                    f"{row["更新日時"]}T00:00:00"
                                    if row["更新日時"]
                                    else None
                                ),
                                datatype=XSD.dateTime,
                            ),
                        ),
                    ]
                ),
            ),
            # 17, 18, 19, 20
            (
                ss,
                HJ.公表組織,
                bpo(
                    [
                        (RDF.type, IC.組織型),
                        (
                            IC.ID,
                            bpo(
                                [
                                    (RDF.type, IC.ID型),
                                    (
                                        IC.体系,
                                        bpo(
                                            [
                                                (RDF.type, IC.ID体系型),
                                                (
                                                    IC.名称,
                                                    bpo(
                                                        [
                                                            (RDF.type, IC.名称型),
                                                            (
                                                                IC.表記,
                                                                row["公表組織-ID名称"],
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                                (
                                                    IC.発行者,
                                                    bpo(
                                                        [
                                                            (RDF.type, IC.実体型),
                                                            (
                                                                IC.名称,
                                                                bpo(
                                                                    [
                                                                        (
                                                                            RDF.type,
                                                                            IC.名称型,
                                                                        ),
                                                                        (
                                                                            IC.表記,
                                                                            row[
                                                                                "公表組織-ID発行者"
                                                                            ],
                                                                        ),
                                                                    ]
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ),
                                    (IC.識別値, row["公表組織-ID識別値"]),
                                ]
                            ),
                        ),
                        (
                            IC.名称,
                            bpo(
                                [(RDF.type, IC.名称型), (IC.表記, row["公表組織-名称"])]
                            ),
                        ),
                    ]
                ),
            ),
            # 21, 22
            (
                ss,
                HJ.区分,
                bpo(
                    [
                        (IC.種別, row["区分-処理種別"]),
                        (IC.表記, row["区分-処理表記"]),
                    ]
                ),
            ),
            # 21, 22
            (
                ss,
                HJ.区分,
                bpo(
                    [
                        (IC.種別, row["区分-訂正種別"]),
                        (IC.表記, row["区分-訂正表記"]),
                    ]
                ),
            ),
            # 21, 22
            (
                ss,
                HJ.区分,
                bpo(
                    [
                        (IC.種別, row["区分-最新種別"]),
                        (IC.表記, row["区分-最新表記"]),
                    ]
                ),
            ),
            # 21, 22
            (
                ss,
                HJ.区分,
                bpo(
                    [
                        (IC.種別, row["区分-過去種別"]),
                        (IC.表記, row["区分-過去表記"]),
                    ]
                ),
            ),
        ]
        return triples


__all__ = ["GbizInfoHojinMapper"]
