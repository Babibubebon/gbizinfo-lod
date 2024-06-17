import csv
import os
import shutil
import time
from typing import Iterator

import click

from . import __version__
from .client import GbizinfoClient
from .mappers import *


@click.group()
def cli():
    pass


@cli.command()
def version():
    click.echo(f"gbizinfo_lod/{__version__}")


@cli.command(help="Download CSV files")
@click.argument(
    "work_dir", type=click.Path(exists=True, file_okay=False, writable=True)
)
@click.option("--sleep", type=int, default=3, help="Sleep time in seconds")
def download(work_dir: str, sleep: int):
    client = GbizinfoClient()

    csv_files = {
        # CSV形式（法人活動情報語彙対応版）
        0: "TodokedeNinteijoho",
        1: "Hyoshojoho",
        2: "Hojokinjoho",
        3: "Chotatsujoho",
        4: "Tokkyojoho",
        5: "Zaimujoho",
        6: "Shokubajoho",
        # CSV形式
        7: "Kihonjoho",
    }

    for file_id, name in csv_files.items():
        zip_file_name = f"{name}_UTF-8.zip"
        csv_file_name = f"{name}_UTF-8.csv"
        zip_file_path = os.path.join(work_dir, zip_file_name)
        csv_file_path = os.path.join(work_dir, csv_file_name)

        click.echo(f"Downloading {zip_file_name}")
        client.download_csv_to_file(zip_file_path, file_id)
        click.echo(f"Unpacking {zip_file_name}")
        shutil.unpack_archive(zip_file_path, work_dir)
        os.remove(zip_file_path)

        if not os.path.exists(csv_file_path):
            raise click.ClickException(f"{csv_file_path} not found")

    kihonjoho_csv_file = os.path.join(work_dir, "Kihonjoho_UTF-8.csv")
    kihonjoho_imi_file = os.path.join(work_dir, "Kihonjoho_IMI_UTF-8.csv")

    if not os.path.exists(kihonjoho_imi_file):
        click.echo("Retrieving Kihonjoho (IMI version)")
        with open(kihonjoho_imi_file, "w", encoding="utf-8") as f:
            writer = None
            for row in get_kihonjoho_imi(kihonjoho_csv_file, client):
                if writer is None:
                    writer = csv.DictWriter(f, fieldnames=row.keys())
                    writer.writeheader()
                writer.writerow(row)


def get_kihonjoho_imi(
    csv_file: str, client: GbizinfoClient, sleep: int = 3
) -> Iterator[dict]:
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        count = 0
        chunk = []
        for row in reader:
            if not row["法人名"]:
                click.echo(f"skip: {row['法人番号']}", err=True)
                continue

            chunk.append(row["法人番号"])
            if len(chunk) == client.CSV_MAX_ROWS:
                count += len(chunk)
                click.echo(f"{count} ...")

                for r in client.output_csv(chunk):
                    yield r
                chunk.clear()
                time.sleep(sleep)

        if len(chunk) > 0:
            for r in client.output_csv(chunk):
                yield r

        count += len(chunk)
        click.echo(f"{count}")


MAPPER_TYPES = [
    "hojin",
    "hojyokin",
    "chotatsu",
    "hyosho",
    "todokede",
    "tokkyo",
    "shokuba",
    "zaimu",
]


@cli.command(help="Convert CSV files to RDF")
@click.argument("work_dir")
@click.option(
    "--mapper", "-m", "mappers", multiple=True, type=click.Choice(MAPPER_TYPES)
)
@click.option("--processes", "-p", type=int, default=-1)
@click.option(
    "--output-dir", "-o", type=click.Path(exists=True, file_okay=False, writable=True)
)
def convert(work_dir: str, mappers: list[str], processes: int, output_dir: str):
    if not mappers:
        mappers = MAPPER_TYPES
    if not output_dir:
        output_dir = work_dir

    for m in mappers:
        match m:
            case "hojin":
                mapper = GbizInfoHojinMapper(
                    os.path.join(work_dir, "Kihonjoho_IMI_UTF-8.csv")
                )
            case "hojyokin":
                mapper = GbizInfoHojyokinMapper(
                    os.path.join(work_dir, "Hojokinjoho_UTF-8.csv")
                )
            case "chotatsu":
                mapper = GbizInfoChotatsuMapper(
                    os.path.join(work_dir, "Chotatsujoho_UTF-8.csv")
                )
            case "hyosho":
                mapper = GbizInfoHyoshoMapper(
                    os.path.join(work_dir, "Hyoshojoho_UTF-8.csv")
                )
            case "todokede":
                mapper = GbizInfoTodokedeMapper(
                    os.path.join(work_dir, "TodokedeNinteijoho_UTF-8.csv")
                )
            case "tokkyo":
                mapper = GbizInfoTokkyoMapper(
                    os.path.join(work_dir, "Tokkyojoho_UTF-8.csv")
                )
            case "shokuba":
                mapper = GbizInfoShokubaMapper(
                    os.path.join(work_dir, "Shokubajoho_UTF-8.csv")
                )
            case "zaimu":
                mapper = GbizInfoZaimuMapper(
                    os.path.join(work_dir, "Zaimujoho_UTF-8.csv")
                )
            case _:
                raise NotImplementedError

        output_file = os.path.join(output_dir, f"{m}.nt")
        click.echo(f"output: {output_file}")
        click.echo(f"Running {m} mapper ...")
        with open(output_file, "w") as f:
            mapper.run(n_jobs=processes, output=f)


@cli.command(help="Fetch CSV data from OutputCSV endpoint")
@click.argument("hojin_bango")
def output_csv(hojin_bango: str):
    client = GbizinfoClient()
    res = client.output_csv([hojin_bango])
    for row in res:
        click.echo(row)
