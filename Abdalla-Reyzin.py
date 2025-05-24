import random
import hashlib 
import time

#ビット数指定
l = 256

#素数生成
def gen_number(p):
    for x in range(40):
        a = random.randrange(2,p-1)
        if pow(a, p-1, mod = p) == 1:
            pass
        else:
            return False

#素数確定
def get_prime():
    while True:
        p = random.randint(10**308,10**309)
        if gen_number(p) != False and p % 4 == 3:
            return p
        
#鍵生成
def key_gen(p,q):
    t1 = time.perf_counter()
    N = p * q
    s = random.randint(1,N)
    S = pow(s, 2, mod=N)
    U = pow(pow(S, pow(2,l), N) ,-1 ,N)
    pk = N, U
    sk = S
    t2 = time.perf_counter()
    print(f"鍵生成: {t2-t1}s")
    return pk, sk # 公開鍵, 秘密鍵

#ハッシュ関数
def hash(Y):
    M = "input.txt" #テキストファイル名
    h = hashlib.sha256()
    with open('./' + M) as f:
        for line in f: 
            h.update(line.encode())
    h.update(str(Y).encode()) 
    h_byte = h.digest()
    h_int = int.from_bytes(h_byte, byteorder = 'big')
    sigma = h_int
    return sigma

#署名生成
def graph_gen(pk,sk):
    t1 = time.perf_counter()
    N = pk[0]
    r = random.randint(1,N)
    R = pow(r,2,N)
    Y = pow(R, pow(2,l), N)
    sigma = hash(Y)
    Z = pow(R * pow(sk, sigma, N), 1, N)
    t2 = time.perf_counter()
    print(f"署名生成: {t2-t1}s")
    return Z, Y ,sigma

#署名検証
def graph_test(pk, Z, sigma):
    t1 = time.perf_counter()
    N = pk[0]
    U = pk[1]
    a = pow(Z, pow(2,l), N)
    b = pow(U, sigma, N)
    Y1 = pow(a * b, 1, N)
    sigma2 = hash(Y1)
    t2 = time.perf_counter()
    if sigma2 == sigma:
        print(1)
    else:
        print(0)
    print(f"署名検証: {t2-t1}s")

#実行する関数
def execute():
    p = get_prime()
    q = get_prime()
    pk, sk = key_gen(p,q)
    Z, Y, sigma = graph_gen(pk,sk)
    graph_test(pk, Z, sigma)

#実行時間計算
t1 = time.perf_counter()
execute()
t2 = time.perf_counter()
diff_time = t2 - t1
print(f"実行時間: {diff_time}")