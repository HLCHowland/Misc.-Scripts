XOR_binary_string = "1110 0000 1001 0111 1110 0111 1111 0110 1101 1101 1111 0100 1101 0000 1000 0101 1100 1010 1100 0011 1000 0100 1110 1001 1001 0111 1000 0000 1000 0000 1110 0100 1100 0011 1001 0111 1000 0100 1110 0010 1001 0100 1101 0110 1000 0100 1001 0101 1001 0000 1001 0101 1001 1100 1001 1101 1111 1011 1110 1100 1111 0011 1001 0101 1000 0100 1001 1110 1000 0100 1111 0111 1101 0001 1100 0111 1100 0111 1100 0001 1101 0111 1101 0111 1000 0101"
XOR_binary_string_list = XOR_binary_string.split()

def xor(a, b, n):
    ans = ""
    for i in range(n):
        if (a[i] == b[i]):
            ans += "0"
        else:
            ans += "1"
    return ans

XORbytes = []
switch = 0
temp = []
for i in XOR_binary_string_list: 
    if switch == 1:
        switch = 0
        temp.append(i)
        mov = xor(''.join(temp), '10100100', 8)
        mov = chr(int(mov, base=2))
        XORbytes.append(mov)
        temp = []
    else:
        temp.append(i)
        switch = 1 

output = []
for r in XORbytes: output.append(r)
output = ''.join(output)
print("\n"+output+"\n")


