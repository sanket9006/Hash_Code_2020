import argparse
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

with open(args.input) as f:
    lines = f.read().splitlines()

b, l, d = list(map(int, lines[0].split()))
books = list(map(int, lines[1].split()))
books_map = dict(enumerate(books))

libs = []
for i in range(l):
    lb, lsignup, lship = list(map(int, lines[2*i+2].split()))
    lbooks = list(map(int, lines[2*i+3].split()))
    lscore = 0
    for j in range(lb):
        if j > d * lship:
            break 
        lscore += books[lbooks[j]]
    libs.append({'b': lb, 'signup': lsignup, 'ship': lship, 'score': lscore, 'books': lbooks})


def weighted_score(lib):
    return lib['score'] / lib['signup']

slibs = sorted(enumerate(libs), key=lambda x: - weighted_score(x[1]))

max_l = 0
temp_d = d
while temp_d > 0 and max_l < l:
    temp_d -= slibs[max_l][1]['signup']
    max_l += 1

pre, ext = os.path.splitext(args.input)
rfile = args.output

output = ''
temp_d = d
skipped_l = 0
for i in range(max_l):
    sbooks = []
    for j in range(slibs[i][1]['b']):
        if slibs[i][1]['books'][j] in books_map:
            sbooks.append(slibs[i][1]['books'][j])
    sbooks = sorted(sbooks, key=lambda x: -books[x])
    out_b = min(len(sbooks), slibs[i][1]['ship'] * temp_d)
    if out_b > 0:
        output += str(slibs[i][0]) + ' ' + str(out_b) + '\n'
        for j in range(out_b):
            del books_map[sbooks[j]]
            output += str(sbooks[j])
            if j < out_b - 1:
                output += ' '
        output += '\n'
    else:
        skipped_l += 1
    temp_d -= slibs[i][1]['signup']
output = str(max_l - skipped_l) + '\n' + output

with open(rfile, 'a') as out:
    out.write(output)
