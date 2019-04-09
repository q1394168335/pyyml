# pyyml
Use python in yaml
## 基本使用
在python中使用：
```python
from pyyml import load

with open('conf.yml') as f:
    raw_conf = f.read()
config = load(raw_conf)
print(config)
```
在yaml中 `${...}` 中的内容将会被python执行：

yaml内容
```yaml
sum: ${1 + 1}
```
实际解析内容
```python
{'sum': 2}
```
通过在文件开头第一行注释来导入所需的包：

```yaml
# libs:['os', 'os.path:path', 'this']
```
通过 [包名]:[别名] 取别名导入包

`'os.path:path' 等同于 python 中的 from os import path`

例如yaml文件内容
```yaml
# libs:['os', 'os.path:path', 'this']
os_name: ${os.name}
base_dir: ${path.abspath(path.dirname(__file__))}
```