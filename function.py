import copy



def write_file():


##########################################################################################

# read file and store clauses to an 2d array
def readFile(fileName):
    fopen = open(fileName, 'r')
    alpha = fopen.readline().replace('\n', '')               # câu alpha
    clauses_quantity = int(fopen.readline()) # số lượng mệnh đề trong KB
    # KB là mảng chứa cơ sở tri thức
    KB = []
    for i in range(clauses_quantity):
        clause = fopen.readline().replace('\n', '').split()
        # remove OR
        for element in clause:
            if element == 'OR':
                clause.remove(element)
        KB.append(clause)
    fopen.close()
    print(KB)
    return alpha, KB

# phủ định mệnh đề
def negative(variable):
    if len(variable) == 2:
        variable = variable[1:]
    else:
        variable = '-' + variable
    return variable


def PL_RESOLVE(clause1, clause2):
    result = []
    newclause1 = copy.deepcopy(clause1)
    newclause2 = copy.deepcopy(clause2)
    for variable in newclause1:
        negative_clause = negative(variable)
        # clause1 và clause2 chứa cặp đối ngẫu thì loại bỏ
        if negative_clause in newclause2:
            newclause2.remove(negative_clause)    
            newclause1.remove(variable)
            # thêm các mệnh đề còn lại vào kết quả hợp giải
            result.append(list(newclause1 + newclause2))
            return result 
    # return về rỗng nếu không có mệnh đề đối ngẫu
    return result

# kiểm tra mệnh đề vô ích
def checkTrue(clause):
    for i in clause:
        if negative(i) in clause:
            return True
    return False

def short(clause):
    for i in range(len(clause) - 1):
        for j in range(i + 1, len(clause)):
            if(clause[i] == clause[j]):
                clause.remove(clause[i])
                break;

    return clause

def transform(clause):  # hàm chuyển về lại mệnh đề để ghi 
    result = ''
    for i in range(len(clause)):
        if i == len(clause) - 1:
            result += clause[i]
            result += '\n'
        else:
            result += clause[i]
            result += ' OR '
    return result

def sort(clause):
    if(len(clause) != 0):
        for i in range(len(clause) - 1):
            for j in range(i + 1, len(clause)):
                if(clause[i][len(clause[i]) - 1] > clause[j][len(clause[j]) - 1]):
                    temp = clause[i]
                    clause[i] = clause[j]
                    clause[j] = temp
        return clause
    return []

        


def isInside(small, big):
    for i in small:
        if not i in big:
            return False
    return True


def PL_RESOLUTION(KB, alpha, fileName):

    f = open(fileName, 'w')

    # đưa phủ định alpha qua KB
    allClauses = KB
    allClauses.append([negative(alpha)])

    # sort 
    for i in allClauses:
        i = sort(i)


    for k in range(4):
        newClause = []
        count = 0
        string = ''
        for i in range(len(allClauses)):
            for j in range(len(allClauses)):
                if j <= i:
                    continue
                else:
                    resolvent = PL_RESOLVE(allClauses[i], allClauses[j])
                    
                    # hợp giải không ra kq
                    if(resolvent == []):
                        continue

                    if(len(resolvent) > 0):
                        resolvent[0] = sort(resolvent[0])
                        resolvent[0] = short(resolvent[0])
                        # nếu hợp giải ra mệnh đề rông
                        if(resolvent[0] == []):
                            count += 1
                            string = str(count) + '\n' + string + '{}\nYES'
                            f.write(string)
                            return True

                        elif checkTrue(resolvent[0]):
                            continue

                        # hợp giải ra mệnh đề mới
                        elif(not resolvent[0] in allClauses):
                            count += 1
                            string += transform(resolvent[0])
                            newClause.append(resolvent[0])
        f.write(str(count))
        f.write('\n')
        f.write(string)
        if(newClause == []):
            f.write('NO')
            return False

        allClauses.extend(newClause)
    

    f.close()



