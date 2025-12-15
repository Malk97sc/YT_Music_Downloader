import argparse
from ytmd.interfaces.cli import main as cli_main
from ytmd.interfaces.gui import main as gui_main

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Music Downloader"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run in GUI mode"
    )

    args = parser.parse_args()

    if args.cli and args.gui:
        print("Choose only one mode: --cli or --gui")
        return

    if args.cli:        
        cli_main()
    elif args.gui:
        gui_main()
    else:
        print("Please choose a mode: --cli or --gui")
