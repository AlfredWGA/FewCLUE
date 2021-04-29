# FewCLUE

中文小样本学习测评基准 FewCLUE: Few-shot learning for Chinese Language Understanding Evaluation

## 简介 Intorudction 
 预训练语言模型，包括用于语言理解或文本生成的模型，通过海量文本语料上做语言模型的预训练的方式，极大提升了NLP领域上多种任务上的表现并扩展了NLP的应用。使用预训练语言模型结合成数千或上万的标注样本，在下游任务上做微调，通常可以取得在特定任务上较好的效果；但相对于机器需要的大量样本，人类可以通过极少数量的样本上的学习来学会特定的物体的识别或概念理解。
 
 小样本学习（Few-shot Learning）正是解决这类在极少数据情况下的机器学习问题。结合预训练语言模型通用和强大的泛化能力基础上，探索小样本学习最佳模型和中文上的实践，是本课题的目标。FewCLUE：中文小样本学习测评基准，基于CLUE的积累和经验，并结合少样本学习的特点和近期的发展趋势，精心设计了该测评，希望可以促进中文领域上少样本学习领域更多的研究、应用和发展。

## 任务描述和统计 Task Descriptions and Statistics
| Corpus   | Train     | Dev  |Test Public| Test Private | Num Labels| Unlabeled| Task | Metric | Source |
| :----:| :----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |
|   | Single |Sentence | Tasks  |
|   EPRSTMT    | 32 | 32 | 610(少) | 753(少) | 2 | 19565 | SntmntAnalysis | Acc | E-CommrceReview |
|   CSLDCP    | 536 |536   | 1784| 2999 | 65? | 18111 | LongTextClassify | Acc |AcademicCNKI |
|   TNEWS    | 240 | 240 |2010| 1500 | 15 |20000| ShortTextClassify | Acc |NewsTitle |
|    IFLYTEK   | 928 | 690  | 1749  | 2279 | 100+  | 7558 | LongTextClassify| Acc |AppDesc |
|     | Sentence | Pair | Tasks |
|    OCNLI   | 32  | 32  |  2520 |  3000 | 3  | 20000 | NLI  |  Acc | 5Genres |
|    BUSTM   | 32 | 32  | 1772 | 2000  | 2 | 4251|SemanticSmlarty | Acc | AIVirtualAssistant | 
|   |Reading |Comprhnsn |Tasks |
|     CHID  | 42 |  42 | 2002 | 2000  | 7？ | 7585 |  MultipleChoice,idiom | Acc  | Novel,EssayNews |
|     CSL  | 32 |  32 | 2828 | 3000 | 2? | 19841 | KeywordRecogntn| Acc | AcademicCNKI| 
|     CLUEWSC  | 32 | 32  |  976（少） | 290(少）  | 2 | 0（少）| CorefResolution  | Acc | ChineseFictionBooks 

    EPRSTMT:电商评论情感分析；CSLDCP：科学文献学科分类；TNEWS:新闻分类；IFLYTEK:APP应用描述主题分类；
    OCNLI: 自然语言推理；BUSTM: 对话短文本匹配；CHID:成语阅读理解；CSL:摘要判断关键词判别；CLUEWSC:代词消歧

## 实验结果
实验设置：训练集和验证集使用32个样本，或采样16个，测试集政策规模。使用RoBERT12层chinese_roberta_wwm_ext作为基础模型。

| 模型   | score     | cecmmnt  | bustm  | ocnli   | csldcp   | tnews | wsc | ifytek| csl | chid  |    
| :----:| :----:  | :----: |:----: |:----: |:----: |:----: |:----: |:----: |:----: |:----: |
| <a href="#">Human</a>        | - |?   | ?    |  90.3  | ？ |71.0 | 98.0 | 66.0 |  84.0|  87.1|
| <a href="https://github.com/ymcui/Chinese-BERT-wwm">TrainAll</a>        | - |-   | -     | -  |  |-  | -  | -  | - | 1- |
| <a href="https://github.com/ymcui/Chinese-BERT-wwm">FineTuning</a>        | - |70.2   | 63.1    | 35.3  |  |52.0N | 49.3N | 17.9N | 50.0N| 15.0N|
| <a href="#">PET</a>      | - | 78.6N | 64.0  | 36.0 |  |51.2N  | 50.0N| 35.1N | 55.0N | 57.5N |
| <a href="#">PtuningB</a>      | - | 88.5N | 65.4  | 35.9 |  |  48.2N  | 51.0N | 32.0N| 50.0N | 15.0N |
| <a href="#">PtuningGPT</a>      | - | 76.4？  | 60.4？   |   |   |  45.3N   | 49.0N | 24.0N | 53.5N  | 13.7N  |
| <a href="#">Zero-shot</a>      | - |   |    |   |   |   25.3N  | 50.0N | 27.7N |  52.2N |  52.2N |
| <a href="#">半监督</a>      | - |   |    |   |   |     |  |  |   |   |

    PtuningB: Ptuning_RoBERTa; PtuningGPT: Ptuning_GPT; Zero-shot: GPT类Zero-shot; TrainAll: 在5份合并后的数据上训练；半监督：小样本+无标签数据;
    N”，代表已更新。wsc: cluewsc; cecmnt：cecmmnt(sentiment)，情感2分类; bustm: bustm(opposts); 
    ?：代表新的数据集下还没有跑过实验。如跑过实验了，去掉“？”，改为N。


## FewCLUE特点
1、任务类型多样、具有广泛代表性。包含多个不同类型的任务，包括情感分析任务、自然语言推理、多种文本分类、文本匹配任务和成语阅读理解等。

2、研究性与应用性结合。在任务构建、数据采样阶段，即考虑到了学术研究的需要，也兼顾到实际业务场景对小样本学习的迫切需求。
如针对小样本学习中不实验结果的不稳定问题，我们采样生成了多份训练和验证集；考虑到实际业务场景类别，我们采用了多个有众多类别的任务（如50+、100+多分类），
并在部分任务中存在类别不均衡的问题。

3、时代感强。测评的主要目标是考察小样本学习，我们也同时测评了模型的零样本学习、半监督学习的能力。不仅能考察BERT类擅长语言理解的模型，
也可以同时查考了近年来发展迅速的GPT-3这类生成模型的中文版本在零样本学习、小样本学习上的能力；

此外，我们提供小样本测评完善的基础设施。
从任务设定，广泛的数据集，多个有代表性的基线模型及效果对比，一键运行脚本，小样本学习教程，到测评系统、学术论文等完整的基础设施。


## 基线模型：运行及介绍（附图） Baselines and Know to run
基线模型：运行及介绍 baseline

## 数据集介绍与下载 Introduction of datasets

##### 1. EPRSTMT（EPR-sentiment）  电商产品评论情感分析数据集  E-commerce Product Review Dataset for Sentiment Analysis
```
     数据量：训练集（32），验证集（32），公开测试集（610），测试集（753），无标签语料（19565）
     例子：
     {"id": 23, "sentence": "外包装上有点磨损，试听后感觉不错", "label": "Positive"}
     每一条数据有三个属性，从前往后分别是 id,sentence,label。其中label标签，Positive 表示正向，Negative 表示负向。
```

##### 2. CSLDCP  中文科学文献学科分类数据集  
```
     例子：
     {"id": 23, "sentence": "外包装上有点磨损，试听后感觉不错", "label": "Positive"}
     每一条数据有三个属性，从前往后分别是 id,sentence,label。其中label标签，Positive 表示正向，Negative 表示负向。
```


##### 3.TNEWS' 今日头条中文新闻（短文本）分类数据集 Toutiao Short Text Classificaiton for News
    该数据集来自今日头条的新闻版块，共提取了15个类别的新闻，包括旅游，教育，金融，军事等。
```
     例子：
     {"label": "102", "label_des": "news_entertainment", "sentence": "江疏影甜甜圈自拍，迷之角度竟这么好看，美吸引一切事物"}
     每一条数据有三个属性，从前往后分别是 分类ID，分类名称，新闻字符串（仅含标题）。
```

##### 4.IFLYTEK' 长文本分类数据集 Long Text classification
    该数据集关于app应用描述的长文本标注数据，包含和日常生活相关的各类应用主题，共119个类别："打车":0,"地图导航":1,"免费WIFI":2,"租车":3,….,"女性":115,"经营":116,"收款":117,"其他":118(分别用0-118表示)。
```
    例子：
    {"label": "110", "label_des": "社区超市", "sentence": "朴朴快送超市创立于2016年，专注于打造移动端30分钟即时配送一站式购物平台，商品品类包含水果、蔬菜、肉禽蛋奶、海鲜水产、粮油调味、酒水饮料、休闲食品、日用品、外卖等。朴朴公司希望能以全新的商业模式，更高效快捷的仓储配送模式，致力于成为更快、更好、更多、更省的在线零售平台，带给消费者更好的消费体验，同时推动中国食品安全进程，成为一家让社会尊敬的互联网公司。,朴朴一下，又好又快,1.配送时间提示更加清晰友好2.保障用户隐私的一些优化3.其他提高使用体验的调整4.修复了一些已知bug"}
    每一条数据有三个属性，从前往后分别是 类别ID，类别名称，文本内容。
```

##### 5.OCNLI 中文原版自然语言推理数据集 Original Chinese Natural Language Inference
    OCNLI，即原生中文自然语言推理数据集，是第一个非翻译的、使用原生汉语的大型中文自然语言推理数据集。
    
    例子：
    {
    "level":"medium",
    "sentence1":"身上裹一件工厂发的棉大衣,手插在袖筒里",
    "sentence2":"身上至少一件衣服",
    "label":"entailment","label0":"entailment","label1":"entailment","label2":"entailment","label3":"entailment","label4":"entailment",
    "genre":"lit","prem_id":"lit_635","id":0
    }

## 任务构建过程与调查问卷 Construction of Tasks
任务构建过程与调查问卷

## 测评报名|提交 Submit
测评报名|提交 Submit

## 数据集文件结构 Data set Structure
    5份训练集，对应5份验证集，1份公开测试集，1份用于提交测试集，1份无标签样本，1份合并后的训练和验证集
    train_0.json：训练集0
    train_1.json：训练集1
    train_2.json：训练集2
    train_3.json：训练集3
    train_4.json：训练集4
    train_few_all.json： 合并后的训练集，即训练集0-4合并去重后的结果
    dev_0.json：验证集0
    dev_0.json：验证集1
    dev_0.json：验证集2
    dev_0.json：验证集3
    dev_0.json：验证集4
    dev_few_all.json： 合并后的验证集，即验证集0-4合并去重后的结果
    test_public.json：公开测试集，用于测试，带标签
    test.json: 测试集，用于提交，不能带标签
    unlabeled.json: 无标签的大量样本

## 教程 Tutorial
教程（Jupyter Notebook/Google Colab）

## 贡献与参与 Contribution & Participation
贡献与参与

## 引用
引用