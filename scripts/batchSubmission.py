#!/usr/bin/env python

import sys
import os
import subprocess
import math
import time
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="Submit array jobs to ifarm.")
parser.add_argument("-a", dest="account", action="store", required=True, help="Enter the Jefferson Lab account. Example: halla")  
parser.add_argument("-s", dest="src", action="store", required=False, default="~/projects/rrg-jmammei/REMOLL/remoll_version", help="source folder where simulation directory exists")
parser.add_argument("-v", dest="version", action="store", required=False, default="real_shield", help= "choose the version of simulation to use.")
parser.add_argument("-j", dest="jsub_dir", action="store", required=True, help="choose directory to write the slurm submission scripts")
parser.add_argument("-t", dest="tmp_dir", action="store", required=True, help="choose directory to write the slurm output logs")
parser.add_argument("-o", dest="out_dir", action="store", required=True, help="choose where to write the output root files")
parser.add_argument("-r", dest="run_range", action = "store", required=False, default="1", help="provide run range. Example: \"2-5\"")
parser.add_argument("-n", dest="n_events", action= "store", required=False, default=1000, help= "provide number of events per job in the array")
parser.add_argument("--time", dest="time", action= "store", required= False, default= "00:25:00", help= "provide the estimated run time. Ex: \"00:25:00\". Usually it is 10 minutes for 1000 moller events.")
parser.add_argument("-w", dest="work_dir", action="store", required=False, default="/scratch/slurm", help="Enter location where analysis takes place. Choose: /scratch/slurm.")

args=parser.parse_args()

args.work_dir=os.path.realpath(args.work_dir)
args.src=os.path.realpath(args.src)

if not os.path.exists(args.jsub_dir):
        os.system("mkdir -p "+args.jsub_dir)
if not os.path.exists(args.tmp_dir):
        os.system("mkdir -p "+args.tmp_dir)
if not os.path.exists(args.out_dir):
        os.system("mkdir -p "+args.out_dir)
if not os.path.exists(args.work_dir):
        os.system("mkdir -p "+args.work_dir)
args.tmp_dir=os.path.realpath(args.tmp_dir)
args.jsub_dir=os.path.realpath(args.jsub_dir)
out=os.path.realpath(args.out_dir)

EventHitRegion = str(4)
LightGuideLowerConeBackAngle = str(np.random.uniform(-60,60)) + " deg"
LightGuideLowerConeFrontAngle = str(np.random.uniform(-60,60)) + " deg"
LightGuideLowerInterface = str(np.random.uniform(0,20)) + " cm"
LightGuideUpperInterface = str(np.random.uniform(0,650)) + " mm"
LightGuidePMTInterfaceOpeningX = str(np.random.uniform(0,20)) + " cm"
LightGuidePMTInterfaceOpeningZ = str(np.random.uniform(0,20)) + " cm"
QuartzSizeZ = str(np.random.uniform(5,30)) + " mm"
QuartzSizeX = str(np.random.uniform(30,120)) + " mm"
QuartzSizeY = str(np.random.uniform(30,200)) + " mm"
QuartzBevelSize = str(0) + " mm"
QuartzRotX = str(-3) + " deg"
PolarRotation = str(3) + " deg"
LightGuideQuartzToPMTOffset = str(0) + " mm"
		
jsubf=open(args.jsub_dir+"/"+args.gen+".sh", "w")
jsubf.write("#!/bin/bash\n")
jsubf.write("#SBATCH --account="+args.account+"\n")
jsubf.write("#SBATCH --partition=production\n")
jsubf.write("#SBATCH --job-name=molleropt\n")
jsubf.write("#SBATCH --time="+args.time+" \n")
jsubf.write("#SBATCH --nodes=1\n")
jsubf.write("#SBATCH --ntasks=1\n")
jsubf.write("#SBATCH --cpus-per-task=1\n")
jsubf.write("#SBATCH --mem=4G\n")
jsubf.write("#SBATCH --output="+args.tmp_dir+"/"+args.gen+"_%A_%a.out\n")
jsubf.write("#SBATCH --chdir="+args.work_dir+"\n")
jsubf.write("cd ${SLURM_JOB_ID}\n")
jsubf.write("mkdir ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}\n")
jsubf.write("cd ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}\n")
macro=args.work_dir+"/${SLURM_JOB_ID}/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}/run"+args.r+".mac"
jsubf.write("touch "+macro+"\n")
jsubf.write("echo /Det/LightGuideLowerConeBackAngle "+LightGuideLowerConeBackAngle+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuideLowerConeFrontAngle "+LightGuideLowerConeFrontAngle+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuideLowerInterface "+LightGuideLowerInterface+" >>"+macro+"\n") 
jsubf.write("echo /Det/LightGuideUpperInterface "+LightGuideUpperInterface+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuidePMTInterfaceOpeningX "+LightGuidePMTInterfaceOpeningX+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuidePMTInterfaceOpeningZ "+LightGuidePMTInterfaceOpeningZ+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuideQuartzInterfaceOpeningX "+LightGuideQuartzInterfaceOpeningX+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuideQuartzInterfaceOpeningZ "+LightGuideQuartzInterfaceOpeningZ+" >>"+macro+"\n")	
jsubf.write("echo /Det/QuartzSizeZ "+QuartzSizeZ+" >>"+macro+"\n")
jsubf.write("echo /Det/QuartzSizeX "+QuartzSizeX+" >>"+macro+"\n")
jsubf.write("echo /Det/QuartzSizeY "+QuartzSizeY+" >>"+macro+"\n")
jsubf.write("echo /Det/QuartzBevelSize "+QuartzBevelSize+" >>"+macro+"\n")
jsubf.write("echo /Det/QuartzRotX "+QuartzRotX+" >>"+macro+"\n")
jsubf.write("echo /Det/PolarRotation "+PolarRotation+" >>"+macro+"\n")
jsubf.write("echo /Det/LightGuideQuartzToPMTOffset "+LightGuideQuartzToPMTOffset+" >>"+macro+"\n")
jsubf.write("echo /Det/UpdateGeometry >>"+macro+"\n")
jsubf.write("echo /Generator/EventHitRegion "+EventHitRegion+" >>"+macro+"\n")
jsubf.write("echo /RunAction/SetID "+args.r+" >>"+macro+"\n")
jsubf.write("echo /random/setSeeds ${SLURM_ARRAY_JOB_ID}${SLURM_ARRAY_TASK_ID} ${SLURM_ARRAY_TASK_ID}${SLURM_ARRAY_JOB_ID} >>"+macro+"\n")
jsubf.write("echo /run/beamOn "+str(args.n_events)+" >>"+macro+"\n")  
jsubf.write("cat "+macro+"\n")
jsubf.write("cp -r "+args.src+"/"+args.version+" .\n")
jsubf.write("cd "+args.version+" \n")
jsubf.write("echo \"Current working directory is `pwd`\"\n")
jsubf.write("./build/MOLLEROpt ../run"+args.r+".mac\n")
jsubf.write("echo \"Program remoll finished with exit code $? at: `date`\"\n")
jsubf.write("cp "+args.work_dir+"/${SLURM_JOB_ID}/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}/*.root "+out+"\n")
jsubf.write("rm -rf "+args.work_dir+"/${SLURM_JOB_ID}/${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}")

jsubf.close()
	        
                
subprocess.call("sbatch --array="+args.run_range+" "+args.jsub_dir+"/run"+args.r+".sh",shell=True)