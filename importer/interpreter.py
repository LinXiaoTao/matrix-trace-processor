class TraceFileInterpreter(object):
    def __init__(self, trace_file, symbols=None):
        self.trace_file = trace_file
        self.symbols = symbols

    def interpret(self):
        trace_data = self.trace_file.data
        method_index = self.symbols.method_index
        parse_trace_data = []
        for item in trace_data:
            depth = int(item['depth'])
            method = method_index[item['method_id']]
            if not method:
                method = '_%s' % item['method_id']
            parse_trace_data.append({
                'depth': depth,
                'method': method,
                'durtime': item['durtime']
            })
        return parse_trace_data
