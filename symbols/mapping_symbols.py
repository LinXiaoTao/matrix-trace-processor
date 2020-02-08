from collections import namedtuple

ACC_PUBLIC = 1
ACC_PRIVATE = 2
ACC_PROTECTED = 4
ACC_STATIC = 8
ACC_FINAL = 16
ACC_SUPER = 32
ACC_SYNCHRONIZED = 32
ACC_VOLATILE = 64
ACC_BRIDGE = 64
ACC_VARARGS = 128
ACC_TRANSIENT = 128
ACC_NATIVE = 256
ACC_ERFACE = 512
ACC_ABSTRACT = 1024
ACC_STRICT = 2048
ACC_SYNTHETIC = 4096
ACC_ANNOTATION = 8192
ACC_ENUM = 16384
ACC_MANDATED = 32768
ACC_DEPRECATED = 131072


def format_access_flag(access_flag):
    result = ''
    if access_flag & ACC_PUBLIC:
        result += 'public '
    if access_flag & ACC_PRIVATE:
        result += 'private '
    if access_flag & ACC_PROTECTED:
        result += 'protected '
    if access_flag & ACC_STATIC:
        result += 'static '
    if access_flag & ACC_FINAL:
        result += 'final '
    if access_flag & ACC_SUPER:
        result += 'super '
    if access_flag & ACC_SYNCHRONIZED:
        result += 'synchronized '
    if access_flag & ACC_VOLATILE:
        result += 'volatile '
    if access_flag & ACC_BRIDGE:
        result += 'bridge '
    if access_flag & ACC_NATIVE:
        result += 'native '
    if access_flag & ACC_ABSTRACT:
        result += 'abstract'
    return result


def extract_mapping_symbols(mapping):
    method_index = {}
    with open(mapping) as mapping_file:
        mapping_content = mapping_file.readlines()
        for symbol in mapping_content:
            symbol = symbol.replace('\n', '')
            method_id = symbol.split(',')[0]
            method_info = symbol.split(',')[2]
            method_index[method_id] = method_info
    return namedtuple('MappingSymbols', ['method_index'])(method_index)
