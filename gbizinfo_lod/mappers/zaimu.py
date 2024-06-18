from rdflib import URIRef

from ..namespace import *
from . import Literal, _TripleMapType, bpo
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoZaimuMapper(GbizInfoKatsudoMapper):
    """財務情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/zaimu")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        s = HJ_DATA[row["ID-識別値"]]
        ss = HJ_EXT[row["キー情報"]]

        # 数量コレクション
        suryo_keys = [
            # 数値, 単位表記, 指標
            (
                "財務情報-売上高",
                "財務情報-売上高ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/売上高",
            ),
            (
                "財務情報-営業収益",
                "財務情報-営業収益ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/営業収益",
            ),
            (
                "財務情報-営業収入",
                "財務情報-営業収入ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/営業収入",
            ),
            (
                "財務情報-営業総収入",
                "財務情報-営業総収入ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/営業総収入",
            ),
            (
                "財務情報-経常収益",
                "財務情報-経常収益ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/経常収益",
            ),
            (
                "財務情報-正味収入保険料",
                "財務情報-正味収入保険料ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/正味収入保険料",
            ),
            (
                "財務情報-経常利益又は経常損失（△）",
                "財務情報-経常利益又は経常損失（△）ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/経常利益又は経常損失",
            ),
            (
                "財務情報-当期純利益又は当期純損失（△）",
                "財務情報-当期純利益又は当期純損失（△）ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/当期純利益又は当期純損失",
            ),
            (
                "資本金-数値",
                "財務情報-資本金ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/資本金",
            ),
            (
                "財務情報-純資産額",
                "財務情報-純資産額ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/純資産額",
            ),
            (
                "財務情報-総資産額",
                "財務情報-総資産額ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/総資産額",
            ),
            (
                "関連人員-人数",
                "財務情報-従業員数ユニット参照",
                "http://hojin-info.go.jp/code/財務情報/従業員数",
            ),
        ]

        triples = [
            (s, HJ.法人活動情報, ss),
            (ss, RDF.type, HJ.財務型),
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
                        (IC.種別, row["名称-種別"]),
                        (IC.表記, row["名称-表記"]),
                    ]
                ),
            ),
            # 4, 5
            (
                ss,
                IC.住所,
                bpo(
                    [
                        (RDF.type, HJ.住所型),
                        (IC.種別, row["住所-種別"]),
                        (IC.表記, row["住所-表記"]),
                    ]
                ),
            ),
            # 6, 7, 8
            (
                ss,
                IC.代表者,
                bpo(
                    [
                        (RDF.type, IC.構成員型),
                        (IC.役割, row["代表者-役割"]),
                        (
                            IC.構成員,
                            bpo(
                                [
                                    (RDF.type, IC.人型),
                                    (
                                        IC.氏名,
                                        bpo(
                                            [
                                                (RDF.type, IC.氏名型),
                                                (IC.種別, row["代表者-表示用種別"]),
                                                (IC.姓名, row["代表者-表示用氏名"]),
                                            ]
                                        ),
                                    ),
                                    (
                                        IC.氏名,
                                        bpo(
                                            [
                                                (RDF.type, IC.氏名型),
                                                (IC.種別, row["代表者-検索用種別"]),
                                                (IC.姓名, row["代表者-検索用氏名"]),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 9, 10, 11
            (
                ss,
                IC.資本金,
                bpo(
                    [
                        (RDF.type, IC.金額型),
                        (IC.数値, Literal(row["資本金-数値"], datatype=XSD.decimal)),
                        (IC.通貨, row["資本金-通貨"]),
                        (
                            IC.通貨コード,
                            Literal(
                                row["資本金-通貨コード"],
                                datatype=ISO4217.ISO3AlphaCurrencyCodeContentType,
                            ),
                        ),
                    ]
                ),
            ),
            # 12
            (
                ss,
                IC.関連人員,
                bpo(
                    [
                        (RDF.type, IC.人数型),
                        (
                            IC.人数,
                            Literal(
                                row["関連人員-人数"], datatype=XSD.nonNegativeInteger
                            ),
                        ),
                    ]
                ),
            ),
            # 13
            (
                ss,
                HJ.更新日時,
                bpo(
                    [
                        (RDF.type, IC.日時型),
                        (
                            IC.標準型日時,
                            Literal(
                                row["更新日時"],
                                datatype=XSD.dateTime,
                            ),
                        ),
                    ]
                ),
            ),
            # 14, 15, 16, 17
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
                                                            (RDF.type, IC.組織型),
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
                                [
                                    (RDF.type, IC.名称型),
                                    (IC.表記, row["公表組織-名称表記"]),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 18
            (
                ss,
                HJ.システム名,
                bpo([(RDF.type, IC.名称型), (IC.表記, row["システム名"])]),
            ),
            # 19
            (ss, HJ.キー情報, row["キー情報"]),
            # 20
            (ss, HJ.回次, row["財務情報-回次"]),
            # 21, 22, 23
            *[
                (
                    ss,
                    HJ.株主情報,
                    bpo(
                        [
                            (RDF.type, HJ.株主情報型),
                            (
                                HJ.順位,
                                Literal(row[f"株主情報{i}-順位"], datatype=XSD.decimal),
                            ),
                            (IC.表記, row[f"株主情報{i}-氏名又は名称"]),
                            (
                                HJ.所有比率,
                                Literal(
                                    row[
                                        f"株主情報{i}-発行済株式総数に対する所有株式数の割合"
                                    ],
                                    datatype=XSD.decimal,
                                ),
                            ),
                        ]
                    ),
                )
                for i in range(1, 16)
            ],
            # 24, 25, 26
            *[
                (
                    ss,
                    HJ.数量コレクション,
                    bpo(
                        [
                            (RDF.type, HJ.数量コレクション型),
                            (
                                HJ.数量,
                                bpo(
                                    [
                                        (RDF.type, HJ.数量型),
                                        (
                                            IC.数値,
                                            Literal(
                                                row[value],
                                                datatype=XSD.decimal,
                                            ),
                                        ),
                                        (
                                            HJ.指標,
                                            (
                                                Literal(
                                                    indicator,
                                                    datatype=IC.コード型,
                                                )
                                                if row[value]
                                                else None
                                            ),
                                        ),
                                        (IC.単位表記, row[unit]),
                                    ]
                                ),
                            ),
                        ]
                    ),
                )
                for value, unit, indicator in suryo_keys
            ],
            # 27, 28, 29, 30, 31, 32
            (
                ss,
                HJ.書類情報,
                bpo(
                    [
                        (RDF.type, IC.文書型),
                        (IC.ID, row["書類情報-書類管理番号"]),
                        (
                            IC.種別コード,
                            bpo(
                                [
                                    (RDF.type, IC.コード型),
                                    (IC.識別値, row["書類情報-書類種別コード"]),
                                ]
                            ),
                        ),
                        (
                            IC.日付,
                            bpo(
                                [
                                    (RDF.type, IC.日付型),
                                    (IC.標準型日付, row["書類情報-提出日"]),
                                    (
                                        IC.種別,
                                        "提出日" if row["書類情報-提出日"] else None,
                                    ),
                                ]
                            ),
                        ),
                        (
                            IC.記述,
                            bpo(
                                [
                                    (RDF.type, IC.記述型),
                                    (IC.説明, row["書類情報-事業年度"]),
                                    (
                                        IC.種別,
                                        (
                                            "事業年度"
                                            if row["書類情報-事業年度"]
                                            else None
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ]
        return triples


__all__ = ["GbizInfoZaimuMapper"]
