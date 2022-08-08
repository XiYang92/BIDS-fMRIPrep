# -*- coding: utf-8 -*-
"""Submit jobs to Slurm job scheduler.

"""

import subprocess
import argparse

parser = argparse.ArgumentParser(description='Submit jobs with slurm.')
parser.add_argument(
    'job_file', action='store', help=('A txt file that each line contains a process command.'))
parser.add_argument('queue', action='store', default='fat', help='Queue name.')
parser.add_argument(
    'n_procs', action='store', default=16, type=int, help='Number of cpu cores.')
parser.add_argument(
    'mem', action='store', default=400, type=int, help='memory.')
parser.add_argument('jobname', action='store', default='process', help='Jobname.')
parser.add_argument(
    '--interval_time', '-t', action='store', default=1, help='Interval time between submitting.')
args = parser.parse_args()

src_fn = args.job_file
queue = args.queue
n_procs = args.n_procs
jobname = args.jobname
mem = args.mem * 1000
interval = args.interval_time

with open(src_fn, 'r') as in_file:
    lines = in_file.readlines()
    for idx, line in enumerate(lines):
        header = (f'#!/bin/bash\n\n'
               f'#SBATCH --job-name={jobname}\n'
               f'#SBATCH --account=osl\n'
	       f'#SBATCH --partition={queue}\n'
               f'#SBATCH --nodes=1\n'
               f'#SBATCH --cpus-per-task={n_procs}\n'
               f'#SBATCH --mem={mem}\n'
	       f'#SBATCH --time=1-00:00:00\n'
               f'#SBATCH --output=/projects/osl/xiy/log/{jobname}_job{idx+1:03d}.out\n'
               f'#SBATCH --error=/projects/osl/xiy/log/{jobname}_job{idx+1:03d}.err\n\n'
	       f'module load singularity\n')
        op_string = header + line + '\n'
        print(op_string)

        # Submit job to slurm
        try:
            p = subprocess.run(
                'sbatch',
                shell=True,
                check=True,
                encoding='utf-8',
                input=op_string,
                stdout=subprocess.PIPE)
            print(p.stdout)
            subprocess.run(f'sleep {interval}', shell=True, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as err:
            print('ERROR:', err)


