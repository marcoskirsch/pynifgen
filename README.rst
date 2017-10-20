Hello @akaszynski

Sorry to contact you via PR, found no better way. Please don't merge.

I'm a software engineer at National Instruments and just ran into akaszynski/pynifgen. It seems it's a fairly new project. I wanted to share with you that I, together with some colleagues, are working on official Python support for NI-FGEN and other modular instruments families. As a matter of fact, we're developing it as Open Source and hosting on GitHub (https://github.com/ni/nimi-python) as well, and some APIs are already available on PyPI and are quite usable: nidmm, nidcpower, niswitch.

You've done some great work here. I am very curious about what / how you're using NI-FGEN and also if you plan to use other products from Python.

The approach we're taking on https://github.com/ni/nimi-python is to use lots of code-generation. This way there's less code to maintain and we ensure consistency across the APIs. It'd be great if you can check it out and we're very open to feedback. Specifically for NI-FGEN we are targeting to upload the first pre-release to PyPI on November 3 (https://github.com/ni/nimi-python/milestone/6).

Marcos
