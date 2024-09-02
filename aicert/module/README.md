# 上传自己的代码包，规范如下：

## 1.对抗样本攻击接口
```txt
class aicert.module.evasion.attack.PGD(model, conf, eps=0.03137254901960784, alpha=0.00784313725490196, steps=10, random_start=True, **kwgs)
描述：给定自然样本生成对抗样本的类，实现attack函数

输入:
model (nn.Module) – 模型对象.
conf (dict) - {"model": 模型名称, "dataset": 数据集名称, "mean": 数据mean List[float], "std": 数据std List[float]}
eps (float) – maximum perturbation. (Default: 8/255)
alpha (float) – step size. (Default: 2/255)
steps (int) – number of steps. (Default: 10)
random_start (bool) – using random initialization of delta. (Default: True)
**kwgs (dict) - 其它参数

def aicert.module.evasion.attack.PGD.attack(images, labels)
描述：给定自然样本生成对抗样本的函数
输入：
images (torch.array) - 自然样本, e.g., torch.float([x1, x2, x3,...,])
labels (torch.array) - 样本标签, e.g., torch.long([y1, y2, y3,...,])

输出：
adv_images (torch.array) - 对抗样本, e.g., torch.float([x1, x2, x3,...,])

Examples：
evasion = aicert.module.evasion.attack.PGD(model, conf={"model":"yolov5", "dataset":"coco2017", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}, eps=8/255, alpha=1/255, steps=10, random_start=True)
adv_images = evasion.attack(images, labels)
```

## 2.对抗样本检测接口
```text
> class aicert.module.evasion.defense.Twis(model, conf, **kwgs)
描述：检测对抗样本的类，实现detect、eval两个函数

Twis类输入:
model (nn.Module) – 模型对象.
conf (dict) - {"model": 模型名称, "dataset": 数据集名称, "mean": 数据mean List[float], "std": 数据std List[float], "num_classes": 标签数量}
**kwgs (dict) - Twis算法需要的其它参数

> def Twis.detect(images)
描述：检测给定的多个样本是否为对抗样本

输入：
images (torch.array) - 嫌疑对抗样本，e.g., torch.float([x1, x2, x3,...,])

输出：
pred (torch.array) - 预测Logits, e.g., e.g., torch.float([[p0, p1], [p0, p1], [p0, p1],...])

> def Twis.eval(images, labels)
输入：
images (torch.array) - 嫌疑对抗样本，e.g., torch.float([x1, x2, x3,...,])
labels (torch.array) - 样本真实类别，e.g., torch.long([y1, y2, y3,...,])

输出：
acc (torch.array) - 验证准确率
tpr (torch.array) - 验证tpr
fpr (torch.array) - 验证fpr

Examples：
twis = aicert.module.evasion.defense.Twis(model, conf={"model":"yolov5", "dataset":"coco2017", "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]})
pred = twis.detect(adv_images)
acc, tpr, fpr = twis.eval(images, labels)
```


## 3.对抗样本去除接口
```text
> class aicert.module.evasion.defense.JPEG(model, conf, adv_method, **kwgs)
描述：通过加噪方式消除对抗样本威胁，实现defense、eval两个函数

model (nn.Module) – 模型对象.
conf (dict) - {"model": 模型名称, "dataset": 数据集名称, "mean": 数据mean List[float], "std": 数据std List[float], "num_classes": 标签数量}
**kwgs (dict) - JPEG算法需要的其它参数


> def JPEG.defense(images, labels, jpeg_quality)
输入：
images (torch.array) - 嫌疑对抗样本，e.g., torch.float([x1, x2, x3,...,])
labels (torch.array) - 样本真实类别，e.g., torch.long([y1, y2, y3,...,])
jpeg_quality (float) - JPEG压缩比例, e.g., 0.9

输出：
images (torch.array) - 清洗后样本，e.g., torch.float([x1, x2, x3,...,])


> def JPEG.eval(model, images, labels)
输入：
model (nn.Module) – 模型对象.
images (torch.array) - 待检测样本，e.g., torch.float([x1, x2, x3,...,])
labels (torch.array) - 样本真实类别，e.g., torch.long([y1, y2, y3,...,])

输出：
acc (torch.array) - 验证准确率
tpr (torch.array) - 验证tpr
fpr (torch.array) - 验证fpr
```



## 4.后门攻击接口
```text


```





