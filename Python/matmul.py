# A = n * m
# B = m * p
# C = n * p

A = [[1, 2],
     [3, 4]]

B = [[5, 6, 7, 8],
     [9, 0, 1, 2]]

C = [[1*5 + 2*9, 1*6 + 2*0, 1*7 + 2*1, 1*8 + 2*2],
     [3* 5 + 4*9, 3*6 + 4*0, 3*7 + 4*1, 3*8 + 4*2]]

def display_matrix(A):
    for row in A:
        print(row)

def matmul(A, B):
    if len(A[0]) != len(B):
        print("Cannot multiply A with B.")
        return None
    
    C = []
    for _ in range(len(A)):
        row = []
        for _ in range(len(B[0])):
            row.append(0)
        C.append(row)
    
    rows = len(C)
    columns = len(C[0])
    
    for i in range(rows):
        for j in range(columns):
            for k in range(rows):
                C[i][j] += A[i][k]*B[k][j]
    
    return C
            
D = matmul(A, B)
display_matrix(C)
display_matrix(D)
            
    
    