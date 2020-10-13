# IPython：一种交互式计算和开发环境
## IPython基础
- 输入变量

  显示出该对象的一个字符串表示，会被格式化为可读性更好的形式
- Tab键自动完成

  自动完成与以输入的字符串相匹配的变量(对象、函数等)或者列出(当有多项时)


## 内省
在变量前或后加上?就可以显示该对象的一些通用信息；用??还将显示该函数的源代码
- `%run`命令

  可以把已经交互的语句当做python程序运行
- 中断正在执行的代码

  Ctrl+C可以在任何时候引发`KeyboardInterrupt`，除一些非常特殊的情况外会停止执行
- 执行剪切板中的代码

  使用`%paste`和`%cpaste`避免代码中空行引起的错误
- 键盘快捷键:

  | 命令 | 说明 |
  | ---- | ---- |
  | Ctrl-P或↑ | 后向搜索命令历史中以当前输入的文本开头的命令 |
  | Ctrl-N或↓ | 前向搜索命令历史中以当前输入的文本开头的命令 |
  | Ctrl-R | 按行读取的反向历史搜索(部分匹配) |
  | Ctrl-Shift-v | 从剪贴板粘贴文本 |
  | Ctrl-C | 中止当前正在执行的代码 |
  | Ctrl-A | 将光标移动到行首 |
  | Ctrl-E | 将光标移动到行尾 |
  | Ctrl-K | 删除从光标开始至行尾的文本 |
  | Ctrl-U | 清除当前行的所有文本 |
  | Ctrl-F | 将光标向前移动一个字符 |
  | Ctrl-B | 将光标向后移动一个字符 |
  | Ctrl-L | 清屏 |
  
- 异常和追踪

  某段异常会输出整个调用栈跟踪，还会附上调用栈附近的几段代码作为上下文参考
- 魔术命令(Magic Command)
IPython的一些特殊命令，通常为常见任务提供便利或轻松控制IPython系统的行为；魔术命令以%为前缀，可以看做命令行程序，大都有一些"命令行选项"

  | 命令 | 说明 |
  | --- | --- |
  | `%quickref` | 显示IPython的快速参考 |
  | `%magic` | 显示所有魔术命令的详细文档 |
  | `%debug` | 从最新的异常跟踪的底部进入交互式调试器 |
  | `%hist` | 打印命令的输入(可选输出)历史 |
  | `%pdb` | 在异常发生后自动进入调试器 |
  | `%paste` | 执行剪贴板中的Python代码 |
  | `%cpaste` | 打开一个特殊提示符以便手工粘贴待执行的Python代码 |
  | `%reset` | 删除interactive命名空间中的全部变量/名称 |
  | `%page *OBJECT*` | 通过分页器打印输出OBJECT |
  | `%run *script.py*` | 在IPython中执行一个Python脚本文件 |
  | `%prun *statement*` | 通过cProfile执行statement并打印分析器的输出结果 |
  | `%time *statement*` | 报告statement的执行时间 |
  | `%timeit *statement*` | 多次执行statement以计算系综平均执行时间 |
  | `%who`、`%who_ls`、`%whos` | 显示interactive命名空间中定义的变量，信息级别/冗余度可变 |
  | `%xdel *variable*` | 删除variable并尝试清除其在IPython中的对象上的一切引用 |

- matplotlib集成与pylab模式

  `IPython --pylab`


## 使用命令历史
IPython上维护着一个位于硬盘的小型数据库，保存执行过的每条命令文本，目的在于：

  1. 只需很少的按键次数即可搜索、自动完成并执行之前已经执行过的命令
  2. 在会话间持久化命令历史
  3. 将输入/输出历史记录到日志文件

- 搜索并重用命令历史

  键盘快捷键Ctrl-P或↑键在命令历史中向上搜索，Ctrl-N或↓键向下搜索，Ctrl-R实现部分增量搜索
- 输入和输出变量
  
  IPython会将输入和输出的引用保存在特殊变量中，最近的两个输出结果在_和__中；输入的文本在_ix变量中，_x为值，其中x为行号
- 记录输入和输出
  
  `%logstart`即可开始记录日志


## 与操作系统交互

| 命令 | 说明 |
| --- | --- |
| `!cmd` | 在系统shell中执行cmd |
| `output = !cmd args` | 执行cmd，并将stdout存放在output中 |
| `%alias *alias_name cmd*` | 为系统shell命令定义别名 |
| `%bookmark` | 使用IPython的目录书签系统 |
| `%cd *directory*` | 将系统工作目录更改为directory |
| `%pwd` | 返回系统的当前工作目录 |
| `%pushd *directory*` | 将当前目录入栈，并转向目标目录 |
| `%popd` | 弹出栈顶目录，并转向该目录 |
| `%dirs` | 返回一个含有当前目录栈的列表 |
| `%dhist` | 打印目录访问历史 |
| `%env` | 以dict形式返回系统环境变量 |

- shell命令和别名

  在IPython中以!开头的命令行表示气候的所有内容需要在系统shell中执行
  
  ```shell
  ip_info = !ifconfig eth0 | grep "inet" //可以获取系统的IP地址
  ```
- 目录书签系统

  保存常用目录的别名以实现快速跳转，`%bookmark [name] [path]`


## 软件开发工具
- 交互式调试器

  错误刚发生时输入%debug命令会跳转到引发异常的栈帧，输入u(up)或d(down)可以在栈跟踪的各级别间切换
  
  设置断点 `run -d filepath`
  
  | 命令 | 功能 |
  | --- | --- |
  | h(elp) | 显示命令列表 |
  | help *command* | 显示*command*的文档 |
  | c(ontinue) | 恢复程序的执行 |
  | q(uit) | 退出调试器，不再执行任何代码 |
  | b(reak) *number* | 在当前文件的第*number*行设置一个断点 |
  | b path/to/*file.py:number* | 在指定文件的第number行设置一个断点 |
  | s(tep) | 单步进入函数调用 |
  | n(ext) | 执行当前行，并前进到当前级别的下一行 |
  | u(p)/d(own) | 在函数调用栈中向上或向下移动 |
  | a(rgs) | 显示当前函数的参数 |
  | debug *statement* | 在新的(递归)调试器中调用语句*statement* |
  | l(ist) *statement* | 显示当前行，以及当前栈级别上的上下文参考代码 |
  | w(here) | 打印当前位置的完整栈跟踪(包括上下文参考代码) |
  
  其他使用场景
  
  ```python
  def set_trace():
      from IPython.core.debugger import Pdb
      Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)
  
  def debug(f, *args, **kwargs):
      from IPython.core.debugger import Pdb
      pdb = Pdb(color_scheme='Linux')
      return pdb.runcall(f, *args, **kwargs)
  ```
  重写这两个函数后，第一个函数在任何希望停下来查看的地方插入，第二个函数可以在任意函数上使用调试器，参数为函数名、输入、输出
  
- 测试代码的执行事件：`%time`和`%timeit`

  `%time`一次执行一条语句然后报告总体执行时间
  
  `%timeit`多次执行一条语句产生比较精确的平均执行时间
  
- 基本性能分析：`%prun`和`%run -p`
  
  `python -m cProfile cprof_example.py` 执行整个程序然后输出各函数的执行时间
  
  `python -m cProfile -s cumulative cprof_example.py` 与上句相比通过-s指定一个排序规则
  
  `%prun -l 7 -s cumulative run_experiment()` or `%run -p -s cumulative cprof_example.py` 上两条语句在IPython的版本
  
- 逐条分析函数性能

  line_profiler小型库中的`%lprun`可以对一个或多个函数进行逐行性能分析
  
  `%lprun -f func1 -f func2 staement_to_profile` 指定要分析的函数，适合"微观"分析
  
## IPython HTML Notebook
基于Web技术的交互式计算文档格式

## 利用IPython提高代码开发效率的几点提示
1. Python的一次加载模式：Python中import过一个模块的话，会新建命名空间保存变量、函数、引入项，下次再执行import会得到命名空间的一个引用，因此使用IPython时要注意reload import过但又修改的模块；还有IPython里的dreload
2. 代码设计提示
   1. 保留有意义的对象和数据
   2. 扁平结构要比嵌套结构好，尽量注意低耦合和模块化，这样易于测试、调试和交互式使用
   3. 无惧大文件

## 高级IPython功能
- 让你的类对IPython更加友好

  为自己编写的类添加__repr__(self)方法，IPython会获取该方法的字符串，控制台输出就更美观
  
- 个性化和配置

  配置文件:ipython_config.py 目录：~/.config/ipython(unix)和%HOME%/.ipython/(Windows)