"""

"""

points = (1,3,3,2,1,4,2,4,1,8,10,1,2,1,1,3,8,1,1,1,1,4,10,10,10,10)

def get_best_word(points, words):
    b = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    d = dict(zip(b,points))
    r_list = []
    for word in words:
        r_list.append(str_to_num(d,word))
    r_list = sorted(sorted(r_list,key = lambda x: (x[2])),key = lambda x: (x[1]),reverse =True)
    return words.index(r_list[0][0])
    
    
def str_to_num(d,word):
    temp = 0
    for letter in word:
        temp += d[letter]
    return (word,temp,len(word))


#print get_best_word(points, ["AABCDEF", "WHO","IS","THE","BEST","OF","US"])
#print get_best_word(points, ["NOQ","TXAY","S","OM","ESFT","CJUKQ","QL","QO","ASTK","Y"])
#get_best_word(points, ["N","AO","TQGZW","P","OBTP","CLWXB","Y","JQGFJ","Q","RP","OC","MRQCZ","ZWN","ZRT","OIRYH","GWPMSZP","LQRYUKQ","LBM","LFEI","VHUX","RTALLIC","JEMUPS","XUW","X","ZLXFMWS","LFAGR","HJ","RTUAI","JRBNG","ZUYSC","CIEYV","FUY","B","EJS","CINBTQS","JEAC","JX","LLILSEK","W","KLUV"])
#get_best_word(points, ["SVWLIDP","FCPKTHW","EREMN","NFEF","PQ","FSC","ZYPOSXJ","BOR","YCGG","RC","DVPE","VAOE","OIGK","OTQE","REJFUFD","FVBCSSB","VHJ","BEC","MWZQ","WX","L","ZPCB","JKLHE","RYFTY","NKP","ID","O","KA","VRXX","NTDB","OERKPC","YFLUI","SKQCJ","PXDSW","ITYWD","TC","LOIDQEJ","NE","YND","VJHOCEC","RPRANZ","BQ","STM","RGVBFW","SMWUYLW","KT","SXHY","XCE","T","SC","UDJU","CHDR","UGXNQ","CQOOBA","O","NWW","V","L","BAQ","AZN","LBTR","N","QSURR","KADPH","M","LCBEAKM","ZHEVXS","F","TVAIQCY","MF","KCI","YQ","RCG","AKYPCP","WJXG","RQXOI","SJI","TWXZ","J","HIKCGHV","EAAXGG","AETSH","EO","BUET","TDIQCO","TKL","FJCRY","ZHAJLK","OLMCVA","F"])
#get_best_word(points, ["RBBL","ZJ","ZOFXE","LMBFCFX","O","JG","SYRYE","VXG","EU","DAIFZR","BQUNZHH","WKO","TFPHPLX","SWLG","CY","JYQNDSM","ITPS","B","UVSDMWR","LCPS"])
#get_best_word(points, ['LGVMJDW', 'HSPASA', 'CFHMVZNGH', 'ESKSKB', 'JDO', 'BQJUECZ', 'BB', 'IVVLXBC', 'ZRENSWMG'])


