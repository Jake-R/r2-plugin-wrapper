import r2lang
import base64
import json

from r2_plugin import plugify


@plugify('At', 'returns a test value')
def test(string):
    return [{'test': 'value'}]


@plugify('Ax', 'print current location')
def location(string):
    return [{'location': r2lang.cmd('iz~[0]').strip()}]


@plugify('Az', 'print all strings that have an xref in code')
def string_xrefs(string):
    js = json.loads(r2lang.cmd('izj'))
    xrefs = [(val, json.loads(r2lang.cmd('axtj @{}'.format(val['vaddr'])))) for val in js]
    xrefs = [x for x in xrefs if x[1]]
    for x in xrefs:
        x[1][0]['str_addr'] = x[0]['vaddr']
        x[1][0]['string'] = base64.b64decode(x[0]['string'])
    return [x[1][0] for x in xrefs]