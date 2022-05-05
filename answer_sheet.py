# encoding: utf-8
# @author: 于东和
# @file: ff.py
# @time: 2022/5/5 17:32
# @desc:


import itertools
import sys

"""----------------------------------第一题-------------------------------------------"""


def merge_dict(source_dict, update_dict) -> dict:
    """
    字典合并
    :param source_dict: 第一个字典
    :param update_dict: 第二个字典
    :return: 合并后的字典
    """
    for k, v in source_dict.items():
        if k in update_dict and isinstance(v, dict) and isinstance(update_dict[k], dict):
            update_dict[k] = merge_dict(v, update_dict[k])
        if k not in update_dict:
            update_dict[k] = v

    return update_dict


source_dict = {'key0': 'a', 'key1': 'b', 'key2': {'inner_key0': 'c', 'inner_key1': 'd'}}
update_dict = {'key1': 'x', 'key2': {'inner_key0': 'y'}}
result = merge_dict(source_dict, update_dict)
print(result)
"""----------------------------------第二题-------------------------------------------"""


def telephone_combination(telephone_nums):
    """

    :param telephone_nums: 电话号码，传入的数字为字符串
    :return:
    """
    # todo 由于给的例子中传入的是字符串，就没有做额外的处理
    dct = {
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"],
    }
    telephone_str_list = []
    for s in telephone_nums:
        telephone_str_list.append(dct[s])
    result = ["".join(i) for i in itertools.product(*telephone_str_list)]
    return result


print(telephone_combination("23"))

"""----------------------------------第三题-------------------------------------------"""
"内存泄漏:程序中已经分配出去的内存无法释放，而导致的内存浪费"

import sys
import time
import threading
import weakref

import gc
import objgraph


class Person(object):
    free_lock = threading.Condition()

    def __init__(self, name: str = ""):
        """
        Parameters
        ----------
        name: str
          姓名

        best_friend: str
          最要好的朋友名
        """
        self._name = name
        self.best_friend = None


def mem_leak():
    """
    循环引用导致内存泄漏
    """
    zhang_san = Person(name='张三')
    li_si = Person("李四")
    print("初次打印引用次数：", sys.getrefcount(zhang_san))

    # 构造出循环引用
    # 李四的好友是张三
    li_si.best_friend = zhang_san
    print("第二次打印引用次数：", sys.getrefcount(zhang_san))

    # 张三的好友是李四
    zhang_san.best_friend = li_si
    print("第三次打印引用次数：", sys.getrefcount(zhang_san))
    # zhang_san.best_friend = "lisi"
    # li_si.best_friend = "zhangsan"
    print("第四次打印引用次数：", sys.getrefcount(zhang_san))  # 引用计数为3,且为循环引用
    print("gc.count1", gc.get_count())


for i in range(50):
    time.sleep(0.01)
    print(i)
    mem_leak()

print("mem_leak 执行完成了.")
# gc.collect()
print("gc.count", gc.get_count())
objgraph.show_most_common_types(limit=50)

# todo 因为循环引用的关系，引用计数不为0，导致内存释放不了
