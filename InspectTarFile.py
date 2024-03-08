import tarfile

with tarfile.open('Sample/fernando.tar', 'r') as tar:
    for member in tar.getmembers():
        print(member.name)