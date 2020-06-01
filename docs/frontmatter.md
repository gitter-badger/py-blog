```markdown
---
title: 标题
date: 2020-06-01
tags:
  - 标签1
  - 标签2
  
categories:
  - [分类1]
  - [分类2,子分类]
  - [分类3,子分类,子分类的子分类]
author: zcmimi
---

write something

```

```
---
...
---
```
像这样,在文章开头两个`---`隔开的区域就是`frontmatter`

`frontmatter`使用`yaml`语法

下面是变量含义:

|变量名|含义|默认值|
|-|-|-|
|`title`|标题|文章的文件名|
|`date`|编辑时间|文件修改时间|
|`author`|作者|默认为博客作者|
|`tags`|标签||
|`categories`|分类||
|`top`|置顶优先级(越大越高)|0|
|`layout`|布局|文章为post,分页为page,修改该项请参照所使用主题的说明|
|自定义变量名|自定义文章的其他信息|请参照所使用主题的说明|

**tips:**

由于`yaml`语法,**`frontmatter`中不能出现`tab`**,请用空格代替

分类方法:

> 假设要添加`Diary`和`Lify`两个并列分类
> 
> ```yaml
> categories:
>   - Diary
>   - Life
> ```
> 
> 上面的写法是错误的,正确写法:
> 
> ```yaml
> categories:
>   - [Diary]
>   - [Life]
> ```
> 
> 再举个例子:
> 
> ```yaml
> categories:
> - [Diary, PlayStation]
> - [Diary, Games]
> - [Life]
> ```
> 
> 此时这篇文章同时包括三个分类：`PlayStation`和`Games`分别都是父分类`Diary`的子分类,同时`Life`是一个没有子分类的分类。

自定义变量:

> 请配合主题使用,如大部分主题`comment`表示是否开启评论,少数主题可能没有评论功能
> 
> 更多其他变量名请参照使用主题的说明
