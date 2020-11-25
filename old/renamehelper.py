import os

path = r'C:\Users\RAUMKOONG\Music\알 수 없는 음악가\Sing Along 5'
destpath = r'D:\Programming\stocktrading\trendanalyzer\singalong5.txt'
files = os.listdir(path)
len(files)
names = open(destpath,'r').readlines()
names = [(i+1 if i>=9 else '0'+str(f'{i+1}'),f.replace('\n','')) for i,f in enumerate(names)]
names = [f'{i} {f}.mp3' for i,f in names]

for s,d in zip(files,names):
    ss = os.path.join(path,s)
    dd = os.path.join(path,d)
    print(ss,'->',dd)
    os.rename(ss,dd)