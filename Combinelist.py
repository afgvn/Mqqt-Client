

mlist = [] 
wlist = []
rlist = []
nm=7
nw=9


def rec ( var1 ,var2 , var3):
    
     count =  0 
     print("tesr start  " + str( len( rlist ) ) + " "+ var1 + " " +  var2 + " " +  var3    )

     flagspace=0
     count =  0 
     count2 =  0
     count3 =  0

     for x in  range(0, len( rlist )  , 1 ):
        
        vart= rlist[x].split()
        count =  0 
        count2 =  0
        count3 =  0
        

        
        if ( vart[0] == var1 or vart[0] == var2 or vart[0] == var3 ) :
            count =  1 
            #print("add 1")

        if ( vart[1] == var1 or vart[1] == var2 or vart[1] == var3 ) :
            count2 =  1
            #print("add 2") 

        if ( vart[2] == var1 or vart[2] == var2 or vart[2] == var3 ) :
            count3 = 1 
            #print("add 3")
        
        #print(rlist[x])
        #print("----" + var1 + " " +  var2 + " " +  var3  + " " + str((count + count2 + count3 )))

        if (count and count2 and  count3 ) == 3:
            flagspace = 1
            break


     if flagspace == 0 :

        #print("++++" + var1 + " " +  var2 + " " +  var3  + " " + str((count + count2 + count3 )))
        rlist.append( var1 + " " +  var2 + " " +  var3  + " " + str((count + count2 + count3 )))


     if len( rlist ) == 0 :
         
        rlist.append( var1 + " " +  var2 + " " +  var3  )
      



for x in  range(1,nm + 1 , 1):
    print (x)  
    wlist.append("m" + str(x) )

for x in  range(1, nw + 1 , 1 ):
    print (x)  
    mlist.append("w" + str(x) )



for x in  range(0, len( wlist )  , 1 ):
    for y in  range(0, len( mlist )  , 1 ):

        rec(wlist[x], mlist[y-1] , mlist[y]) 


for x in  range(0, len( mlist )  , 1 ):
    for y in  range(0, len( wlist )  , 1 ):
        rec(mlist[x], wlist[y-1]  ,  wlist[y]) 



print (wlist)
print (mlist)
print (rlist)