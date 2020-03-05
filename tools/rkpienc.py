"""
Reference implementation of the Reekpie encoder.
Only v1.0 is supported (the only ever made).
"""

import zstandard
import brotli
import lzma

from utils     import maprange, copyfile, copyfilemap, rnum
from argparse  import ArgumentParser, FileType
from sys       import stdout, stdin, stderr
from functools import partial

class ReekpieEncoder(ArgumentParser):
    _SAMPLEFORMATS       = ('unsigned', 'signed', 'float', 'adpcm', 'mu-law', 'a-law')
    _COMPRESSORS         = ('none', 'zstd', 'brotli', 'lzma')

    def __init__(self):
        ArgumentParser.__init__(self)

        self.add_argument('file_in',
            type= FileType('rb'),
            nargs= '?', default= stdin.buffer,
            help= "readable file to read raw data")

        self.add_argument('-o',
            dest= 'file_out', type= FileType('wb'),
            default= stdout.buffer,
            help= "writable file to put encoded data")

        self.add_argument('-sampleformat',
            dest= 'pcm_sampleformat', required= True,
            choices= self._SAMPLEFORMATS,
            help= "sampleformat used in PCM data")

        self.add_argument('-compression',
            dest= 'rkpi_compression',
            choices= self._COMPRESSORS, default= 'none',
            help= "compression algorithm applied on input data")
        
        self.add_argument('--compresssion-density',
            dest= 'rkpi_compression_density',
            type= partial(rnum, min= 0, max= 100), default= 100,
            help= "effort to be applied to compression (more = more effort)")
        
        self.add_argument('-bytedepth',
            dest= 'pcm_bytedepth', required= True,
            type= int, choices= (1, 2, 3, 4, 8),
            help= "bytedepth of PCM data")

        self.add_argument('-samplerate',
            dest= 'pcm_samplerate', required= True,
            type= partial(rnum, min= 0, max= 2**32 - 1),
            help= "samplerate of PCM data")

        self.add_argument('-planar',
            dest= 'pcm_channellayout',
            action= 'store_true',
            help= "use planar channellayout")

        self.add_argument('--big-endian',
            dest= 'pcm_endianness',
            action= 'store_true',
            help= "use big-endian byteorder")

        self.add_argument('-channels',
            dest= 'pcm_channels', required= True,
            type= partial(rnum, min= 1, max= 64),
            help= "number of channels inside PCM data")

        self.args = self.parse_args()
    
    def main(self):
        rkpihdr = {
            'sampleformat':      self._SAMPLEFORMATS.index(self.args.pcm_sampleformat) + 1,
            'compression':       self._COMPRESSORS  .index(self.args.rkpi_compression)    ,
            'bytedepth':         self.args.pcm_bytedepth                                  ,
            'samplerate':        self.args.pcm_samplerate                                 ,
            'channellayout':     self.args.pcm_channellayout                              ,
            'endianness':    int(self.args.pcm_endianness)                                ,
            'channels':          self.args.pcm_channels
        }

        # override bytedepth if the sampleformat forces so.
        if self.args.pcm_sampleformat in ('adpcm', 'a-law', 'mu-law'):
            rkpihdr['bytedepth'] = 1

        # write out the header to file, doesn’t care about the
        # raw data in the file as there’s no size info.
        self.args.file_out.write(self._encode_rkpi_hdr(rkpihdr))

        if self.args.rkpi_compression == 'none':
            if copyfile(self.args.file_in, self.args.file_out) == 0:
                stderr.write("Can’t do IO.")
        else:
            _COMPDS = partial(maprange, self.args.rkpi_compression_density, 100j)
            data_copied = 0 # how many bytes were copied compression.

            # Zstandard compressor.
            if rkpihdr['compression'] == 0b01:
                data_copied = copyfilemap(
                    self.args.file_in, self.args.file_out,
                    zstandard.ZstdCompressor(level= _COMPDS(1+22j)).compress)
            
            # Brotli compressor.
            if rkpihdr['compression'] == 0b10:
                comp = brotli.Compressor(quality= _COMPDS(11j), lgwin= 24)

                data_copied = copyfilemap(
                    self.args.file_in, self.args.file_out, comp.compress)
                data_copied+= self.args.file_out.write(comp.finish())

            # LZMA compressor.
            elif rkpihdr['compression'] == 0b11:
                data_copied = copyfile(self.args.file_in,
                    lzma.LZMAFile(self.args.file_out, 'w'))
            

            if data_copied == 0:
                stderr.write("Compressor failed or can’t do IO.")
    
    @classmethod
    def _encode_rkpi_hdr(self, opts: dict) -> bytes:
        return b'RKPI' + bytes((
            ((opts['sampleformat']  &    7) << 5) |
            ((opts['compression']   &    3) << 3) |
            ((opts['bytedepth']     &    3) -  1) ,
             (opts['samplerate']    >>  24) &  255,
             (opts['samplerate']    >>  16) &  255,
             (opts['samplerate']    >>   8) &  255,
              opts['samplerate']            &  255,
            ((opts['channellayout'] &    1) << 8) |
            ((opts['endianness']    &    1) << 7) |
            ((opts['channels']      &   63) -  1)))

if __name__ == "__main__":
    rkpienc = ReekpieEncoder()
    rkpienc.main()