#!/bin/bash



ID=$1

# specify the path of the key
KEY_PWD="$PWD/key.ngc"
S3_DIR="s3://p1apr18/SalmonTE_GTEX"


if [ ! -d "$PWD/sratoolkit.2.9.2-ubuntu64" ]; then
    echo "Downloading sratoolkit..."
    wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.9.2/sratoolkit.2.9.2-ubuntu64.tar.gz
    tar xvzf sratoolkit.2.9.2-ubuntu64.tar.gz
    ./sratoolkit.2.9.2-ubuntu64/bin/vdb-config --import key.ngc $PWD
fi

if [ ! -d "$PWD/fastq" ]; then
    echo "Creating fastq directory..."
    mkdir fastq
fi

if [ ls $PWD/$ID*.fastq 1> /dev/null 2>&1 ]; then
    echo "Run fasterq-dump to download $ID..."
    ./sratoolkit.2.9.2-ubuntu64/bin/fasterq-dump $ID -f -p -e 16 -3 -O $PWD/fastq/
else
    echo "Found FASTQ files... running fasterq-dump is being skipped."
fi

if [ ! -d "$PWD/SalmonTE" ]; then
    echo "cloning SalmonTE..."
    git clone https://github.com/hyunhwaj/SalmonTE
    pip3 install snakemake==5.1.5 docopt pandas --user
else
    echo "SalmonTE has been cloned, and it will not be downloaded again."
fi

echo "Running SalmonTE... for $ID"
python3 SalmonTE/SalmonTE.py quant --reference=hs $PWD/fastq/*.fastq
aws s3 cp $PWD/SalmonTE_output/$ID/quant.sf $S3_DIR/$ID.sf
