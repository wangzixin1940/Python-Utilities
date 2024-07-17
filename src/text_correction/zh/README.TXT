Q: The download model (2.7 GB) is too slow. How do I use my multi-threaded download tool to download models?
A: You can try it:
    1. Download the model from  https://deepspeech.bj.bcebos.com/zh_lm/zh_giga.no_cna_cmn.prune01244.klm (2.7 GB).
    2. Then put it to /path/to/your/user/folder/.pycorrector/datasets
    3. Enjoy!

Q: I have a ready-made model. How can I use it in the program?
A: You can try it:
    Method 1:
        1. Put your model to /path/to/your/user/folder/.pycorrector/datasets
        2. Rename your model file to zh_giga.no_cna_cmn.prune01244.klm
        3. Enjoy!
    Method 2:
        1. Find line 42 of main.py (corrector = Corrector())
        2. Modify it to: "corrector = Corrector(language_model_path="/path/to/your/model/model.klm")" (NO need for the outermost double quotation marks)
        3. Enjoy!