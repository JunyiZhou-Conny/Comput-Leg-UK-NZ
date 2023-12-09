#!/bin/bash
#SBATCH --job-name=writtenQA
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

source ~/.bashrc
conda activate scraper
echo "file=$1 env=qtm"
python -u /home/jjestra/research/computational_legislature/uk/Coding/WrittenQA/$1.py qtm