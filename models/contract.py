class Contract(object):
    def __init__(self):
        self.address = None
        self.bytecode = None
        self.function_sighashes = []
        self.is_erc20 = False
        self.is_erc721 = False
