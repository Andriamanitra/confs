import json
import pathlib
import sys

import lark


class ConfsTreeToDict(lark.Transformer):
    INT_MIN = - 2 ** 63
    INT_MAX = 2 ** 63 - 1

    def empty(self, items) -> list:
        return []

    def number(self, items) -> int:
        value = int(items[0].value)
        if value < self.INT_MIN or value > self.INT_MAX:
            raise ValueError("Integer value out of bounds!")
        return value

    def multiline_string(self, items) -> str:
        value = items[0].value.strip()
        return value.removeprefix('"\n').removesuffix('\n"')

    def string(self, items) -> str:
        value = items[0].value
        return value.removeprefix('"').removesuffix('"')

    def list(self, items) -> list:
        return items

    def checked_assignment(self, items) -> dict:
        options, identifier, rvalue = items
        options = [option.value for option in options.children]
        identifier = identifier.value
        rvalue = rvalue.value
        if rvalue in options:
            value = options.index(rvalue)
        else:
            valids = ', '.join(options)
            raise ValueError(
                f"Invalid value '{rvalue}' for enumerable '{identifier}'. " +
                f"Valid values are: {valids}")
        return {identifier: value}

    def assignment(self, items) -> dict:
        identifier, rvalue = items
        return {identifier.value: rvalue}

    def section(self, items) -> dict:
        header, *assignments = items
        result = {}
        current = result
        for part in header.children:
            current[part.value] = {}
            current = current[part]
        for dct in assignments:
            for k, v in dct.items():
                current[k] = v
        return result

    def confs(self, items) -> dict:
        result = {}
        for dct in items:
            result.update(dct)
        return result


confs_spec = pathlib.Path("confs.lark").read_text()
confs_parser = lark.Lark(confs_spec, start="confs")
confs_transformer = ConfsTreeToDict()


def confs2dict(confs: str) -> dict:
    tree = confs_parser.parse(confs)
    return confs_transformer.transform(tree)


def confs2json(confs: str) -> str:
    dct = confs2dict(confs)
    return json.dumps(dct)


def main() -> int:
    confs_str = pathlib.Path(sys.argv[1]).read_text()
    json_str = confs2json(confs_str)
    print(json_str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
