#!/bin/bash
#SBATCH --job-name=oral_questions
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

source ~/.bashrc
conda activate scraper
python -u /home/jjestra/research/computational_legislature/uk/Coding/OralQuestions/OralQuestions.py qtm