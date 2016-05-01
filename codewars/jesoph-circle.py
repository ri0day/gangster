def solve(n,m):  
    list=range(n)  
    m -= 1  
    k=m%n;  
    while(len(list) >1):  
        print "in while k == %d , m == %d"%(k,m)
        del list[k]  
        k= (k+m) % len(list)  
        print list
    return list[0] 

print solve(41,3)


