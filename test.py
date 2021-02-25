import glob

print(len(glob.glob('images/*png')) + len(glob.glob('images/*ico')) + len(glob.glob('images/*gif')))