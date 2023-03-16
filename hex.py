class Hex:
    @staticmethod
    def bytes_to_hex(bytes):
        l = [format(int(i),'02x') for i in bytes]
        return " ".join(l)

    @staticmethod
    def msg_analysis(bytes):
        l = [hex(int(i)) for i in bytes]
        return " ".join(l)
