import random
import hashlib 
import time

#ビット数指定
l = 256
#鍵更新回数
T = 5

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
    S0 = random.randint(1,N)
    U = pow(pow(S0, pow(2,l*(T+1)), N) ,-1 ,N)
    pk = N, U, T
    sk = N, T, 0, S0 # j=0 における鍵生成
    t2 = time.perf_counter()
    print(f"鍵生成: {t2-t1}s")
    return pk, sk # 公開鍵, 秘密鍵

#ハッシュ関数
def hash(j, Y):
    M = "input.txt" #テキストファイル名
    h = hashlib.sha256()
    with open('./' + M) as f:
        for line in f: 
            h.update(line.encode())
    h.update(str(j).encode())
    h.update(str(Y).encode()) 
    h_byte = h.digest()
    h_int = int.from_bytes(h_byte, byteorder = 'big')
    sigma = h_int
    return sigma

#署名生成
def graph_gen(sk):
    t1 = time.perf_counter()
    N=sk[0]
    j = sk[2] 
    Sj = sk[3]
    R = random.randint(1,N)
    Y = pow(R, pow(2,l*(T+1-j)), N)
    sigma = hash(j, Y)
    Z = pow(R * pow(Sj, sigma, N), 1, N)
    graph = j, Z, sigma
    t2 = time.perf_counter()
    print(f"署名生成: {t2-t1}s")
    return graph

#署名検証
def graph_test(pk, graph):
    t1 = time.perf_counter()
    N = pk[0]
    U = pk[1]
    j = graph[0]
    Z = graph[1]
    sigma = graph[2]
    a = pow(Z, pow(2,l * (T+1-j)), N)
    b = pow(U, sigma, N)

    Y1 = pow(a * b, 1, N)
    sigma2 = hash(j,Y1)
    if sigma2 == sigma:
        print("結果: 1")
    else:
        print("結果: 0")
    t2 = time.perf_counter()
    print(f"署名検証: {t2-t1}s")

#鍵更新
def update_key(sk):
    t1 = time.perf_counter()
    N=sk[0]
    S=sk[3]
    j = sk[2] + 1
    S_new = pow(S, pow(2, l), N)
    sk_new = N, T, j, S_new 
    t2 = time.perf_counter()
    print(f"{j}回目 鍵更新: {t2-t1}s")
    return sk_new

#実行関数
def execute():
    p = get_prime()
    q = get_prime()
    pk, sk = key_gen(p,q)
    graph = graph_gen(sk)
    graph_test(pk, graph)

    for a in range(T):
        sk = update_key(sk)
        new_graph = graph_gen(sk)
        graph_test(pk, new_graph)

execute()