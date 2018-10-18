import os

S3_DIR="s3://p1apr18/SalmonTE_GTEX"
SAMPLEID_FILE="sra_id.txt"

#get the syn IDs of jobs already run on cluster
doneFileName = 'jobs_finished.txt'
doneList = []
with open(doneFileName, 'r') as handler:
    for line in handler:
        line = line.strip()
        line = line.strip()
        doneList.append(line)


doneList = list(set(doneList))
doneFile = open(doneFileName, 'a')

JOB_SCRIPT = 'run_salmonte.sh'
HOME_DIR = os.getcwd()

#read file and get the sample names
sampleList = []
with open(SAMPLEID_FILE, 'r') as handler:
    sampleList = [l.strip() for l in handler]

maxJobs = 200
for k, sample_id in enumerate(sampleList):
    if sample_id in doneList:
        continue
    print('sample:', sample_id)
    doneFile.write(sample_id + '\n')
    JOB_NAME = 'jp5'+sample_id
    JOB_LOGFILE = HOME_DIR + '/' + sample_id + '_logFile_1.txt'
    print('sample_id:', sample_id, 'JOB_NAME:', JOB_NAME)
    #continue
    #running on cluster
    if 1:
        #pass
            cmd = 'qsub -pe smp 1 -N ' + JOB_NAME + ' ' + JOB_SCRIPT + ' ' + HOME_DIR + ' ' + sample_id  + ' '  + JOB_LOGFILE
            print('qsub cmd:', cmd)
            os.system(cmd)
    #running locally
    if 0:
        cmd = 'sh '  + JOB_SCRIPT + ' ' + HOME_DIR + ' ' + sample_id  + ' '  + JOB_LOGFILE
        print('cmd:', cmd)
        os.system(cmd)

    if k == maxJobs:
        break

doneFile.close()

exit()
