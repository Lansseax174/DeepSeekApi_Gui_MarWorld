# import multiprocessing
# import os
# from time import sleep
#
#
# def compute(a=0):
#     while True:
#         a += 1
#         print(str(a) + 'a' + '\n')
#
#
# if __name__ == '__main__':
#     number_workers = os.cpu_count()
#     process = []
#
#     for _ in range(number_workers):
#         p = multiprocessing.Process(target=compute)
#         p.start()
#         process.append(p)
#
#     for p in process:
#         p.join()