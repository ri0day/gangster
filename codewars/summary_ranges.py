def summary_ranges(nums):
    if len(nums) == 0:
        return []
    lst = []
    start = end  = nums[0]
    for  n in (nums[1:]):
        if end + 1 == n or n == end:
            end = n
        else:
            print 'in else'
            lst.append([start,end])
            start = end = n
    if start != None:
        lst.append([start,end])
    return [str(r[0]) if r[0] == r[1] else str(r[0])+'->'+str(r[1]) for r in lst]

print summary_ranges([0, 1, 2, 5, 6, 9])
