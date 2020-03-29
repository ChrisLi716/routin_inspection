import sys


class Const:
    class ConstError(PermissionError):
        pass

    class ConstCaseError(ConstError):
        pass

    # 重写 __setattr__() 方法
    def __setattr__(self, name, value):
        # 已包含该常量，不能二次赋值
        if name in self.__dict__:
            raise self.ConstError("Can't change const {0}".format(name))
        # 所有的字母需要大写
        if not name.isupper():
            raise self.ConstCaseError("const name {0} is not all uppercase".format(name))
        self.__dict__[name] = value

# # 将系统加载的模块列表中的 constant 替换为 Const() 实例
# sys.modules[__name__] = Const()
