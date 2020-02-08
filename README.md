# Matrix Trace Processor

处理  [matrix-trace-canary](https://github.com/Tencent/matrix/tree/master/matrix/matrix-android/matrix-trace-canary) 中的堆栈信息。

## Demo

![demo](https://raw.githubusercontent.com/LinXiaoTao/matrix-trace-processor/master/demo/1581129760409.png)

## Usage

1. 保存堆栈信息到文件中

2. 将 matrix 生成的 methodMapping.txt 保存下来

3. 执行 python 脚本

   ``` shell
   python3 main.py workflow_traces demo/1581129760409.log > demo/1581129760409.txt demo/methodMapping.txt
   ```

4. 使用 [FlameGraph](https://github.com/brendangregg/FlameGraph) 将上面输出的 1581129760409.txt 转到 svg 文件

   ``` shell
    stackcollapse.pl demo/1581129760409.txt > demo/1581129760409.folded
    flamegraph.pl demo/1581129760409.folded > demo/1581129760409.svg
   ```

## Contributing

PRs accepted.

## License

MIT