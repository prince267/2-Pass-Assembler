from sys import argv
import sys
from tabulate import tabulate

reg32=[["eax","000"],["ecx","001"],["edx","010"],["ebx","011"],["ebp","100"],["esp","101"],["esi","110"],["edi","111"]]

#--------------------------------------------------------------------------------------------------------------------------
#symbol and label table
def file_symbol(filename):
    file=open(filename,"r")
    lines=file.readlines()
    line=0
    addr=0
    res_add=0
    lit=1  #literal no
    sym=1   #symbol no
    lbl=1   #lable no
    symbol_table=[]
    label_table=[]
    temp_symbol=[]
    temp_label=[]
    while(line<len(lines)):
        if(" db " in lines[line]):
            temp=lines[line].split(" db ")
            temp[0]=temp[0].strip(" ")
            i=0
            t=""
            if(temp[0] in temp_symbol):
                print(filename," ",line," error: symbol redifned ",temp[0],"\n")
                exit()
            else:
                temp_symbol+=temp[0]
                count=0
                while(i<len(temp[1])):
                    if(temp[1][i]=='"'):
                        i=i+1
                        while(temp[1][i]!='"'):
                            t=t+temp[1][i]
                            i=i+1
                    if(temp[1][i]==","):
                        count+=1
                    i=i+1
                temp[1]=[t]
                symbol_table+=[["sym#"+str(sym),temp[0],addr,1,len(temp[1][0])+count,"lit#"+str(lit),"d",temp[1]]]
                lit+=1
                sym+=1
                addr=addr+len(temp[1][0])+count

        if(" dd " in lines[line]):
            temp=(lines[line].strip().split(" "))
            temp[2]=[int(x) for x in temp[2].split(",")]
            if(temp[0] in temp_symbol):
                print(filename," ",line," error: symbol redifned ",temp[0],"\n")
                exit()
            else:
                temp_symbol+=temp[0]
                symbol_table+=[["sym#"+str(sym),temp[0],addr,4,len(temp[2]),"lit#"+str(lit),"d",temp[2]]]
                lit+=1
                sym+=1
                addr=addr+4*len(temp[2])
        if(" resd " in lines[line]):
            temp=(lines[line].strip().split(" "))
            if(temp[0] in temp_symbol):
                print(filename," ",line," error: symbol redifned ",temp[0],"\n")
                exit()
            else:
                temp_symbol+=temp[0]
                symbol_table+=[["sym#"+str(sym),temp[0],res_add,4,len(temp[1]),"-","d","-"]]
                res_add+=4
        if(" resb " in lines[line]):
            temp=(lines[line].strip().split(" "))
            if(temp[0] in temp_symbol):
                print(filename," ",line," error: symbol redifned ",temp[0],"\n")
                exit()
            else:
                temp_symbol+=temp[0]
                symbol_table+=[["sym#"+str(sym),temp[0],res_add,4,len(temp[1]),"-","d","-"]]
                res_add+=1
        if("global" in lines[line]):
            while(line<len(lines)):
                if("global" in lines[line]):
                    temp=(lines[line].strip().split(" "))
                    temp_label+=[temp[1]]
                    label_table+=[[line,"lable#"+str(lbl),temp[1],"u"]]
                    lbl+=1
                if(":" in lines[line]):
                    temp=lines[line].strip(" ").split(":")
                    if(temp[0] in temp_label):
                        for l in label_table:
                            if(temp[0]==l[2]):
                                l[3]="d"
                    else:
                        label_table+=[[line,"lable#"+str(lbl),temp[0],"u"]]
                        temp_label+=[temp[0]]
                        lbl+=1
                if(" jmp " in lines[line]):
                    temp=lines[line].split("jmp ")
                    temp[1]=temp[1].strip("\n")
                    if(temp[1] in temp_label):

                        for l in label_table:
                            if(temp[1]==l[2]):
                                l[3]="d"
                    else:
                        label_table+=[[line,"lable#"+str(lbl),temp[1],"u"]]
                        temp_label+=[temp[1]]
                        lbl+=1
                if("jnz " in lines[line]):
                    temp=lines[line].split("jmp ")
                    temp[1]=temp[1].strip("\n")
                    if(temp[1] in temp_label):
                        for l in label_table:
                            if(temp[1]==l[2]):
                                l[3]="d"
                    else:
                        label_table+=[[line,"lable#"+str(lbl),temp[1],"u"]]
                        temp_label+=[temp[1]]
                        lbl+=1
                line=line+1
        line=line+1
    return(symbol_table,label_table)

#--------------------------------------------------------------------------------------------------------------------
#literal table
def file_literal(filename,symbol_table,line):
    j=1
    lit_table=[]
    temp_lit=[]
    file=open(filename,"r")
    lines=file.readlines()
    for sym in symbol_table:
        if(sym[7]!="-"):
            if(sym[3]==1):
                t=""
                for i in range(len(sym[7][0])):
                    z=hex(ord(sym[7][0][i]))[2:]
                    if(len(z)==1):
                        z+='0'+z
                    t+=z
                lit_table+=[[sym[5],t,sym[7]]]
                temp_lit+=[sym[7]]
                j=j+1
            else:
                t=[]
                for i in sym[7]:
                    z=hex(i)[2:]
                    if(len(z)==1):
                        z='0'+z
                    t+=[z]
                lit_table+=[[sym[5],t,sym[7]]]
                temp_lit+=[sym[7]]
                j=j+1
    while(line<len(lines)):
        if(":" in lines[line]):
            break
        line+=1
    while(line<len(lines)):
        if(":" in lines[line].replace(" ","") and "," in lines[line]):
            t=lines[line].split(":")[0].replace(" ","")
            lines[line]=(lines[line].replace(t,"")).replace(":","")
        if("," in lines[line]):
            temp=lines[line].split(",")
            temp=temp[0].strip().split(" ")+temp[1].strip().split(" ")
            if(temp[2].isdigit()):
                if(int(temp[2]) not in temp_lit):
                    t=hex(int(temp[2]))[2:]
                    if(len(t)==1):
                        t='0'+t
                    lit_table+=[["lit#"+str(j),t,int(temp[2])]]
                    temp_lit+=[int(temp[2])]
                    j=j+1
        if("dword" in lines[line]):
            if("+" in lines[line] or "*" in lines[line]):
                temp=lines[line].split("dword")
                temp=temp[1].replace(" ","")
                temp=temp.replace("+",",").replace("*","").replace("[","").replace("]","")
                temp=temp[1:]
                for t in temp:
                    if(t.isdigit()):
                        if(int(t) not in temp_lit):
                            t1=hex(int(t))[2:]
                            if(len(t1)==1):
                                t1='0'+t1
                            lit_table+=[["lit#"+str(j),t1,int(t)]]
                            temp_lit+=[int(t)]
                            j=j+1


        line=line+1
    return(lit_table)
#-----------------------------------------------------------------------------------------------------------------------
#inetermmediate file
def file_intermediat(filename,symbol_table,lit_table,d):
    i_file=open(filename.split(".")[0]+'.i',"w")
    file=open(filename,"r")
    lines=file.readlines()
    line=0
    t=0
    temp_reg=[x[0] for x in reg32]
    temp_lit=[str(x[2]) for x in lit_table]
    temp_sym=[x[1].replace("\t","") for x in symbol_table]
    while(line<d):
        if " dd " in lines[line]:
            text_split=lines[line].split(" dd ")

            temp=lines[line][:len(text_split[0])+1]
            temp_t1=temp.replace(" ","").replace("\t","")
            temp1=lines[line].split("dd")
            temp1[1]=temp1[1].replace(" ","").replace("\n","")
            temp_t=temp1[1]
            temp1[1]=("["+temp1[1]+"]").replace(",",", ")
            lines[line]=temp.replace(temp_t1,"sym#"+str(temp_sym.index(temp_t1)+1))+lines[line][len(text_split[0])+1:].replace(temp_t,"lit#"+str(temp_lit.index(temp1[1])+1))

        if " db " in lines[line]:
            text_split=lines[line].split(" db ")
            temp=lines[line][:len(text_split[0])+1]
            temp_t1=temp.replace(" ","").replace("\t","")
            temp1=text_split[1][(" "+text_split[1]).index('"'):]
            temp_t=temp1
            temp1="['"+temp1[:temp1.index('"')]+"']"
            lines[line]=(temp.replace(temp_t1,"sym#"+str(temp_sym.index(temp_t1)+1))+lines[line][len(text_split[0])+1:].replace(temp_t,"lit#"+str(temp_lit.index(temp1)+1))).replace('"',"")

        if (" resb " in lines[line] or " resd " in lines[line]):
            if(" resb " in lines[line]):
                text_split=lines[line].split(" resb ")
                t=" resb "
            else:
                text_split=lines[line].split(" resd ")
                t=" resd "
            temp=text_split[0].replace(" ","").replace("\t","")
            lines[line]=text_split[0].replace(temp,"sym#"+str(temp_sym.index(temp)))+t+text_split[1]
        lines[line]=lines[line].replace("\n","")
        i_file.write(lines[line])
        i_file.write("\n")
        line=line+1

    while(d<len(lines)):
        for r in temp_reg:
            lines[d]=lines[d].replace(r,"reg#"+str(temp_reg.index(r)))


        temp=lines[d].split(",")
        if(len(temp)>1):
            temp1=temp[1].replace(" ","").replace("\n","").replace("\t","")
            if(temp1 in temp_sym):
                lines[d]=temp[0]+",sym#"+str(temp_sym.index(temp1)+1)
            if(temp1 in temp_lit):
                lines[d]=temp[0]+","+temp[1].replace(temp1,"lit#"+str(temp_lit.index(temp1)+1))

            if("dword" in temp1):
                temp2=temp1.replace("dword","").replace("[","").replace("]","").replace("\n","")
                if("+" in temp2 or "*" in temp2):
                    temp2=temp2.replace("+",",").replace("*",",")
                    temp2=temp2.split(",")
                    temp2[1]=temp2[1].replace(temp2[1],"lit#"+str(temp_lit.index(temp2[1])+1))
                    temp2[2]=temp2[2].replace(temp2[2],"lit#"+str(temp_lit.index(temp2[2])+1))
                    lines[d]=temp[0]+",val["+temp2[0]+","+temp2[1]+","+temp2[2]+"]"

                else:
                    temp2=temp2.replace(temp2,"sym#"+str(temp_sym.index(temp2)+1))
                    lines[d]=temp[0]+",val["+temp2+",lit#"+temp2[4:]+"_01]"
        else:
            temp=temp[0]
            if("dword" in temp):
                temp=temp.split("dword")
                temp[1]=temp[1].replace("[","").replace("]","").replace("\n","")
                temp[1]=temp[1].replace(temp[1],"sym#"+str(temp_sym.index(temp[1])+1))
                lines[d]=temp[0]+"val["+temp[1]+"]"
            else:
                temp=temp.split(" ")
                if(len(temp)>1):
                    temp[1]=temp[1].replace(" ","").replace("\n","")
                    if(temp[1] in temp_sym):
                        temp[1]=temp[1].replace(temp[1],"sym#"+str(temp_sym.index(temp[1])+1))
                    lines[d]=temp[0]+" "+temp[1]
        lines[d]=lines[d].replace("\n","")
        i_file.write(lines[d])
        i_file.write("\n")
        d+=1
#-------------------------------------------------------------------------------------------------------------------------
#lst file
def file_lst(filename,iter_file,symbol_table,lit_table,d):
    file=open(filename,"r")
    lines=file.readlines()
    file1=open(iter_file,"r")
    lines1=file1.readlines()
    line=0
    temp_reg=[x[0] for x in reg32]
    temp_lit=[str(x[2]) for x in lit_table]
    temp_sym=[x[1].replace("\t","") for x in symbol_table]
    while(line<d):
        if("dd" in lines1[line]):
            temp=lines1[line].split("dd")
            temp[0]=temp[0].replace("\t","").replace(" ","")
            addr=symbol_table[int(temp[0][4:])-1][2]
            t=hex(addr)[2:]
            t1="0"*(8-len(t))
            addr=t1+t+"  "
            t=""
            lit=lit_table[int(temp[0][4:])-1][1]
            for lit1 in lit:
                t=t+lit1+"0"*(8-len(lit1))
            t4=str(line+1)+" "+addr+t+"  "
            print(t4+lines[line].strip(" ").replace("\t",""))
        elif("db" in lines[line]):
            temp=lines1[line].split("db")
            temp[0]=temp[0].replace("\t","").replace(" ","")
            addr=symbol_table[int(temp[0][4:])-1][2]
            t=hex(addr)[2:]
            t1="0"*(8-len(t))
            addr=t1+t+"  "
            lit=lit_table[int(temp[0][4:])-1][1]
            t4=str(line+1)+" "+addr+lit+"0a00"
            print(t4+lines[line])
        elif("resb" in lines1[line] or "resd" in lines1[line]):
            if("resb" in lines1[line]):
                temp=lines1[line].split("resb")
                temp[0]=temp[0].replace("\t","").replace(" ","")
                addr=symbol_table[int(temp[0][4:])-1][2]
                t=hex(addr)[2:]
                t1="0"*(8-len(t))
                addr=t1+t+"\t"
                temp[1]=temp[1].replace("\n","").replace(" ","")
                temp[1]=hex(int(temp[1]))[2:]
                t2="0"*(8-len(temp[1]))+temp[1]
                t2="<res "+t2+" >"
                lines[line].replace("\t","")
                t4=str(line+1)+" "+addr+t2+"  "
                print(t4+lines[line])
        else:
            t4=str(line+1)+" "
            print(t4+lines[line])
        line+=1
    while(line<len(lines1)):
        if(":" in lines1[line]):
            break
        t4=str(line+1)+" "
        print(t4+lines[line])
        line+=1
    n=0
    while(line<len(lines1)):
        if("mov" in lines1[line]):
            temp=lines1[line].replace("mov","").replace(" ","")
            temp=temp.split(",")
            temp[0]=temp[0].replace("\t","")
            temp[1]=temp[1].replace("\n","")
            if(temp[1][:4]=="lit#"):
                t=hex(184+int(temp[0][4:]))[2:]
                lit=lit_table[int(temp[1][4:])-1][1]
                r=lit+"0"*(8-len(lit))
                t2=t+r
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
            elif(temp[0][:4]=="reg#" and temp[1][:4]=="reg#"):
                t1="11"+reg32[int(temp[1][4:])][1]+reg32[int(temp[0][4:])][1]
                t2="89"+hex(int(t1,2))[2:]
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
            elif("val" in temp[1]):
                temp[1]=temp[1].replace("val[","")
                if(temp[1][:4]=="sym#"):
                    d=hex(symbol_table[int(temp[1][4:])-1][2])[2:]
                    if(len(d)==1):
                        d="0"+d
                    d=d+"0"*(8-len(d))
                    if(temp[0]=="reg#0"):
                        t2="A1["+d+"]"
                        t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                        str(line+1)+" "+t3+"  "+t2
                        print(t4+lines[line])
                        n=n+len(t2.replace("[","").replace("]",""))/2
                    else:
                        t1="00"+reg32[int(temp[0][4:])][1]+"101"
                        t2="8B"+hex(int(t1,2))[2:]+"["+d+"]"
                        t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                        t4=str(line+1)+" "+t3+"  "+t2
                        print(t4+lines[line])
                        n=n+len(t2.replace("[","").replace("]",""))/2
            elif(temp[0][:4]=="reg#" and temp[1][:4]=="sym#"):
                t=hex(184+int(temp[0][4:]))[2:]
                d=hex(symbol_table[int(temp[1][4:])-1][2])[2:]
                if(len(d)==1):
                    d="0"+d
                d=d+"0"*(8-len(d))
                t2=t+"["+d+"]"
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2-2





        if("add" in lines1[line]):
            temp=lines1[line].replace("add","").replace(" ","")
            temp=temp.split(",")
            temp[0]=temp[0].replace("\t","")
            temp[1]=temp[1].replace("\n","")
            if(temp[0][:4]=="reg#" and temp[1][:4]=="reg#"):
                t1="11"+reg32[int(temp[1][4:])][1]+reg32[int(temp[0][4:])][1]
                t2="01"+hex(int(t1,2))[2:]
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
            if(temp[1][:4]=="lit#"):
                t2="83C"+temp[0][4:]+lit_table[int(temp[1][4:])-1][1]
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
        if("sub" in lines1[line]):
            temp=lines1[line].replace("sub","").replace(" ","")
            temp=temp.split(",")
            temp[0]=temp[0].replace("\t","")
            temp[1]=temp[1].replace("\n","")
            if(temp[0][:4]=="reg#" and temp[1][:4]=="reg#"):
                t1="11"+reg32[int(temp[1][4:])][1]+reg32[int(temp[0][4:])][1]
                t2="29"+hex(int(t1,2))[2:]
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
            if(temp[1][:4]=="lit#"):
                t2="83E"+hex(8+int(temp[0][4:]))[2:]+lit_table[int(temp[1][4:])-1][1]
                t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
                t4=str(line+1)+" "+t3+"  "+t2
                print(t4+lines[line])
                n=n+len(t2)/2
        if(len(temp)>3):
            temp[3]=temp[3].replace("\n","").replace("]","")
            t="01"+reg32[int(temp[0][4:])][1]+reg32[int(temp[1][4:])][1]
            t2="8B"+hex(int(t,2))[2:]+"04"
            t3="0"*(8-len(hex(n)[2:]))+hex(n)[2:]
            t4=str(line+1)+" "+t3+"  "+t2
            print(t4+lines[line])
            n=n+len(t2)/2
        line+=1

#--------------------------------------------------------------------------------------------------------------------------
#driver code

if __name__ == '__main__':
    filename=argv[2]
    t=argv[1]
    symbol_table,label_table=file_symbol(filename)

    lit_table=file_literal(filename,symbol_table,label_table[0][0])

    if(argv[1]=="-s"):
        print("\n\t\t\t\t\t\tSymbol_Table\n")
        print(tabulate(symbol_table, headers=["symbol","name","address","size","length","literal","defOrUndef","value"]))
        print("\n\n\t\t\t\t\t\tLabel_Table\n")
        print(tabulate(label_table, headers=['line', 'lable_no','name',"defOrUndef"]))
    elif(argv[1]=="-l"):
        print(tabulate(lit_table, headers=['literalNo', 'hex','value']))
    elif(argv[1]=="-i"):
        print("Intermmediate File "+filename.split(".")[0]+".i"+" created\n")
        file_intermediat(filename,symbol_table,lit_table,label_table[0][0])
    elif(argv[1]=="-lst"):
        print("Lst File "+filename.split(".")[0]+".lst"+" created\n")
        file_intermediat(filename,symbol_table,lit_table,label_table[0][0])
        file_lst(filename,filename.split(".")[0]+".i",symbol_table,lit_table,label_table[0][0])
