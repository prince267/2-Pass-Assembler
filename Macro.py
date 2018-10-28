from sys import argv
import sys

def macro_tabel(filename):
    file=open(filename,"r")
    lines=file.readlines()
    line=0
    macros=[]
    while(line<len(lines)):
        if("section" in lines[line] or "data" in lines[line] or "text" in lines[line] or "bss" in lines[line]):
            break
        if("%macro" in lines[line]):
            temp=(lines[line].strip().split(" "))
            start=line
            while("%endmacro" not in lines[line]):
                line+=1
            end=line
            macros+=[[temp[1],temp[2],start,end]]
        line=line+1
    macros=macros[::-1]
    #print(macros)
    return(macros,line)

def macro_apply(filename,macros,n):
    file=open(filename,"r")
    lines=file.readlines()
    line=0
    new_file=[]
    temp_macros=[]
    new_macro=[]
    for mcrs in macros:
        if([mcrs[0],mcrs[1]] not in temp_macros):
            new_macro+=[mcrs]
            temp_macros+=[[mcrs[0],mcrs[1]]]
    #print(new_macro)
    #print(temp_macros)

    while(line<n):
        print(lines[line])
        line+=1

    while(line<len(lines)):
        temp=lines[line].strip(" ").split(" ")
        temp[0]=temp[0].replace("\n","").replace("\t","")
        if(temp[0] in [c[0] for c in temp_macros]):
            temp[1]=temp[1].replace("\n","").replace("\t","")
            temp[1]=temp[1].split(",")
            l=str(len(temp[1]))
            temp1=[temp[0],l]
            j=temp_macros.index(temp1)
            temp2=new_macro[j]
            si=temp2[2]
            ei=temp2[3]
            for i in range(si,ei+1):
                if("%macro" not in lines[i]):
                    if("%endmacro" not in lines[i]):
                        if("%" in lines[i]):
                            temp3=lines[i].split("%")
                            temp3[1]=temp3[1].replace("\n","")
                            lines[i]=lines[i].replace("%"+temp3[1],temp[1][int(temp3[1])-1])
                            print(lines[i])
                        else:
                            print(lines[i])

        else:
            print(lines[line])
        line+=1




if __name__ == '__main__':
    filename=argv[1]
    macros,line=macro_tabel(filename)
    macro_apply(filename,macros,line)
