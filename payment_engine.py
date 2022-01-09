import argparse
import os
from engine import Engine


def file_exists(file_path):
    # TODO: move to helper
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError("{0} does not exist".format(file_path))
    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""engine that processes the 
    payments crediting and debiting accounts. Reads input CSV, writes output to stdout"""
    )
    parser.add_argument(dest="file_path", help="CSV file to read", type=file_exists)
    args = parser.parse_args()
    pe = Engine(args.file_path)
    pe.run()
    print("client,available,held,total,locked")
    for client_id, values in pe.client_accounts.items():
        result_str = client_id
        for value in values.values():
            result_str += f",{value}"
        print(result_str)
