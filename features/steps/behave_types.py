from behave import register_type


def parse_ints(text):
    return [int(s) for s in text.split(",")]


def split_strings(text):
    return text.split(",")


register_type(IntList=parse_ints)
register_type(StrList=split_strings)
