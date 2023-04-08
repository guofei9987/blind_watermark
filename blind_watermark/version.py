__version__ = '0.4.4'


class Notes:
    def __init__(self):
        self.show = True

    def print_notes(self):
        if self.show:
            print(f'''
Welcome to use blind-watermark, version = {__version__}
Make sure the version is the same when encode and decode
Your star means a lot: https://github.com/guofei9987/blind_watermark
This message only show once. To close it: `blind_watermark.bw_notes.close()`
            ''')
            self.close()

    def close(self):
        self.show = False


bw_notes = Notes()
