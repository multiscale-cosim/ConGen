import commands
from . import _vicogen


def main():
    args = commands.parse_arguments()
    _vicogen.handle_arguments(args)

if __name__ == '__main__':
    main()
