#!/bin/bash
#SBATCH --job-name=hansard_onlytxt
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

source ~/.bashrc
conda activate scraper
python -u /home/jjestra/research/computational_legislature/uk/Coding/Hansard/hansard_common_only_txt.py qtm