import csv

import requests


class GbizinfoClient:
    DOWNLOAD_ENDPOINT = "https://info.gbiz.go.jp/hojin/Download"
    CSV_ENDPOINT = "https://info.gbiz.go.jp/hojin/OutputCSV"
    CSV_MAX_ROWS = 1000

    def __init__(self):
        self.session = requests.Session()

    def download_csv(
        self, downfile: int, downtype: str = "zip", downenc: str = "UTF-8"
    ) -> requests.Response:
        data = {
            "downfile": downfile,
            "downtype": downtype,
            "downenc": downenc,
        }
        res = self.session.post(self.DOWNLOAD_ENDPOINT, data=data, stream=True)
        res.raise_for_status()
        return res

    def download_csv_to_file(
        self,
        file_path: str,
        downfile: int,
        downtype: str = "zip",
        downenc: str = "UTF-8",
    ) -> None:
        res = self.download_csv(downfile, downtype, downenc)
        with open(file_path, "wb") as f:
            for c in res.iter_content(chunk_size=4 * 1024):
                f.write(c)

    def output_csv(
        self, hojin_bango_list: list[str], csvdata: str = "00", output: str = "U"
    ) -> list[dict[str, str]]:
        data = {
            "csvdata": csvdata,
            "output": output,
            "hojinBangoList": ",".join(hojin_bango_list),
        }
        res = self.session.post(self.CSV_ENDPOINT, data=data, stream=True)
        res.raise_for_status()
        lines = res.iter_lines(decode_unicode=True)
        next(lines)
        return [row for row in csv.DictReader(lines)]
