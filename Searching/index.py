# Genetic Algorithm untuk mencari nilai minimum dari fungsi f(x1, x2)
# TIDAK menggunakan library eksternal kecuali 'random' bawaan Python
import random

# Konfigurasi awal
POP_SIZE = 6
CHROM_LENGTH = 20
GEN_MAX = 100
PC = 0.7
PM = 0,1  # Probabilitas mutasi
BITS_PER_VAR = 10
X_MIN = -10
X_MAX = 10

# (Optional) Untuk reproducibility hasil random:
random.seed(12345)

# Fungsi konversi dari biner ke bilangan riil
def bin_to_real(bits, min_val, max_val):
    decimal = 0
    for i, bit in enumerate(reversed(bits)):
        if bit == '1':
            decimal += 2**i
    return min_val + decimal * (max_val - min_val) / (2**len(bits) - 1)

# Decode kromosom menjadi nilai x1 dan x2
def decode(chrom):
    x1_bin = chrom[:BITS_PER_VAR]
    x2_bin = chrom[BITS_PER_VAR:]
    x1 = bin_to_real(x1_bin, X_MIN, X_MAX)
    x2 = bin_to_real(x2_bin, X_MIN, X_MAX)
    return x1, x2

# Fungsi matematika dasar
def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

def sin(x):
    pi = 3.141592653589793
    x = x % (2 * pi)
    res = 0
    for i in range(10):
        res += (-1)**i * x**(2*i+1) / factorial(2*i+1)
    return res

def cos(x):
    pi = 3.141592653589793
    x = x % (2 * pi)
    res = 0
    for i in range(10):
        res += (-1)**i * x**(2*i) / factorial(2*i)
    return res

def tan(x):
    c = cos(x)
    if abs(c) < 1e-6:
        return 1e6
    return sin(x) / c

def sqrt(x):
    if x < 0:
        return 0
    guess = x / 2
    for _ in range(10):
        guess = 0.5 * (guess + x / guess)
    return guess

def exp(x):
    res = 0
    for i in range(20):
        res += x**i / factorial(i)
    return res

# Fungsi objektif
def objective_function(x1, x2):
    try:
        return - (sin(x1) * cos(x2) * tan(x1 + x2) + 0.75 * exp(1 - sqrt(x1 * x1)))
    except:
        return 1e6

# Fungsi fitness
def fitness(x1, x2):
    f = objective_function(x1, x2)
    return 1 / (1 + abs(f))

# Inisialisasi populasi
def init_population():
    pop = []
    for _ in range(POP_SIZE):
        chrom = ''
        for _ in range(CHROM_LENGTH):
            chrom += '1' if get_rand() < 0.5 else '0'
        pop.append(chrom)
    return pop

# Fungsi random
def get_rand():
    return random.random()  # hasil float antara 0.0 - 1.0

# Seleksi orangtua dengan Roulette Wheel
def roulette_selection(pop, fits):
    total = sum(fits)
    r = get_rand() * total
    acc = 0
    for i in range(len(pop)):
        acc += fits[i]
        if acc >= r:
            return pop[i]
    return pop[-1]

# Crossover dua orangtua
def crossover(p1, p2):
    if get_rand() < PC:
        pt = int(get_rand() * (CHROM_LENGTH - 1)) + 1
        return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
    return p1, p2

# Mutasi satu bit
def mutate(chroms):
    total_bits = len(chroms) * CHROM_LENGTH
    idx = int(get_rand() * total_bits)
    child = idx // CHROM_LENGTH
    bit = idx % CHROM_LENGTH
    mutated = list(chroms[child])
    mutated[bit] = '1' if mutated[bit] == '0' else '0'
    chroms[child] = ''.join(mutated)
    return chroms

# ---------- Main Program ----------
population = init_population()
best_chrom = None
best_fit = -1

for g in range(GEN_MAX):
    decoded = [decode(c) for c in population]
    fits = [fitness(x1, x2) for x1, x2 in decoded]

    # Seleksi orangtua
    p1 = roulette_selection(population, fits)
    p2 = roulette_selection(population, fits)

    # Crossover dan Mutasi
    c1, c2 = crossover(p1, p2)
    c1, c2 = mutate([c1, c2])

    # Replacing individu terlemah
    weakest = sorted(range(len(fits)), key=lambda i: fits[i])[:2]
    population[weakest[0]] = c1
    population[weakest[1]] = c2

    # Update solusi terbaik
    for chrom in population:
        x1, x2 = decode(chrom)
        f = fitness(x1, x2)
        if f > best_fit:
            best_fit = f
            best_chrom = chrom

    # Tampilkan hasil generasi ini
    x1_best, x2_best = decode(best_chrom)
    f_best = objective_function(x1_best, x2_best)
    print(f"Generasi {g+1:03d}: x1 = {x1_best:.5f}, x2 = {x2_best:.5f}, f(x1,x2) = {f_best:.5f}")

# Setelah semua generasi selesai
print("\n=== HASIL AKHIR ===")
print(f"Kromosom terbaik: {best_chrom} ({f_best:.5f})")
print("x1 =", x1_best)
print("x2 =", x2_best)
print("f(x1,x2) =", f_best)