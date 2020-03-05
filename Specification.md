<h1 align=center>reekpie</h1>
<p align=center>a general purpose lossless audio-format tailored to be a replacement for the most popular format WAVE, claimed to save more bytes <s>entropy</s> than WAVE/AIFF, allows some of best compression algorithms to compress the PCM data for saving even more (e.g lzma, zstd).</p>
<p align=center>This format is made very simple for <b>programmers</b> to implement it in their applications.</p>

---

### Features
- Supports lossless compression (eg. brotli, gzip, xzip).
- No muxing overhead at all.
- Supports variants of PCM *(eg. ADPCM, a-law, mu-law)*.

#### Compressors
Compression algorithms supported by the format alongside their authors, baseline decoders or encoders doesn't require these to be implmented.

- [Zstandard][2] — Facebook
- [Brotli][3] — Google
- [LZMA][4] — Igor Pavlov (7-Zip)

#### Sampleformats
Types of PCM coding variants are supported in the format, some are non-linear formats. Every encoder and decoder impelementation must implement these.

- Signed
- Unsigned
- Float
- ADPCM
- μ-law
- A-law

---

### Specification
More granule implementation details about how exactly it should be interchanged between programs. Specification is splitted into several versions, each version differs from each other.

Size of fields in the header stays constant version to version unless a version states a different magic code for parsing. Multibyte integers always use the big-endian byteorder.

#### v`1.0`

Valid files must contain `0x52, 0x4b, 0x50, 0x49` magic code in the beginning as an identifier of a Reekpie file (eg. tagging structures such as ID3v2 aren't allowed).

Total size of the header is `10` bytes including the magic code. Size column denotes much bits each field does consume. Addtional techniques are used to save even more space, those techniques are described in the description of each field.

<table>
<th>Field</th><th>Size</th><th>Description</th>
<tr><td>Sampleformat</td><td>3</td><td>Variant of PCM used to encode. Note that, ADPCM, Mu-law, A-law enforces the bytedepth to be exactly <code>1</code> byte.<ul>
<li>1 = Unsigned</li>
<li>2 = Signed</li>
<li>3 = Float</li>
<li>4 = ADPCM</li>
<li>5 = Mu-law</li>
<li>6 = A-law</li>
</ul></td></tr>
<tr><td>Compression</td><td>2</td><td>Compression algorithm used to compress PCM data.<ul>
<li>0 = Uncompressed</li>
<li>1 = Zstandard</li>
<li>2 = Brotli</li>
<li>3 = LZMA</li>
</ul>
Note that, baseline encoders might not support all the algorithms described here.
</td></tr>
<tr><td>Bytedepth</td><td>3</td><td>Number of bytes each sample takes to represent itself. The value to put here is <code>Bytedepth - 1</code> (eg. <code>1</code> becomes <code>0</code>, <code>8</code> becomes <code>7</code>).</td></tr>
<tr><td>Samplerate</td><td>32</td><td>Number of PCM samples are in per second known as the samplerate of audio. If not the exact, a pitch shift can be heard.</td></tr>
<tr><td>Channellayout</td><td>1</td><td>Ordering of channels throughout the PCM stream. Note that, interleaved is the most common and planar is rarer.<ul>
<li>0 = Interleaved</li>
<li>1 = Planar</li>
<ul></td></tr>
<tr><td>Endianness</td><td>1</td><td>Endianness of multibyte PCM samples. Note that, for singlebyte samples ignore this field.<ul>
<li>0 = Little</li>
<li>1 = Big</li>
<ul></td></tr>
<tr><td>Channels</td><td>6</td><td>Number of audio channels in the PCM data. The value to put here is <code>Number of Channels - 1</code> (eg. <code>1</code> becomes <code>0</code>, <code>64</code> becomes <code>63</code>).</td></tr>
</table>

---

[2]: https://facebook.github.io/zstd/
[3]: https://brotli.org/
[4]: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm