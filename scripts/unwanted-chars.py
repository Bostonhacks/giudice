# Find characters that Python can't read so they can be removed
#
# Sometimes Devpost produces unrecognizable chars that give errors,
# so this can be useful in finding where they are when they can't
# be easily seen.
#
# Replace "unwanted" with whatever character causes an error

unwanted = "\xe2" # Put the error char here
with open("tracks.py") as fp:
    for i, line in enumerate(fp):
        if unwanted in line:
            print i, repr(line)