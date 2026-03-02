# BlueArchive-decrypt-demo

## 总览

碧蓝档案(国际服)数据解密,反序列化工具demo,最后结果会存放在dist文件夹中

> [!WARNING]
>
> 不想写很多flatbuffer结构文件,只有部分作为例子,可自行编写插件来.

## 环境安装

推荐使用虚拟环境

```shell
pip install -r requirements.txt
```

## 项目结构

- converters:转换器,用于反序列化,项目会动态加载该目录下的所有解释器
- example:用作demo的文件
- FlatData:由flatc生成
- modules:存放各种工具类
- config.yaml:项目配置
- demo_decrypt.py:数据解密的例子
- demo_zip_password:获取压缩包密码的例子

> [!WARNING]
>
> 使用flatc生成之后的FlatData中的enum,最好改成继承IntEnum,方便解析

## Converter转换器文件结构

- 文件中必须包含 `__converter__meta__`属性
- 类名必须为 `Converter`且需要继承 `DBConverter`或 `TableConverter`并且需要实现 `parse_data`方法，具体传入值见下方

### DBConverter

该转换器主要用于转换在 `ExcelDB.db`sqlite数据库中表格里面的blob类型数据,其中在实现 `parse_data(self, data:Any)`中的data数据为sqlite的表查询结果

### TableConverter

该转换器主要用于从 `Excel.zip`解压之后的bytes类型文件,其中在实现 `parse_data(self, data:Any)`中的data数据为解密之后的bytes数据,可以直接传入flatbuffer对应的getRootAs方法
