import argparse

import convert.numpy


def _main():

    FILE_EXTENSIONS = tuple(file_extension
                            for module in convert.universal.SUPPORTED_MODULES
                            for file_extension in module.FILE_EXTENSIONS)

    # parse arguments
    parser = argparse.ArgumentParser(
        description=f'Convert a file containing into another file format. '
                    f'Supported file extensions are {FILE_EXTENSIONS}.'
                    f'Not every converting might be reasonable.')

    parser.add_argument('file', type=str,
                        help='The file that should be converted.')
    parser.add_argument('file_extension', type=str, choices=FILE_EXTENSIONS,
                        help='The new file extension to which the file should be converted.')

    args = parser.parse_args()

    # convert
    convert.numpy.convert_file_extension(args.file, args.file_extension)


if __name__ == "__main__":
    _main()
