"""Utilities for general work (eg. decoding, encoding)
these are not specific to this stuff."""

from functools import partial
from io        import DEFAULT_BUFFER_SIZE
from argparse  import ArgumentParser

def rnum(n, min, max):
    """Constrcuts a number constrained under a certain range
    whose bounds are [min..max)"""
    n = float(n)
    
    if n < min or n > max:
        raise ValueError(f"numeral out of bounds of [{min}..{max})")

    return int(n) if n.is_integer() else n

def copyfile(i, o, bufsize= DEFAULT_BUFFER_SIZE) -> int:
    """Copies a readable filestream's content into a 
    writable filestream, yields how many bytes were copied.
    
    If the `i` filestream doesn't support `read` call
    or `o` doesn't support `write` call, `0` is returned"""
    if not hasattr(i, 'read') or not hasattr(o, 'write'):
        return 0

    total_copied = 0
    in_data = i.read(bufsize)

    if not isinstance(in_data, bytes):
        return 0

    while in_data:
        o.write(in_data)
        total_copied+= len(in_data)

        in_data = i.read(bufsize)
    return total_copied

def copyfilemap(i, o, cb, bufsize= DEFAULT_BUFFER_SIZE) -> int:
    """Same as `copyfile`, except passes through data recieved
    from input by a callback and writes to the output file.

    `cb` is a function accepting an argument (input data at
    a maximum size of `DEFAULT_BUFFER_SIZE`), if not returned
    the same type of value or if not a callable reference `0` is yield"""
    if not hasattr(i, 'read') or not hasattr(o, 'write') or not callable(cb):
        return 0

    total_copied = 0
    in_data = i.read(bufsize)

    if not isinstance(in_data, bytes):
        return 0

    while in_data:
        in_data = cb(in_data)
        if not isinstance(in_data, bytes):
            return 0

        o.write(in_data)
        total_copied+= len(in_data)

        in_data = i.read(bufsize)
    return total_copied

def maprange(x, input: complex, output: complex):
    """Scales bound of `x` as of `input` and converts to another 
    bound as of `output`. `input` and `output` are complex numbers
    whose `real` denotes minimum and `imag` denotes maximum value."""
    a =  input.real; b =  input.imag
    c = output.real; d = output.imag

    return (x-a) * (d-c)/(b-a) + c