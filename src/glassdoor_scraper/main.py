import os
from gui import GUI


def main() -> None:
    directory = "./output"
    if not os.path.exists(directory):
        os.mkdir(directory)

    GUI.show_ui()

if __name__ == "__main__":
    main()
