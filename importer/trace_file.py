class TraceFile(object):

    def __init__(self, data):
        super(TraceFile, self).__init__()
        self.data = data

    @staticmethod
    def from_string(data):
        result = []
        for item in data:
            item = item.replace('\n', '')
            result.append({
                'depth': item.split(',')[0],
                'method_id': item.split(',')[1],
                'count': item.split(',')[2],
                'durtime': item.split(',')[3]
            })
        return TraceFile(result)

    @staticmethod
    def from_file(file):
        with open(file) as fd:
            data = fd.readlines()
            return TraceFile.from_string(data)
