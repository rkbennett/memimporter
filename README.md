# Memimporter

memimporter is an implementation of the _memimporter package which is part of [py2exe](https://github.com/py2exe/py2exe). The build process (setup.py) was based on [paker](https://github.com/desty2k/paker)'s setup.py.

## Usage

While you could simply use this iteration of memimporter the same as you normally would, this one comes with a couple extra goodies. The first being a new dlopen function, which mimics cffi's dlopen function but from memory. Another thing different about this implementation is that I've added a dllmain function, which means if this dll is loaded by python the function is automatically added to the builtin functions.

## Preamble

When I was trying to figure out how to load pyd files from memory I ran into a curious chicken or the egg scenario. I could use memimporter to load the pyd files, but memimport itself is a pyd. This left me trying to figure out what would/could load memimport's pyd itself. That is when I happened upon [pymemimporter](https://github.com/n1nj4sec/pymemimporter). Sadly this repo was pretty out of date in that it only had working shellcode for x86, and to make matters worse it was written for python 2 (gross). So this at least led me to know what I was trying to do was possible, but because that repo appears to have been somewhat abandoned I was unable to ask n1nj4 for the methodology used to generate the shellcode.

## My (dll)main mang!

At some point during the process of furiously googling and banging my head against my desk it dawned on me that _memimporter had no dll entrypoint because that's not how python does things. Which made me wonder what would happen if I gave it one. At first it didn't seem to have any real benefit and that may have been partly to do with my lack of knowledge about how python's c api works. Eventually (after much reading of python's docs) I stumbled across a method of injecting the memimporter function directly into the python builtins when the module was imported. Because of a few subtle hints from the [pymemimporter](https://github.com/n1nj4sec/pymemimporter) README, I was able to determine that this was the direction I needed to persue, but where to go from there....

## sRDI to inject

I ended up turning me focus back to a tool I had tried using earlier in my reseach, [sRDI](https://github.com/monoxgas/sRDI). Using sRDI with my newly compiled (self-loading) memimporter, I ended up with some position independant shellcode to try. Using the usual windll api calls I was able to write the dll to memory and cast it as a function. The simple execution of this function results in the addition of memimporter to the python builtins. For a working code example check out my [py3memimporter](https://github.com/rkbennett/py3memimporter) repo, and for those that were waiting for the explanation of how I did it, sorry for the delay.

## How to do this mamba jamba

- `cd` into repo directory
- run `python ./setup.py build` to build binary
- `cd` into the `./build` directory
- `cd` into the subdirectory that begins with `lib`
- start a python interactive shell via `python`
- import functions from ShellcodeRDI `from ShellcodeRDI import *` (https://github.com/monoxgas/sRDI)
- read the generated _memimport pyd `dll = open("_memimporter.cp310-win_amd64.pyd", 'rb').read()` (file name may vary, check the file name in the current directory)
- generate the PIC shellcode `shellcode = ConvertToShellcode(dll)`
- convert the resulting shellcode to a python bytes object
- this bytes object can be pasted into the py3memimport script to replace the existing `buf` bytes variable

## Final thoughts

I'm pretty sure this method could be used for nearly any pyd file in python. Haven't tried any others, but hopefully I'll have planted the seed for someone else to try other ones.

## Special Thanks

[py2exe](https://github.com/py2exe) without you, there wouldn't be a memimporter module

[desty2k](https://github.com/desty2k) for the work you did to create a build file for a standalone memimporter

[n1nj4sec](https://github.com/n1nj4sec) for letting me know it was possible

[natesubra](https://github.com/natesubra) for pushing me to learn more of this stuff

[monoxgas](https://github.com/monoxgas) for the sRDI project which got me across the finish line
