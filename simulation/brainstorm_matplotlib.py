import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

population_size = 1000
initial_infected = 1
infection_rate = 0.3
recovery_rate = 0.1
days = 100

# 未感染+未感染过的
susceptible = population_size - initial_infected
# 感染的
infected = initial_infected
# 恢复好的
recovered = 0

S, I, R = [susceptible], [infected], [recovered]


def update(num, S, I, R, bars):
    global susceptible, infected, recovered
    # 新感染的 = 易感染者 * 感染者 * 感染率
    new_infected = infection_rate * infected * susceptible / population_size
    new_recovered = recovery_rate * infected

    susceptible -= new_infected
    infected += new_infected - new_recovered
    recovered += new_recovered

    S.append(susceptible)
    I.append(infected)
    R.append(recovered)

    bars[0].set_height(susceptible)
    bars[1].set_height(infected)
    bars[2].set_height(recovered)

    return bars


fig, ax = plt.subplots()
bars = plt.bar(['Susceptible', 'Infected', 'Recovered'], [S[-1], I[-1], R[-1]], color=['blue', 'red', 'green'])

anim = FuncAnimation(fig, update, fargs=(S, I, R, bars), frames=days, repeat=False)
plt.ylim(0, population_size)
plt.title('Disease Spread Simulation')
plt.show()
