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
描述：检测对抗样本的类，实现detect、eval两个函数的类

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
描述：通过加噪方式消除对抗样本威胁，实现defense、eval两个函数的类

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
> class aicert.module.backdoor.attack.BadNet(model, conf, **kwgs)
描述：通过微调已经训练好的模型，在其中添加后门的类

model (nn.Module) – 模型对象.
conf (dict) - {"model": 模型名称, "dataset": 数据集名称, "mean": 数据mean List[float], "std": 数据std List[float], "num_classes": 标签数量, "targeted": 后门攻击修改的标签}
**kwgs (dict) - BadNet算法整体需要的其它参数


> def BadNet.train(train_loader, lr, steps, **kwgs)
输入：
train_loader (torchvison.Dataloader) – 训练数据集.
lr (float) - learning rate, e.g., 1e-4
steps (int) - 微调迭代次数，e.g., 100
**kwgs (dict) - BadNet算法微调需要的其它参数
输出：
model (nn.Module) – 植入后门的模型对象.


> def JPEG.eval(model, test_loader)
输入：
model (nn.Module) – 模型对象.
test_loader (torchvison.Dataloader) – 测试数据集.
输出：
acc (torch.array) - 验证准确率
iou (torch.array) - 分割IOU
```


## 4.后门防御接口
```text
> class aicert.module.backdoor.attack.NeuralCleanse(model, conf, **kwgs)
> class aicert.module.backdoor.attack.STRIP(model, conf, **kwgs)
描述：检测模型中存在的后门trigger，并逆向trigger的类

model (nn.Module) – 模型对象.
conf (dict) - {"model": 模型名称, "dataset": 数据集名称, "mean": 数据mean List[float], "std": 数据std List[float], "num_classes": 标签数量, "targeted": 后门攻击修改的标签}
**kwgs (dict) - STRIP算法整体需要的其它参数


> def STRIP.detect(data_loader, **kwgs)
描述：检测后门函数
输入：
data_loader (torchvison.Dataloader) – 校验数据集.
**kwgs (dict) - STRIP算法微调需要的其它参数
输出：
prob (torch.array) – 模型存在后门预测置信度.


> def STRIP.reverse(data_loader, **kwgs)
描述：逆向trigger函数
输入：
data_loader (torchvison.Dataloader) – 校验数据集.
**kwgs (dict) - STRIP算法微调需要的其它参数
输出：
images (torch.array) – 逆向出来的trigger图像.
```


