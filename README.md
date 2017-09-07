# Download script for Human Connectome Project (HCP-1200 release) data

This is a script to download the HCP-1200 subjects release.  For more information on the Human Connectome Project, see [their website](http://www.humanconnectome.org/).  The script is based on a script to download the [enhanced NKI data](https://github.com/FCP-INDI/rocklandsample/blob/master/download_rockland_raw_bids.py).  

[//]: # (I have written this script for personal use, but maybe other people can use it.  I don't provide support, nor am I related to the team collecting and processing the data.)

It's definitely suboptimal (as in: it's not very flexible), so in case someone wants to make it better, feel free :-)

#### Using the script
The script runs in python 2.7 and requires the following dependencies:
- pandas
- boto3
- shutil
- tarfile

#### HCP S3 credentials
To use this script, you need to create HCP credentials.  You'll need to accept the terms of data usage as well.  You can do so by following (the beginning of) this tutorial: https://wiki.humanconnectome.org/display/PublicData/How+To+Connect+to+Connectome+Data+via+AWS).

Once you have generated your credentials, create or append the following to `~/.aws/credentials`:
```
[hcp]
AWS_ACCESS_KEY_ID=XXXXXXXXX
AWS_SECRET_ACCES_KEY=XXXXXXXXXX
```
(of course you need to replace XXXXXXX with your credentials ;-) )


#### Example

The python runs for each subject separate, and requires the subject code as input (see `utils/subjects.txt` for all subject codes):

```
python download_HCP_1200.py --subject=996782 --out_dir=/data/output/
```

#### Select modalities / data
In an ugly but working attempt to only download a part of the data, you can comment out parts of line 15-22.

#### Create tarballs
You probably won't need this, but because the cluster I'm using (Stanford's [sherlock](http://sherlock.stanford.edu/)) has a limit on the number of files per user, and the HCP data has **a HUGE** amount of files, I've put in an extra argument `tartasks` that will make tarballs with the coregistered and processed task data for each task.  For example:

```
python download_HCP_1200.py --subject=996782 --out_dir=/data/output/ --tartasks
```

#### Use on SLURM scheduler
I mostly run my jobs in array jobs on a cluster.  This sets an environment variable `$SLURM_ARRAY_TASK_ID` (an integer).  The script `utils/get_subject.py` will grab that integer and transform it into a subject code.  This setup is *not* required to run this script, but it makes it definitely easier :-)

For example, I would run this command:

```
sbatch --array=0-1119 download_HCP_1200.sh
```

This is going to launch 1120 jobs (1 for each subject), where `download_HCP_1200.sh` could be:
```
#!/bin/bash
#SBATCH --job-name=HCP_download
#SBATCH --time=4:00:00

module load system
module load py-scipystack/1.0_py27

SUBJECT=$(python utils/get_subject.py 2>&1)

python download_HCP_1200.py --subject=$SUBJECT --out_dir=/data/output/ --tartasks

```
