from rdflib import Namespace
from rdflib.namespace import RDF, XSD

IC = Namespace("http://imi.go.jp/ns/core/rdf#")
IC_ID = Namespace("http://imi.go.jp/ns/code_id/id/")
HJ = Namespace("http://hojin-info.go.jp/ns/domain/biz/1#")
HJ_DATA = Namespace("http://hojin-info.go.jp/data/")
HJ_BASIC = Namespace("http://hojin-info.go.jp/data/basic/")
HJ_EXT = Namespace("http://hojin-info.go.jp/data/ext/")
ISO4217 = Namespace(
    "urn:un:unece:uncefact:codelist:standard:ISO:ISO3AlphaCurrencyCode:2012-08-31#"
)

__all__ = [
    "RDF",
    "XSD",
    "IC",
    "IC_ID",
    "HJ",
    "HJ_DATA",
    "HJ_BASIC",
    "HJ_EXT",
    "ISO4217",
]
