# GSOC22_Tools-for-improving-subtitle-caption-quality
[![Status](https://img.shields.io/badge/status-active-success.svg)]() 
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

## About
This is a tool to detect word errors and grammatical errors for CCExtractor files. This tool basically takes generated txt file from CCExtractor as input and gives another txt file that contains the lines of error, original errors, and suggestions for correctness.

This GSoC project [Tools-for-improving-subtitle-caption-quality](https://summerofcode.withgoogle.com/programs/2022/projects/GJVsyb6V) is contributed by Qing with [Red Hen Lab](https://www.redhenlab.org/home), under the supervision from Rosa Illán.

## Prerequests
If you only want to get a better Spanish dictionary for Hunspell, you can download these two files and put them into your own machine:
```
/spell/dictionary/es_red.aff
/spell/dictionary/es_red.dic
```


Installing all the packages from the requirements.txt file to the virtual environment:
```
pip install -r requirements.txt
```

For grammar checker, you should download the trained mT5 model with the name "pytorch_model.bin", and put it into ./grammar/model. Here is the link to the model:
```
https://drive.google.com/drive/folders/1C9PttRNQyDYjuhhURT8PjaRZ0BqbG-vH
```


## Introduction
This project is aimed to improve offer both spell and grammar checkers to support the daily research of Red Hen Lab. 

Red Hen Lab uses Hunspell as their spell checker, but the original Hunspell reports right spelling as wrong frequently. To solve this problem, I add the NER function and an extra English word recognition function to the Hunspell. Besides, I used some simple methods like combining dictionaries and extending dictionaries to get a better dictionary that suits the daily life of Red Hen Lab.

For the grammar checker, I choose a Huggingface model which was continued pre-trained under the Spanish [CC-NEWS-ES-titles](https://huggingface.co/datasets/LeoCordoba/CC-NEWS-ES-titles) dataset, then fine-tune this model under the [cowsl2h](https://github.com/ucdaviscl/cowsl2h) grammar error correction (GER) dataset. But the GER dataset was created by using foreign students who just learn Spanish for a short time, this domain differs from news dramatically, so it didn't perform well. I will try to find a better GER dataset and try other methods later.

The detailed working of this tool is included in the final submission blog.

## Usage Spell Checker
The usage of this is very simple. You can use the spell checker easily by following:
```
python3 cospell.py --file './test_file/ES_test.txt' --language 'es' --dictionary 'es_red'
```
If you want to save the output, just save the output of the terminal to a file in such a way:
```
python3 cospell.py --file './test_file/ES_test.txt' --lag 'es' --dict es_red > 'output.txt'
```

## Usage Grammar Checker
Here is an example of using the grammar checker to test the sentence under the test file.
```
python3 grammar.py --file './test_file/ES_test.txt'
```