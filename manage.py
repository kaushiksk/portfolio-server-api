from portfolioserver.db import init_db_from_cas_file
import click
import cutie
import os
import sys

CAS_FILE_PATH = "./cas-portfolio.pdf"


@click.group()
def cli():
    pass


@cli.command("init-db")
def init_db_command():
    if not os.path.exists(CAS_FILE_PATH):
        print(
            "File not found. Make sure you saved your CAS file as cas-portfolio.pdf in directory root"
        )
        sys.exit(0)

    init_db_from_cas_file(CAS_FILE_PATH)


@cli.command("run")
@click.option("--host", default="127.0.0.1", help="Bind socket to this host.")
@click.option("--port", default=8000, help="Port to run the server on.")
def runserver(host, port):
    os.system(
        "uvicorn --factory portfolioserver:create_app --host {0} --port {1}".format(
            host, port
        )
    )


if __name__ == "__main__":
    cli()
