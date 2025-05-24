import os
import sys
import random
import hashlib 
import time


# KI署名における公開鍵
PK = None

#鍵更新における懸念点
SKstar = None

#暗号化する文章
M = "input.txt"

#ビット数指定
l = 256

#実行回数指定
J = 0

#公開鍵指定
N = None

#ミラーラビン素数判定方式
def is_prime(n, k = 40):
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

#素数確定
def get_prime():
    while True:
        p = random.getrandbits(1024)
        if is_prime(p) and p % 4 == 3:
            return p
        
#鍵生成
def key_gen_KI(p,q):
    
    global N
    N = p * q
    s = random.randint(1,N)
    S = pow(s, 2, mod=N)
    U = pow(S, pow(2, l), N)
    U_inv = pow(U, -1, N)
    sk = S
    pk = N, U_inv

    return sk, pk 


#ハッシュ関数 (Pki で署名)
def hash_KI(Y,M):
    try:
        h = hashlib.sha256()
        #テキストファイル名
        M = "input.txt" 
        if os.path.exists(M):
            with open('./' + M) as f:
                h.update((f.read()).encode())
        h.update(str(Y).encode())
        h_byte = h.digest()
        h_int = int.from_bytes(h_byte, byteorder = 'big')
        sigma = h_int
        return sigma
    except OSError as e :
        print(e)

#署名生成
def graph_gen(M,sk):
    try:
        global N 
        r = random.randint(1,N)
        R = pow(r,2,N)
        Y = pow(R, pow(2,l), N)
        sigma = hash_KI(Y,M)
        Z = (R * pow(sk, sigma, N)) % N
        return sigma, Z
    except OSError as e :
        print(e)

#署名検証
def graph_test(M,sin,PK):
    try:
        N, U = PK
        sigma, Z = sin
        a = pow(Z, pow(2,l), N)
        b = pow(U, sigma, N)
        Y1 = (a * b) % N
        sigma2 = hash_KI(Y1, M)
        return sigma2 == sigma
    except OSError as e :
        print(e)

#-------------AbdallaReyzinを用いたKI署名-------------
#安全な環境とする
def secure_gen_ki():
    try:
        t1 = time.perf_counter()
        p = get_prime()
        q = get_prime()
        SKst, Pk = key_gen_KI(p,q)
        SKi, PKi = key_gen_KI(p,q)
        sigma_j_st = graph_gen(str(PKi),SKst) 
        #安全な環境の秘密鍵
        global SKstar
        SKstar = SKst
        #署名者の公開鍵
        PK = Pk #(N,U)
        #署名者の秘密鍵
        sig_sk = SKi, PKi, sigma_j_st 
        t2 = time.perf_counter()
        print(f"鍵生成: {t2-t1}s")
        return PK, sig_sk
    except OSError as e :
        print(e)

#署名生成
def sig_gen_ki(M,sk):
    try:
        t1 = time.perf_counter()
        SKi, PKi, SIGMA_j_st = sk
        SIGMA_jm = graph_gen(M, SKi) 
        SIGMA = PKi, SIGMA_j_st, SIGMA_jm 
        t2 = time.perf_counter()
        print(f"署名生成: {t2-t1}s")
        return SIGMA
    except OSError as e :
        print(e)

#署名検証
def sig_test_ki(PK, SIGMA, M):
    try:
        t1 = time.perf_counter()
        PKj, SIGMA_j_st, SIGMA_jm = SIGMA
        b_star = graph_test_1(PK, SIGMA_j_st, PKj)
        b_j = graph_test_2(PKj, SIGMA_jm, M) 
        t2 = time.perf_counter()
        print(f"署名検証: {t2-t1}s")
        if b_star and b_j:
            return True
        return False
    except OSError as e :
        print(e)

def graph_test_1(PK, SIGMA_j_st, PKj):
    try:
        N, U = PK
        sigma, Z = SIGMA_j_st
        a = pow(Z, pow(2,l), N)
        b = pow(U, sigma, N)
        Y1 = (a * b) % N
        sigma2 = hash_KI(Y1, M)
        return sigma2 == sigma
    except OSError as e :
        print(e)

def graph_test_2(PKj, SIGMA_jm, M):
    try:
        N, U = PKj
        sigma, Z = SIGMA_jm
        a = pow(Z, pow(2,l), N)
        b = pow(U, sigma, N)
        Y1 = (a * b) % N
        sigma2 = hash_KI(Y1, M)
        return sigma2 == sigma
    except OSError as e :
        print(e)

#鍵更新
# def update_key_ki(SKst):
#     #時刻Jの更新
#     global J
#     J = J + 1
#     p = get_prime() #新たな
#     q = get_prime()
#     SKj_new, PKj_new = key_gen_KI(p,q)
#     SIGMA_new = graph_gen(SKst,PKj_new )
#     sk = SKj_new, PKj_new, SIGMA_new
#   return sk 

#実行関数
def KI_exe():
    sig_pk, sig_sk = secure_gen_ki() 
    SIGMA = sig_gen_ki(M,sig_sk)
    res = sig_test_ki(sig_pk,SIGMA,M)
    print("署名検証結果:", res)
    #鍵更新
    # for i in range(5):
    #     global SKstar
    #     SKst = SKstar
    #     sk = update_key_ki(SKst)
    #     new_graph = graph_gen(sk,M)
    #     res = sig_test_ki(sig_pk,new_graph,M)
    #     print("署名検証結果:", res)

if __name__ == '__main__':
    try:
        KI_exe()
    except OSError as e:
        print(e)
    