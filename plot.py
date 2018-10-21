import matplotlib.pyplot as plt

filename = 'logN1kT5kR1k.txt'

logs = open(filename).readlines()
logs = logs[1:]

L_list = [int(log.split('\t')[0]) for log in logs]
acc_list = [float(log.split('\t')[1].replace('\n', '')) for log in logs]

plt.plot(L_list, acc_list)
plt.xlabel('L')
plt.ylabel('平均成功率[%]')
plt.ylim(0.0, 110.0)
plt.show()
