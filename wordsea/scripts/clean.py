from wordsea.dictionary.clean import WikiRawStream


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean the raw Wiktionary data.",
        epilog="Download pre-extracted data from https://kaikki.org/dictionary/rawdata.html.",
    )
    parser.add_argument("path", type=str, help="path to raw Wiktionary data (JSON)")
    args = parser.parse_args()

    stream = WikiRawStream(path=args.path)
    stream.process()
    stream.export()
