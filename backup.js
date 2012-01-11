base = "/data0/backup/"
function showdate(n)  {  
var uom = new Date(new Date()-0+n*86400000);  
uom = uom.getFullYear() + "-" + (uom.getMonth()+1) + "-" + uom.getDate();  
return uom;  
}
db.runCommand({fsync:1,lock:1})
runProgram("cp","-ar","/data0/mongodb/data",base+showdate(0))
db.$cmd.sys.unlock.findOne()
removeFile(base+showdate(-5))
