from rdflib import URIRef

from ..namespace import *
from . import Literal, _TripleMapType, bpo
from ._katsudo import GbizInfoKatsudoMapper


class GbizInfoShokubaMapper(GbizInfoKatsudoMapper):
    """職場情報"""

    @property
    def graph(self) -> URIRef:
        return URIRef("http://hojin-info.go.jp/graph/shokuba")

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        s = HJ_DATA[row["ID-識別値"]]
        ss = HJ_EXT[row["キー情報"]]

        # 数量コレクション
        suryo_keys = [
            # 数値, 単位表記, 指標, 種別
            (
                "職場情報-企業規模",
                "人",
                "http://hojin-info.go.jp/code/職場情報/企業規模",
                None,
            ),
            (
                "職場情報-企業規模詳細(男性)",
                "人",
                "http://hojin-info.go.jp/code/職場情報/企業規模詳細（男性）",
                None,
            ),
            (
                "職場情報-企業規模詳細(女性)",
                "人",
                "http://hojin-info.go.jp/code/職場情報/企業規模詳細（女性）",
                None,
            ),
            (
                "職場情報-平均継続勤務年数-男性",
                "年",
                "http://hojin-info.go.jp/code/職場情報/男性平均継続勤務年数",
                "職場情報-平均継続勤務年数-範囲",
            ),
            (
                "職場情報-平均継続勤務年数-女性",
                "年",
                "http://hojin-info.go.jp/code/職場情報/女性平均継続勤務年数",
                "職場情報-平均継続勤務年数-範囲",
            ),
            (
                "職場情報-正社員の平均継続勤務年数",
                "年",
                "http://hojin-info.go.jp/code/職場情報/正社員平均継続勤務年数",
                "職場情報-平均継続勤務年数-範囲",
            ),
            (
                "職場情報-従業員の平均年齢",
                "歳",
                "http://hojin-info.go.jp/code/職場情報/従業員平均年齢",
                None,
            ),
            (
                "職場情報-月平均所定外労働時間",
                "時間",
                "http://hojin-info.go.jp/code/職場情報/月平均所定外労働時間",
                None,
            ),
            (
                "職場情報-労働者に占める女性労働者の割合",
                "%",
                "http://hojin-info.go.jp/code/職場情報/女性労働者割合",
                "職場情報-労働者に占める女性労働者の割合-範囲",
            ),
            (
                "職場情報-女性管理職人数",
                "人",
                "http://hojin-info.go.jp/code/職場情報/女性管理職人数",
                None,
            ),
            (
                "職場情報-管理職全体人数（男女計）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/管理職人数",
                None,
            ),
            (
                "職場情報-女性役員人数",
                "人",
                "http://hojin-info.go.jp/code/職場情報/女性役員人数",
                None,
            ),
            (
                "職場情報-役員全体人数（男女計）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/役員人数",
                None,
            ),
            (
                "職場情報-育児休業対象者数（男性）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/育児休業対象者数（男性）",
                None,
            ),
            (
                "職場情報-育児休業対象者数（女性）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/育児休業対象者数（女性）",
                None,
            ),
            (
                "職場情報-育児休業取得者数（男性）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/育児休業取得者数（男性）",
                None,
            ),
            (
                "職場情報-育児休業取得者数（女性）",
                "人",
                "http://hojin-info.go.jp/code/職場情報/育児休業取得者数（女性）",
                None,
            ),
        ]

        triples = [
            (s, HJ.法人活動情報, ss),
            (ss, RDF.type, HJ.職場情報型),
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
            # 2
            (
                ss,
                IC.連絡先,
                bpo(
                    [
                        (RDF.type, IC.連絡先型),
                        (IC.Webサイト, row["連絡先-Webサイト"]),
                    ]
                ),
            ),
            # 3
            (
                ss,
                IC.代表者,
                bpo(
                    [
                        (RDF.type, IC.構成員型),
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
                                                (IC.姓名, row["代表者-表示用氏名"]),
                                            ]
                                        ),
                                    ),
                                    (
                                        IC.氏名,
                                        bpo(
                                            [
                                                (RDF.type, IC.氏名型),
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
            # 4
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
            # 5, 6, 7, 8
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
            # 9
            (
                ss,
                HJ.システム名,
                bpo([(RDF.type, IC.名称型), (IC.表記, row["システム名"])]),
            ),
            # 10
            (ss, HJ.キー情報, row["キー情報"]),
            # 11
            (
                ss,
                HJ.創業日,
                bpo(
                    [
                        (RDF.type, IC.日付型),
                        (
                            IC.年,
                            Literal(row["職場情報-創業年"], datatype=XSD.integer),
                        ),
                    ]
                ),
            ),
            # 12
            (ss, HJ.事業内容, row["職場情報-事業概要"]),
            # 13
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
            # 14, 15, 16, 17
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
                                                    "http://hojin-info.go.jp/code/職場情報/企業規模",
                                                    datatype=IC.コード型,
                                                )
                                                if row[value]
                                                else None
                                            ),
                                        ),
                                        (
                                            IC.単位表記,
                                            unit if row[value] else None,
                                        ),
                                        (
                                            IC.種別,
                                            row[category] if category else None,
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                )
                for value, unit, indicator, category in suryo_keys
            ],
        ]
        return triples


__all__ = ["GbizInfoShokubaMapper"]
