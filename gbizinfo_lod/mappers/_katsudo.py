from ..namespace import *
from . import CSV2RDFMapper, Literal, _TripleMapType, bpo


class GbizInfoKatsudoMapper(CSV2RDFMapper):
    """法人活動情報 共通"""

    @staticmethod
    def map_to_triples(row: dict[str, str]) -> list[_TripleMapType]:
        s = HJ_DATA[row["ID-識別値"]]
        ss = HJ_EXT[f"{row['ID-識別値']}_{row['キー情報']}"]

        triples = [
            (s, HJ.法人活動情報, ss),
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
            # 2, 3, 4
            (
                ss,
                IC.名称,
                bpo(
                    [
                        (RDF.type, IC.名称型),
                        (IC.種別, row["名称-種別"]),
                        (IC.表記, row["名称-表記"]),
                        (IC.カナ表記, row["名称-カナ表記"]),
                    ]
                ),
            ),
            # 5, 6, 7
            (
                ss,
                IC.連絡先,
                bpo(
                    [
                        (RDF.type, IC.連絡先型),
                        (IC.種別, row["連絡先-種別"]),
                        (IC.電話番号, row["連絡先-電話番号"]),
                        (IC.FAX番号, row["連絡先-FAX番号"]),
                    ]
                ),
            ),
            # 8, 9
            (
                ss,
                IC.関連組織,
                bpo(
                    [
                        (RDF.type, IC.組織関連型),
                        (IC.役割, row["関連組織-役割"]),
                        (
                            IC.組織,
                            bpo(
                                [
                                    (RDF.type, IC.組織型),
                                    (
                                        IC.名称,
                                        bpo(
                                            [
                                                (RDF.type, IC.名称型),
                                                (IC.表記, row["関連組織-名称"]),
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 10, 11, 12, 13, 14, 15
            (
                ss,
                IC.住所,
                bpo(
                    [
                        (RDF.type, HJ.住所型),
                        (IC.種別, row["住所-種別"]),
                        (IC.表記, row["住所-表記"]),
                        (IC.郵便番号, row["住所-郵便番号"]),
                        (IC.都道府県, row["住所-都道府県"]),
                        (IC.市区町村, row["住所-市区町村"]),
                        (HJ.町名番地等, row["住所-町名番地等"]),
                    ]
                ),
            ),
            # 16, 17, 18
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
                                    (RDF.type, IC.構成員型),
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
            # 19
            (
                ss,
                IC.設立日,
                bpo(
                    [
                        (RDF.type, IC.日付型),
                        (IC.標準型日付, Literal(row["設立日"], datatype=XSD.date)),
                    ]
                ),
            ),
            # 20, 21, 22
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
            # 23
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
            # 24
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
            # 25, 26, 27, 28
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
            # 29
            (
                ss,
                HJ.システム名,
                bpo([(RDF.type, IC.名称型), (IC.表記, row["システム名"])]),
            ),
            # 30
            (ss, HJ.キー情報, row["キー情報"]),
            # 31
            (ss, HJ.業種コード, row["業種コード"]),
            # 32
            (ss, HJ.事業内容, row["事業内容"]),
            # 33
            (
                ss,
                HJ.営業エリア,
                bpo(
                    [
                        (
                            IC.名称,
                            bpo(
                                [
                                    (RDF.type, IC.名称型),
                                    (IC.表記, row["営業エリア-表記"]),
                                ]
                            ),
                        )
                    ]
                ),
            ),
            # 34, 35, 36
            (
                ss,
                HJ.決算情報,
                bpo(
                    [
                        (RDF.type, HJ.決算情報型),
                        (
                            IC.金額,
                            bpo(
                                [
                                    (RDF.type, IC.金額型),
                                    (
                                        IC.数値,
                                        Literal(
                                            row["決算情報-金額"], datatype=XSD.decimal
                                        ),
                                    ),
                                    (IC.通貨, row["決算情報-通貨"]),
                                    (
                                        IC.通貨コード,
                                        Literal(
                                            row["決算情報-通貨コード"],
                                            datatype=ISO4217.ISO3AlphaCurrencyCodeContentType,
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 37
            (
                ss,
                HJ.認定日,
                bpo(
                    [
                        (RDF.type, IC.日付型),
                        (
                            IC.標準型日付,
                            Literal(row["法人活動-認定日"], datatype=XSD.date),
                        ),
                    ]
                ),
            ),
            # 38
            (
                ss,
                HJ.活動名称,
                bpo([(RDF.type, IC.名称型), (IC.表記, row["法人活動-活動名称"])]),
            ),
            # 39
            (ss, HJ.部門, row["法人活動-部門"]),
            # 40, 41
            (
                ss,
                HJ.区分,
                bpo(
                    [
                        (IC.種別, row["法人活動-区分-種別"]),
                        (IC.表記, row["法人活動-区分-内容"]),
                    ]
                ),
            ),
            # 42
            (ss, HJ.対象, row["法人活動-対象"]),
            # 43
            (
                ss,
                IC.金額,
                bpo(
                    [
                        (RDF.type, IC.金額型),
                        (IC.数値, Literal(row["法人活動-金額"], datatype=XSD.decimal)),
                    ]
                ),
            ),
            # 44
            (
                ss,
                HJ.状況,
                bpo(
                    [
                        (RDF.type, IC.状況型),
                        (
                            IC.名称,
                            bpo(
                                [
                                    (RDF.type, IC.名称型),
                                    (IC.表記, row["法人活動-状況名称"]),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 45, 46
            (
                ss,
                IC.期間,
                bpo(
                    [
                        (RDF.type, IC.期間型),
                        (
                            IC.開始日時,
                            bpo(
                                [
                                    (RDF.type, IC.日時型),
                                    (
                                        IC.標準型日付,
                                        Literal(
                                            row["法人活動-期間開始日時"],
                                            datatype=XSD.dateTime,
                                        ),
                                    ),
                                ]
                            ),
                        ),
                        (
                            IC.終了日時,
                            bpo(
                                [
                                    (RDF.type, IC.日時型),
                                    (
                                        IC.標準型日付,
                                        Literal(
                                            row["法人活動-期間終了日時"],
                                            datatype=XSD.dateTime,
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
            # 47
            (ss, HJ.備考, bpo([(IC.種別, row["備考-種別"])])),
            # 48
            (ss, HJ.資格, bpo([(IC.種別, row["資格-表記"])])),
        ]
        return triples


__all__ = ["GbizInfoKatsudoMapper"]
