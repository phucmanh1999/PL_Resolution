from sys import argv

#command line read file input and output name
fileInput = argv[1]
fileOutput= argv[2]

"""c1 = "-A B".split(" ")
c2 = "B -C".split(" ")
c3 = "A -B C".split(" ")
c4 = ["-B"]

alpha = "-A"
clauses = [c1,c2,c3,c4]"""

def read_file(fileName):
    """
    :param fileName: string name of file
    :return: alpha: string, KB: list
    """
    fopen = open(fileName, "r")
    alpha = fopen.readline().replace("\n","") #remove "\n" (enter)
    KB = []
    num_clause = int(fopen.readline())
    #"A OR B OR C" -> ["A","B","C"]
    for i in range(num_clause):
        clause = fopen.readline().replace("\n","").split(" ")  #remove \n in last, and split string to 3 literal
        while("OR" in clause):
            clause.remove("OR") #remove "OR"
        while ("" in clause): #if there are more than 1 space between literals #e.g. A   OR B OR C
            clause.remove("")  # remove ""
        KB.append(clause)
    return alpha,KB

def negative(literal):
    """
    :param literal:  "A"
    :return: negative clause: "-A"
    """
    if literal[0] == '-':
        return literal[1:]
    else:
        return '-' + literal
def resolve(c11, c22):
    """
    :param c1: clause: ["A","B","C"] (A v B v C)
    :param c2: like c1
    :return: a resolution of (c1,c2)
    """
    c1 = list(c11)
    c2 = list(c22)
    if (len(c1)== 1 and len(c1) == len(c2)): #len c1 = len c2 = 1
        if c1[0] == negative(c2[0]):
            return "{}"

    for literal in c1:
        if negative(literal) in c2:
            c2.remove(negative(literal))
            c1.remove(literal)
            result = c1+c2
            return result
    return []

def checkRemoveIfTrue(clause):
    """
    check to possible to remove clause
    :param clause: ["-B","B","C"] (-B v B v C) -> true v C
    :return: remove <=> True
    """
    for literal in clause:
        if negative(literal) in clause:
            return True
    return False
def toPositive(literal):
    """
    transform literal to positive
    :param literal: A or -A
    :return: A
    """
    if literal[0]=="-":
        return literal[1:];
    else:
        return literal

def sortAlpha(clause):
    """
    sort and remove same literal
    :param clause:
    :return:
    """
    i=0
    while(i<len(clause)-1):
        j=i+1
        while(j<len(clause)):
            if clause[i] == clause[j]:
                del clause[j]
                j -= 1
                i -= 1
            j+=1
        i+=1

    for i in range(len(clause)-1):
        for j in range(i+1,len(clause)):
            if (toPositive(clause[i])> toPositive(clause[j])):
                #swap
                temp = clause[i]
                clause[i]= clause[j]
                clause[j] = temp

def transToString(clause):
    """
    trans to string to write file output
    :param clause:
    :return: string
    """
    string =""
    for i in range(len(clause)-1):
        string += clause[i]
        string += " OR "
    string += clause[-1]
    string += "\n"


    return  string
def resolution(alpha, KB):
    """
    Check KB entails allpha?
    open and write result in file Output.txt
    :param alpha: string
    :param KB: list knowledge base
    :return: nothing
    """
    fwrite = open(fileOutput, "w") #open file to write
    clauses = KB + [[negative(alpha)]] # add negative alpha into KB
    while (True):
        new_clauses = []
        num_of_res = 0
        string_write = ""
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                result_res = resolve(clauses[i], clauses[j])
                sortAlpha(result_res)
                if result_res == []: #cant resolve
                    continue
                if result_res in clauses: # exist
                    continue
                if checkRemoveIfTrue(result_res): # e.g B v-B - C -> remove
                    continue
                if result_res == "{}":
                    string_write +="{}\nYES"
                    num_of_res += 1
                    string_write = str(num_of_res)+"\n"+ string_write
                    fwrite.write(string_write)
                    return True #stop
                else:
                    string_write += transToString(result_res)
                    num_of_res +=1
                    new_clauses.append(result_res)
        string_write = str(num_of_res) + "\n" + string_write
        fwrite.write(string_write)
        if new_clauses ==[]:
            string_write +="0\nNo"
            fwrite.write("No")
            return False #stop
        clauses += new_clauses
	


def main():
    """
    open and read file Input.txt
    Resolution
    :return:
    """
    alpha, KB = read_file(fileInput)
    resolution(alpha,KB)
    print("Done!")
main()