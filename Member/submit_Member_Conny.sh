#!/bin/bash
#SBATCH --job-name=member
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

source ~/.bashrc
conda activate scraper
echo "env=qtm"
python -u /home/jjestra/research/computational_legislature/uk/Coding/Member/Member.py qtm