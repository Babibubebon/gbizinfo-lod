# gBizINFO-LOD

[![PyPI version](https://badge.fury.io/py/gbizinfo-lod.svg)](https://badge.fury.io/py/gbizinfo-lod)

[gBizINFO](https://info.gbiz.go.jp/)が提供する[CSV形式のデータ](https://info.gbiz.go.jp/hojin/DownloadTop)からLinked Open Data(LOD)データセットを生成するためのツール

生成したデータセットにアクセスできる公開SPARQLエンドポイントも以下で提供しています。

<https://metadata.moe/project/gbizinfo/>

## 使い方

### インストール

```shell
pip install gbizinfo-lod
```

### CSVファイルダウンロード

変換元となる法人活動情報語彙対応版CSVファイル群のダウンロード
(注: 法人基本情報は全件の一括ダウンロードが不可のため時間がかかる)

```shell
gbilod download ./work_dir/
```

### CSV-RDF変換

ダウンロードしたCSVファイル群をRDFに変換

```shell
gbilod convert ./work_dir/ -o ./output_dir/
```

[Graph URI](#graph-uri)毎にファイルが出力される(デフォルトはN-Quads形式)

その他オプションは `gbilod convert --help` を参照

## 変換仕様

基本的には以下の仕様書に基づく。

- gBizINFO SPARQL API仕様書: https://warp.ndl.go.jp/info:ndljp/pid/13539552/info.gbiz.go.jp/api/document/API.pdf
- リソース定義書 (CSV, XMLスキーマ仕様書): https://info.gbiz.go.jp/common/data/resourceinfo.pdf

### 仕様書との差異

仕様書上の定義と異なる、または未定義である箇所を以下にまとめる。

- 法人番号を表す `ic:ID/ic:体系` の目的語は `<http://imi.go.jp/ns/code_id/id/corporateNumber>`

```turtle
ex:Hojin <http://imi.go.jp/ns/core/rdf#ID> [
         <http://imi.go.jp/ns/core/rdf#体系> <http://imi.go.jp/ns/code_id/id/corporateNumber> ;
         <http://imi.go.jp/ns/core/rdf#識別値> "0123456789123" ;
         a <http://imi.go.jp/ns/core/rdf#ID型>
] .
```

- 職場情報および財務情報における `hj:数量コレクション/hj:数量/hj:指標` の目的語はic:コード型の型付リテラル
  - 提供されていたRDFデータがこのようになっており、互換性確保のためこの仕様を踏襲する。 
  - 本来はリテラルではなく、 `http://hojin-info.go.jp/graph/commonCode` グラフ内で定義されているリソースへのURI参照を期待したものと思われる。

```turtle
ex:HojinShokuba <http://hojin-info.go.jp/ns/domain/biz/1#数量コレクション> [
    <http://hojin-info.go.jp/ns/domain/biz/1#数量> [
        <http://hojin-info.go.jp/ns/domain/biz/1#指標> "http://hojin-info.go.jp/code/職場情報/企業規模"^^<http://imi.go.jp/ns/core/rdf#コード型> ;
        <http://imi.go.jp/ns/core/rdf#単位表記> "人" ;
        <http://imi.go.jp/ns/core/rdf#数値> 100.0 ;
        a <http://hojin-info.go.jp/ns/domain/biz/1#数量型>
    ]
] .
```

## Graph URI

- 法人基本情報: `http://hojin-info.go.jp/graph/hojin`
- 補助金情報: `http://hojin-info.go.jp/graph/hojyokin`
- 調達情報: `http://hojin-info.go.jp/graph/chotatsu`
- 表彰情報: `http://hojin-info.go.jp/graph/hyosho`
- 届出認定情報: `http://hojin-info.go.jp/graph/todokede`
- 特許情報: `http://hojin-info.go.jp/graph/tokkyo`
- 職場情報: `http://hojin-info.go.jp/graph/shokuba`
- 財務情報: `http://hojin-info.go.jp/graph/zaimu`
- 共通コード: `http://hojin-info.go.jp/graph/commonCode`

## 背景

かつてgBizINFOではSPARQL APIが提供されており、APIを利用することでRDF形式のデータにアクセスすることができた。
また、RDFストアとしてAmazon Neptuneを採用し[^1]、実践的な運用ノウハウが公開されるなど[^2]、システム面でも有用な事例であった。

一方で、野村総合研究所が落札した「令和4年度経済産業省デジタルプラットフォーム構築事業(
Gビズインフォを通じた効果的なオープンデータ利活用の促進に向けた調査)
」の[報告書 (2023年3月17日)](https://www.meti.go.jp/meti_lib/report/2022FY/000235.pdf)
によると、LOD形式でのデータ提供について以下のような実態を指摘しており、公共データ分野でのLODの一定のニーズは認めているものの、SPARQL APIエンドポイントの存続有無の検討が必要と結論づけている。

```
現行Gビズインフォにおける、利用者の期待と現状
機能 - SPARQL API
実態: 法人データにおいてはLODの普及度が低いため、活用されているとは言いがたい。
利用者からの評価: △ インタビュー先のうち多数は知らない・知っているが使いにくいので使わないといった評価であった。
```

2023年10月31日にはgBizINFOサイト上でRDF形式データの提供廃止が告知され、2024年4月1日に完全廃止となった[^3]。

[^1]: [AWS 導入事例：経済産業省](https://aws.amazon.com/jp/solutions/case-studies/meti/)
[^2]: [経済産業省のデジタル化とgBizINFOの展開 2020年8⽉](https://pages.awscloud.com/rs/112-TZM-766/images/Session%204%20-%20gBizINFO.pdf)
[^3]: [RDF廃止（サービス終了）のお知らせ](https://info.gbiz.go.jp/html/RdfStop.html)

## License

本リポジトリに含まれる [`commonCode.ttl`](commonCode.ttl) および [`commonCode.nq`](commonCode.nq) を除くリソースは、MIT Licenseで提供される。

`commonCode.ttl` および `commonCode.nq` は、「[gBizINFO](https://info.gbiz.go.jp/)」（経済産業省）のSPARQL APIより取得・加工して作成したもので、[経済産業省 利用規約](https://www.meti.go.jp/main/rules.html)に従い利用するものである。
