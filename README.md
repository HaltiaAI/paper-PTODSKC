# paper-PTODSKC
This repository contains code and access to the dataset used for our paper titled `Prompt-Time Ontology-Driven Symbolic Knowledge Capture with Large Language Models`. This document is intended for researchers, developers and those who would like to build, run, and experiment with paper-PTODSKC.

## Prerequisites and Dependencies

* requires M series Apple silicon 
* Requires native Python 3.8 - 3.11. In our work, we utilized the system-managed Python installation on macOS, located at `/usr/bin/python3`, which is pre-installed with the operating system. To use it, you can either create aliases for `/usr/bin/python3` and `/usr/bin/pip3` as `python` and `pip` or directly reference them in every command involving `python` or `pip`. It's important to note that if you opt to use a different version of Python, you will need to update the Python path in `runBenchmarks.py` and `fineTunedShot.py`.
* requires macOS>= 13.3, Please note that MLX platform developers highly recommend using macOS 14 (Sonoma)

## Installation

`mlx-lm` is available on [PyPI]. Please refer to the official [MLX documentation] and  [MLX examples] for more details on the MLX platform.  
To install the Python API, run:

```bash
pip install mlx-lm
```

## How To Use

### Fine-tuning datasets
Datasets needed to generate the KC QLoRA adapter exists under the `data` directory. `base.jsonl` file under this directory is the fundamental dataset used for the training and testing. 

`data/train.jsonl`, `data/test.jsonl`, and `data/valid.jsonl` files holds the user-prompts and prompt response pairs for train, test and validation datasets for the entire fine-tuning set, respectively.`data/2/`, `data/4/`, and `data/8/` folders holds the same structure for 2, 4, and 8 prompts per ontology concepts that are used in the performance evaluation section of the paper.

* Please note that test and validation sets holds the same prompts to be able to ease the control the quality of the QLoRA adapter generation process. 

### Generating ground-truth file
`generateGroundTruth.py` script processes the `data/test.jsonl` file line-by-line and writes the expected prompt response for each user input to a separate file under `results/test_ground_truth_output/`. The output of each line is written to a different file in the followign format, first line's output is written to 1.ttl file etc... The generated ground-truth file will be used in performance evaluations.

To generate the `results/test_ground_truth.jsonl`file, run the following command:
```bash
python scripts/generateGroundTruth.py 
```

### Model file
In our work, we utilize the 4-bit quantized and mlx-converted version of the Mistral-7B-Instruct-v0.2 model. All model files must be placed under the `model/Mistral-7B-Instruct-v0.2-4bit-mlx` folder located in the main directory of our repository. To replicate our test results accurately, please download the mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx file from the mlx-community on Hugging Face and ensure it is placed in the specified path.

### Adaptors
The generated QLoRA adapters are saved under the `adapters/` directory. You can find the QLoRA adapters used in the paper under this directory. 

### Fine-tuning
QLoRA adapter creation can be done with the following command. Please feel free to update the QLoRA training parameters:

```bash
python -m mlx_lm.lora --train --model model/Mistral-7B-Instruct-v0.2-4bit-mlx --iters 600 --data ./data --batch-size 4 --lora-layers 16 --adapter-file adapters/adapters_b4_l16_i600_ts134_mistral_I_v02_4b.npz
```

### Running the benchmarks
To be able to evaluate the generated adapter with the model please use the `runBenchmarks.py` script with `--model-path` and `--adapter-path` arguments. This script calls `fineTunedShot.py`, reading input from `data/test.jsonl` and writing the results to the `results/test_evaluation_output/` directory.

```bash
python scripts/runBenchmarks.py --model-path model/Mistral-7B-Instruct-v0.2-4bit-mlx --adapter-path adapters/adapters_b4_l16_i612_ts68_mistral_I_v02_.npz
```

### Evaluation
`calculateF1Score.py` script compares each method's result file with the ground-truth file and calculates precision, recall and f1-score. All results are written to the `evaluation_results.txt` file under `results` directory.
```bash
python scripts/calculateF1Score.py
```

## Troubleshooting
* if any script complains about jinja2 library please install it separately using the following command:
```bash
pip install jinja2
```

[PyPI]: https://pypi.org/project/mlx-lm/
[MLX documentation]: https://ml-explore.github.io/mlx/build/html/install.html
[MLX examples]: https://github.com/ml-explore/mlx-examples
[mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx]: https://huggingface.co/mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx/tree/main

### Cite

```bash
@misc{coplu2024ontologydriven,
      title={Prompt-{Time} {Ontology}-{Driven} {Symbolic} {Knowledge} {Capture} with {Large} {Language} {Models}},
      author={Tolga Çöplü and Arto Bendiken and Andrii Skomorokhov and Eduard Bateiko and Stephen Cobb},
      year={2024},
      eprint={2405.14012},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```