from Functions import f

def find_best():
    best = [0, 0, 0, 0]
    best_fitness = f(best)
    for x1 in range(-16, 16):
        for x2 in range(-16, 16):
            for x3 in range(-16, 16):
                for x4 in range(-16, 16):
                    if f([x1, x2, x3, x4]) < best_fitness:
                        best = [x1, x2, x3, x4]
                        best_fitness = f([x1, x2, x3, x4])
    return best, best_fitness

print(find_best())