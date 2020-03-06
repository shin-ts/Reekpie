<h1 align=center>reekpie tools</h1>

> a general purpose lossless audio-format tailored to be a replacement for the most popular format WAVE.

This is a reference implementation of the audio-format written in Python 3x, which supports all the features denoted in the specification.

![](https://img.shields.io/badge/License-WTFPL-blue)
![](https://img.shields.io/badge/Made%20with-Python%203.x-blue)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/tryamid/reekpie)
![GitHub contributors](https://img.shields.io/github/contributors/tryamid/reekpie)
![GitHub last commit](https://img.shields.io/github/last-commit/tryamid/reekpie)

---

### Installation
[Python >=3.5][1] interpreter is required for executing the tools (make sure that it’s in the path). Note that, installation methods might differ as of environment (eg. on a Debian based system one might run `apt-get install python3 python3-pip`, `pacman -S python-pip` on a ArchLinux based system).

Make sure that the output of `where python` or `which python` or `which python3` and `where pip` or `which pip` or `which pip3` isn’t blank.

Main code exists in the `tools/` folder, you’ve to install it manually as there’s no PyPI package yet for this tool. Switch the current directory to there and execute `pip -r requirements.txt` (replace `pip` with `pip3` if doesn’t work).

### Usage

An imaginary file is choosen for the input for demonstration purposes. The name is `reekapeeka.raw` which is a raw PCM data (bitdepth = 24, channels = 2, bytedepth = 3, samplerate = 48000, sampleformat = float).

> Extension convention for Reekpie files is either `.rkp` or `.rkpi`.

<br/>

Encapsulate PCM data with no compression at all. Note that the details about input must be given in advance because there’s no other way it can detect.
```ps
rkpienc 'reekapeeka.raw' -bytedepth 3 -samplerate 48000 -channels 2 'reekapeeka.rkp'
```

Encapsulate PCM data with 'brotli' compression. Yes, it does have compression but supports only some, either 'zstd' or 'brotli' or 'lzma'.

```ps
rkpienc 'reekapeeka.raw' -bytedetpth 3 -samplerate 48000 -channels 2 -compression brotli 'reekapeeka.rkp'
```

> #### Limitations
> - **Compression**: 'brotli' or 'zstd' or 'lzma' or no compression at all.
> - **Bytedepth**: 1, 2, 3, 4, 8 (5, 6, 7 are allowed but not used often so excluded).
> - **Samplerate**: 0 to 4294967295 (eg. 44100, 48000 are used more often).
> - **Channels**: 0 to 63 (eg. 1, 2, 6 are used more often).
> - **Sampleformats**: 'unsigned' or 'signed' or 'float' or 'adpcm' or 'a-law' or 'mu-law'.

---

### Contribution
Contribution can be done either making the reference implementation better or enriching the specification. If you like to do a change fork this project and file a pull request with describing what have you changed what’s the point of it.

[1]: https://www.python.org/downloads/