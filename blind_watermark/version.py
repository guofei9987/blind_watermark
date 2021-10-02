__version__ = '0.4.1'
print_notes = True


class Notes:
    def __init__(self):
        self.show = True

    def print_notes(self):
        if self.show:
            print(f'''
Welcome to use blind-watermark, version = {__version__}
Make sure the version is the same when encode and decode
Star matters: https://github.com/guofei9987/blind_watermark
This message only show once. To close it: blind_watermark.bw_notes.close()
            ''')
            self.close()

    def close(self):
        self.show = False


bw_notes = Notes()
