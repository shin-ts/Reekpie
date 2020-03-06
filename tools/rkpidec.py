#!/usr/bin/env python
"""
Reference implementation of the Reekpie decoder.
Only v1.0 is supported (the only ever made).
"""

import zstandard
import brotli
import lzma

from argparse  import ArgumentParser, FileType
from sys       import stdin, stdout, stderr
from utils     import copyfilemap, copyfile

class ReekpieDecoder(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self)

        self.add_argument('file_in',
            type= FileType('rb'),
            default= stdin.buffer,
            help= "file to decode Reekpie data from")

        self.add_argument('-o',
            dest= 'file_out',
            type= FileType('wb'),
            default= stdout.buffer,
            help= "file to dump decoded raw PCM data into")

        self.add_argument('--no-decompress',
            action= 'store_true',
            dest= 'do_decompress',
            help= "pass the data as it is (don't decompress if compressed)")

        self.args = self.parse_args()

    def main(self):
        rkpihdr = self._decode_rkpi_header(self.args.file_in.read(10))
        if rkpihdr is None:
            print("Reekpie header not found or incomplete."); exit()

        # dump information to the TTY for describing the
        # aspects of the PCM data (as this is required
        # for parsing). NOTE: Put that into STDERR to avoid
        # it being piped with a program or a file by default.
        stderr.write((
             "Sampleformat:  {sample_format}\n"
             "Compression:   {compression}\n"
            f"Bytedepth:     {rkpihdr['bytedepth']}\n"
            f"Samplerate:    {rkpihdr['samplerate']}\n"
             "Channellayout: {channel_layout}\n"
             "Endianness:    {endianness}\n"
            f"Channels:      {rkpihdr['channels']}\n").format_map({
                'channel_layout': ('interleaved', 'planar') \
                                [rkpihdr['channellayout']],
                'endianness':     ('little', 'big') \
                                [rkpihdr['endianness']],
                'sample_format':  ('unknown', 'unsigned', 'signed', 'float', 'adpcm', 'mu-law', 'a-law') \
                                [rkpihdr['sampleformat']],
                'compression':    ('none', 'zstd', 'brotli', 'lzma') \
                                [rkpihdr['compression']]
            }))

        if self.args.do_decompress or rkpihdr['compression'] == 0b00:
            if copyfile(self.args.file_in, self.args.file_out) == 0:
                stderr.write("Can’t do IO.")
        else:
            data_copied = 0 # how many bytes were copied during decompression.

            # Zstandard decompressor.
            if rkpihdr['compression'] == 0b01:
                data_copied = copyfile(zstandard.ZstdDecompressor()
                        .stream_reader(self.args.file_in), self.args.file_out)
            
            # Brotli decompressor.
            elif rkpihdr['compression'] == 0b10:
                data_copied = copyfilemap(self.args.file_in, self.args.file_out,
                    brotli.Decompressor().decompress)
            
            # LZMA decompressor.
            elif rkpihdr['compression'] == 0b11:
                data_copied = copyfile(lzma.LZMAFile(self.args.file_in), self.args.file_out)
            

            if data_copied == 0:
                stderr.write("Decompressor failed or can’t do IO.")
            
    @classmethod
    def _decode_rkpi_header(self, hdr: bytes) -> dict or None:
        if len(hdr) < 10:      return None
        if hdr[:4] != b'RKPI': return None

        return {
            'sampleformat':   hdr[4] >> 5                ,
            'compression':    hdr[4] >> 3           &  3 ,
            'bytedepth':     (hdr[4] &  7)          +  1 ,
            'samplerate':     hdr[8]       | hdr[7] << 8 |
                              hdr[6] << 16 | hdr[5] << 24,
            'channellayout':  hdr[9] >> 7                ,
            'endianness':     hdr[9] >> 6           &  1 ,
            'channels':      (hdr[9] &  63)         +  1
        }

if __name__ == "__main__":
    rkpidec = ReekpieDecoder()
    rkpidec.main()