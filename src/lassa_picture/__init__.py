class Picture:
    def __init__(self, path: str = None):
        if path:
            self.import_file(path)
        else:
            self.path: str = path
            self.data: list = None
            self.grey: bool = None

    def __str__(self):
        cntn = ""
        if self.grey:
            if self.data:
                for ligne in self.data:
                    for pixel in ligne:
                        cntn += f"\033[38;2;{pixel[0]};{pixel[0]};{pixel[0]}m██"
                    cntn += '\033[0m\n'
        else:
            if self.data:
                for ligne in self.data:
                    for pixel in ligne:
                        r, g, b = pixel
                        cntn += f"\033[38;2;{r};{g};{b}m██"
                    cntn += '\033[0m\n'
        return cntn

    def get_data_file(self) -> str:
        """
        Return file data in string.
        :return: File data.
        """
        def get_value(x: int) -> str:
            """
            Returns the value in 3 digits.
            :param x: The value.
            :return: The value with 3 digits.
            """
            txt = str(x)
            while len(txt) < 3:
                txt = '0' + txt
            return txt

        cntn = str(int(self.grey)) + "\n"

        for ligne in self.data:
            for pixel in ligne:
                r, g, b = pixel
                cntn += f"{get_value(r)},{get_value(g)},{get_value(b)}|"
            cntn = cntn[:-1] + "\n"

        return cntn

    def import_file(self, path: str) -> None:
        """
        Import the .lassa file
        :param path: Picture file path.
        :return: None
        """
        self.path = path
        self.grey = open(path, 'r').read().splitlines()[0] == '1'
        if self.grey:
            self.data = [
                [
                    [pixel] for pixel in ligne.split('|')
                ]
                for ligne in open(path, 'r').read().splitlines()[1:]
            ]
        else:
            self.data = [
                [
                    [pixel.split(',')[0], pixel.split(',')[1], pixel.split(',')[2]]
                    for pixel in ligne.split('|')
                ]
                for ligne in open(path, 'r').read().splitlines()[1:]
            ]

    def export_file(self, path: str = None) -> None:
        """
        Export the .lassa file
        :param path: Picture file path.
        :return: None
        """
        if self.data:
            if not path:
                path = self.path

            cntn = self.get_data_file()

            with open(path, 'w') as file:
                file.write(cntn)

    def convert_grey(self, path: str = None) -> None:
        """
        Convert file to grayscale
        :param path: Picture file path.
        :return: None
        """
        if not self.grey:
            if not path:
                path = self.path

            self.grey = True
            cntn = "1\n"
            for ligne in self.data:
                for pixel in ligne:
                    r, g, b = pixel
                    cntn += f"{int(0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b))}|"
                cntn = cntn[:-1] + "\n"
            with open(path, 'w') as file:
                file.write(cntn)

            self.import_file(path)

    def draw(self) -> None:
        """
        Draw the drawing
        :return: None
        """
        print(self)
