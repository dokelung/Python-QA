# python 如何生成特定列表格式

## 問題

```python
aa = [
    {'ip': '192.168.1.1', 'projectname__pname': 'hh', 'id': 1, 'projectname_id': 1}, 
    {'ip': '192.168.3.2', 'projectname__pname': 'hh', 'id': 2, 'projectname_id': 1}, 
    {'ip': '192.168.22.3', 'projectname__pname': 'qm', 'id': 3, 'projectname_id': 2}, 
    {'ip': '192.168.5.3', 'projectname__pname': 'ssh', 'id':4, 'projectname_id': 3}
]
```

大家好，我想把 `aa` 中的列表生成以下 `bb` 的格式:

```python
bb = [
    {
        'projectname_id': 1,
        'projectname__pname': 'hh',
        'children': [{'id': 1, 'text': '192.168.1.1'},{'id': 2, 'text': '192.168.1.2'}]
    },
    {
        'projectname_id': 2,
        'projectname__pname': 'qm',
        'children': [{'id': 3, 'text':'192.168.22.3'}]
    },
    {
        'projectname_id': 3,
        'projectname__pname': 'ssh',
        'children': [{'id': 4, 'text': '192.168.5.3'}]
    }
]
```

請問代碼怎麽實現?

問題出自 [segmentfault](), by [tempreg](https://segmentfault.com/u/tempreg)

## 回答

代碼:

```python
def aa2bb(aa):
    bb = []
    proj_id_map = {}
    for ad in aa:
        proj_id = ad['projectname_id']
        child = {'id': ad['id'], 'text': ad['ip']}
        if proj_id not in proj_id_map:
            bd = {
                'projectname__pname': ad['projectname__pname'],
                'projectname_id': ad['projectname_id'],
                'children': [child]
            }
            bb.append(bd)
            proj_id_map[proj_id] = bd
        else:
            bd = proj_id_map[proj_id]
            bd['children'].append(child) 
    return bb
```

測試:

```python
from pprint import pprint

aa = [
    {'ip': '192.168.1.1', 'projectname__pname': 'hh', 'id': 1, 'projectname_id': 1}, 
    {'ip': '192.168.3.2', 'projectname__pname': 'hh', 'id': 2, 'projectname_id': 1}, 
    {'ip': '192.168.22.3', 'projectname__pname': 'qm', 'id': 3, 'projectname_id': 2}, 
    {'ip': '192.168.5.3', 'projectname__pname': 'ssh', 'id':4, 'projectname_id': 3}
]

pprint(aa2bb(aa))
```

結果:

```python
[{'children': [{'id': 1, 'text': '192.168.1.1'},
               {'id': 2, 'text': '192.168.3.2'}],
  'projectname__pname': 'hh',
  'projectname_id': 1},
 {'children': [{'id': 3, 'text': '192.168.22.3'}],
  'projectname__pname': 'qm',
  'projectname_id': 2},
 {'children': [{'id': 4, 'text': '192.168.5.3'}],
  'projectname__pname': 'ssh',
  'projectname_id': 3}]
```
