import argparse
import os

import convert.universal


def _main():
    description = os.linesep.join((
        f'Convert a file into another file format.',
        f'Supported file extensions are {convert.universal.SUPPORTED_FILE_EXTENSIONS}.',
        f'Supported conversion pairs are {convert.universal.SUPPORTED_FILE_EXTENSION_COMBINATIONS}.'))
    # parse arguments
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('file', type=str,
                        help='The file that should be converted.')
    parser.add_argument('file_extension', type=str, choices=convert.universal.SUPPORTED_FILE_EXTENSIONS,
                        help='The new file extension to which the file should be converted.')

    args = parser.parse_args()

    # convert
    convert.universal.convert_file_extension(args.file, args.file_extension)


if __name__ == "__main__":
    _main()
