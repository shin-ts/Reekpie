<h1 align=center>reekpie tools</h1>

A general purpose lossless audio-format tailored to be a replacement for the most popular format WAVE or AIFF.
This is a reference implementation of the audio-format written in Python 3x, supports all the features denoted in the specification.

![](https://img.shields.io/badge/License-WTFPL-blue)
![](https://img.shields.io/badge/Made%20with-Python%203.x-blue)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/tryamid/reekpie)
![GitHub contributors](https://img.shields.io/github/contributors/tryamid/reekpie)
![GitHub last commit](https://img.shields.io/github/last-commit/tryamid/reekpie)

---

### Installation
[Python >=3.5][1] interpreter is required for executing the tools (make sure that it’s in the path). Note that, installation methods might differ as of environment (eg. on a Debian based system one might run `apt-get install python3 python3-pip`, `pacman -S python-pip` on a ArchLinux based system).

Make sure that `python` and `pip` are both in PATH, otherwise it will fail (eg. `where python pip` shouldn't return blank lines, replace `where` with `which` if Windows NT).

Main code exists in the `tools/` folder, you’ve to install it manually as there’s no PyPI package yet for this tool. Switch the current directory to there and execute `pip -r requirements.txt` (replace `pip` with `pip3` if doesn’t work).

Python files of `tools/` must be in the PATH variable too to call the script from anywhere in the filesystem. On Windows associate Python files with the interpreter *(TODO: fix this issue on NT based systems with a non-bash shell)*.

### Usage

An imaginary file is choosen for the input for demonstration purposes. The name is `reekapeeka.raw` which is a raw PCM data (bitdepth = 24, channels = 2, bytedepth = 3, samplerate = 48000, sampleformat = float, endianness = little, channellayout = interleaved).

> Extension convention for Reekpie files is either `.rkp` or `.rkpi`.

<br/>

Encapsulate PCM data with no compression at all. Note that the details about input must be given in advance because there’s no other way it can detect. <sup>(1)</sup>
```bash
$ rkpienc 'reekapeeka.raw' -bytedepth 3 -samplerate 48000 -channels 2 'reekapeeka.rkp'
```

Encapsulate PCM data with 'brotli' compression. Yes, it does have compression but supports only some, either 'zstd' or 'brotli' or 'lzma'. <sup>(2)</sup>

```bash
$ rkpienc 'reekapeeka.raw' -bytedetpth 3 -samplerate 48000 -channels 2 -compression brotli 'reekapeeka.rkpi'
```

<br/>
Decapsulate PCM data from the Reekpie file we’ve just encoded (from the second example shown). It should spit out some data on the console like this.

```bash
$ rkpidec 'reekapeeka.rkpi' 'reekapeeka.raw'
Sampleformat:  signed
Compression:   brotli
Bytedepth:     3
Samplerate:    48000
Channellayout: interleaved
Endianness:    little
Channels:      2
```

<sup>^ You use this to re-construct the audio properly. Ignore the 'Compression' field as it’s only informal purposes.</sup>

> #### Limitations
> - **Compression**: ['brotli'][2] or ['zstd'][3] or ['lzma'][4] or no compression at all.
> - **Bytedepth**: 1, 2, 3, 4, 8 (5, 6, 7 are allowed but not used often so excluded).
> - **Samplerate**: 0 to 4294967295 (eg. 44100, 48000 are used more often).
> - **Channels**: 0 to 63 (eg. 1, 2, 6 are used more often).
> - **Sampleformats**: 'unsigned' or 'signed' or 'float' or ['adpcm'][5] or ['a-law'][6] or ['mu-law'][7].
---

### Contribution
Contribution can be done either making the reference implementation better or enriching the specification. If you like to do a change fork this project and file a pull request with describing what have you changed what’s the point of it.

[1]: https://www.python.org/downloads/
[2]: https://brotli.org/
[3]: https://facebook.github.io/zstd/
[4]: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm
[5]: https://en.wikipedia.org/wiki/Adaptive_differential_pulse-code_modulation
[6]: https://en.wikipedia.org/wiki/A-law_algorithm
[7]: https://en.wikipedia.org/wiki/%CE%9C-law_algorithm
