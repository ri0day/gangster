"""
Write a program that will calculate the number of trailing zeros in a factorial of a given number.

N! = 1 * 2 * 3 * 4 ... N

zeros(12) = 2 # 1 * 2 * 3 .. 12 = 479001600 
that has 2 trailing zeros 4790016(00)
Be careful 1000! has length of 2568 digital numbers.

"""
def zeros(n):
    if n < 2 or not n:
        return n
    r = str(reduce(lambda x,y: x*y ,xrange(1,n+1)))
    count = 0
    print r
    for x in xrange(len(r)-1,-1,-1):
        if r[x] == '0':
            count += 1
        else:
            return count
    return count

print zeros(12)
