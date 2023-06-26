from math import ceil
power = lambda x : sum([int(i) for i in str(bin(x))[2:]]) == 1
complete = lambda x : list((x[::-1] + '0' * (11 - len(x) % 11)))
hamming = lambda x : [[int(x.pop(0)) if j != 0 and len(x) > 0 else 0 for j in i] for i in [[l if l != 0 and not power(l) else 0 for l in range(0, 16, 1)] for k in range(0, ceil(len(x) / 11))]]
parity = lambda x : [[sum([k for k in i]) if power(j) else j for j in i] for i in x]
print(hamming(complete(str(bin(10000000))[2:])))