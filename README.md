# r2-plugin-wrapper
A wrapper library that makes it simple to implement fully featured radare2 plugins in Python.

Currently in a pre-alpha state and needs modified versions of radare2 and radare2-bindings.
## Usage:
r2-plugin-wrapper is simple:

```python
# import r2's python plugin
import r2lang
# import plugify
from r2_plugin import plugify

#decorate your function
@plugify('Ax', 'print current location')
def location(string):
    return [{'location': r2lang.cmd('s').strip()}]
```
r2-plugin-wrapper handles print modes for you, just create a function that takes a string as an argument and returns a list of dictionaries and then launch r2 with `r2 -i path/to/your/plugin.py`.



