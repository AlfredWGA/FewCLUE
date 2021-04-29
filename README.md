# FewCLUE

中文小样本学习测评基准 FewCLUE:Few-shot learning for Chinese Language Understanding Evaluation

## 简介 Intorudction 
 预训练语言模型，包括用于语言理解或文本生成的模型，通过海量文本语料上做语言模型的预训练的方式，极大提升了NLP领域上多种任务上的表现并扩展了NLP的应用。使用预训练语言模型结合成数千或上万的标注样本，在下游任务上做微调，通常可以取得在特定任务上较好的效果；但相对于机器需要的大量样本，人类可以通过极少数量的样本上的学习来学会特定的物体的识别或概念理解。
 
 小样本学习（Few-shot Learning）正是解决这类在极少数据情况下的机器学习问题。结合预训练语言模型通用和强大的泛化能力基础上，探索小样本学习最佳模型和中文上的实践，是本课题的目标。FewCLUE：中文小样本学习测评基准，基于CLUE的积累和经验，并结合少样本学习的特点和近期的发展趋势，精心设计了该测评，希望可以促进中文领域上少样本学习领域更多的研究、应用和发展。

## 任务描述和统计 Task Descriptions and Statistics
| Corpus   | Train     | Dev  |Test Public| Test Private | Num Labels| Unlabeled| Task | Metric | Source |
| :----:| :----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |:----:  |
|   | Single |Sentence | Tasks  |
|   EPRSTMT    | 32 | 32 | 610 | 753 | 2 | 19565 | SntmntAnalysis | Acc | E-CommrceReview |
|   CSLDCP    | 536 |536   | 1784| 2999 | 67 | 18111 | LongTextClassify | Acc |AcademicCNKI |
|   TNEWS    | 240 | 240 |2010| 1500 | 15 |20000| ShortTextClassify | Acc |NewsTitle |
|    IFLYTEK   | 928 | 690  | 1749  | 2279 | 119  | 7558 | LongTextClassify| Acc |AppDesc |
|     | Sentence | Pair | Tasks |
|    OCNLI   | 32  | 32  |  2520 |  3000 | 3  | 20000 | NLI  |  Acc | 5Genres |
|    BUSTM   | 32 | 32  | 1772 | 2000  | 2 | 4251|SemanticSmlarty | Acc | AIVirtualAssistant | 
|   |Reading |Comprhnsn |Tasks |
|     CHID  | 42 |  42 | 2002 | 2000  | 7？ | 7585 |  MultipleChoice,idiom | Acc  | Novel,EssayNews |
|     CSL  | 32 |  32 | 2828 | 3000 | 2? | 19841 | KeywordRecogntn| Acc | AcademicCNKI| 
|     CLUEWSC  | 32 | 32  |  976 | 290  | 2 | 0| CorefResolution  | Acc | ChineseFictionBooks 

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


## 基线模型及运行 Baselines and Know to run
    目前支持4类代码：直接fine-tuning、PET、Ptuning、GPT
    
    直接fine-tuning: 
        一键运行.基线模型与代码
        1、克隆项目 
           git clone https://github.com/CLUEbenchmark/FewCLUE.git
        2、进入到相应的目录
           分类任务  
               例如：
               cd FewCLUEDatasets/baseline/models_tf/fine_tuning/bert/
        3、运行对应任务的脚本(GPU方式): 会自动下载模型并开始运行。
           bash run_classifier_xxx.sh
           如运行 bash run_classifier_ecomments.sh 会开始cecmmnt任务的训练和评估
    
    PET/Ptuning/GPT:
        环境准备：
          预先安装Python 3.x(或2.7), Tesorflow 1.14+, Keras 2.3.1, bert4keras。
          需要预先下载预训练模型：chinese_roberta_wwm_ext，并放入到pretrained_models目录下
        
        运行：
        1、进入到相应的目录，运行相应的代码。以ptuning为例：
           cd ./baselines/models_keras/ptuning
        2、运行代码
           python3 ptuning_iflytek.py
              

## 数据集介绍 Introduction of datasets

####   分类任务 Single Sentence Tasks
##### 1. EPRSTMT（EPR-sentiment）  电商产品评论情感分析数据集  E-commerce Product Review Dataset for Sentiment Analysis
```  电商产品评论的情感分析，根据评论来确定情感的极性，正向或负向。
     数据量：训练集（32），验证集（32），公开测试集（610），测试集（753），无标签语料（19565）
     
     例子：
     {"id": 23, "sentence": "外包装上有点磨损，试听后感觉不错", "label": "Positive"}
     每一条数据有三个属性，从前往后分别是 id,sentence,label。其中label标签，Positive 表示正向，Negative 表示负向。
```

##### 2. CSLDCP  中文科学文献学科分类数据集     
```  
     中文科学文献学科分类数据集，包括67个类别的文献类别，这些类别来自于分别归属于13个大类，范围从社会科学到自然科学，文本为文献的中文摘要。
     数据量：训练集（536），验证集（536），公开测试集（1784），测试集（2999），无标签语料（67）
     
     例子：
     {"id": 23, "sentence": "外包装上有点磨损，试听后感觉不错", "label": "Positive"}
     每一条数据有三个属性，从前往后分别是 id,sentence,label。其中label标签，Positive 表示正向，Negative 表示负向。
```


##### 3.TNEWS 今日头条中文新闻（短文本）分类数据集 Toutiao Short Text Classificaiton for News
     该数据集来自今日头条的新闻版块，共提取了15个类别的新闻，包括旅游、教育、金融、军事等。
```  数据量：训练集（240），验证集（240），公开测试集（2010），测试集（1500），无标签语料（20000）
     
     例子：
     {"label": "102", "label_des": "news_entertainment", "sentence": "江疏影甜甜圈自拍，迷之角度竟这么好看，美吸引一切事物"}
     每一条数据有三个属性，从前往后分别是 分类ID，分类名称，新闻字符串（仅含标题）。
```

##### 4.IFLYTEK 长文本分类数据集 Long Text classification
    该数据集关于app应用描述的长文本标注数据，包含和日常生活相关的各类应用主题，共119个类别："打车":0,"地图导航":1,"免费WIFI":2,"租车":3,….,"女性":115,"经营":116,"收款":117,"其他":118(分别用0-118表示)。
``` 数据量：训练集（928），验证集（690），公开测试集（1749），测试集（2279），无标签语料（7558）
    
    例子：
    {"label": "110", "label_des": "社区超市", "sentence": "朴朴快送超市创立于2016年，专注于打造移动端30分钟即时配送一站式购物平台，商品品类包含水果、蔬菜、肉禽蛋奶、海鲜水产、粮油调味、酒水饮料、休闲食品、日用品、外卖等。朴朴公司希望能以全新的商业模式，更高效快捷的仓储配送模式，致力于成为更快、更好、更多、更省的在线零售平台，带给消费者更好的消费体验，同时推动中国食品安全进程，成为一家让社会尊敬的互联网公司。,朴朴一下，又好又快,1.配送时间提示更加清晰友好2.保障用户隐私的一些优化3.其他提高使用体验的调整4.修复了一些已知bug"}
    每一条数据有三个属性，从前往后分别是 类别ID，类别名称，文本内容。
```

#### Sentence Pair Tasks 
##### 5.OCNLI 中文原版自然语言推理数据集 Original Chinese Natural Language Inference
    OCNLI，即原生中文自然语言推理数据集，是第一个非翻译的、使用原生汉语的大型中文自然语言推理数据集。
    数据量：训练集（32），验证集（32），公开测试集（2520），测试集（3000），无标签语料（20000）
    
    例子：
    {
    "level":"medium",
    "sentence1":"身上裹一件工厂发的棉大衣,手插在袖筒里",
    "sentence2":"身上至少一件衣服",
    "label":"entailment","label0":"entailment","label1":"entailment","label2":"entailment","label3":"entailment","label4":"entailment",
    "genre":"lit","prem_id":"lit_635","id":0
    }
    
##### 6.BUSTM 小布助手对话短文本匹配数据集 XiaoBu Dialogue Short Text Matching 
    对话短文本语义匹配数据集，源于小布助手。它是OPPO为品牌手机和IoT设备自研的语音助手，为用户提供便捷对话式服务。
    意图识别是对话系统中的一个核心任务，而对话短文本语义匹配是意图识别的主流算法方案之一。要求根据短文本query-pair，预测它们是否属于同一语义。
    
    数据量：训练集（32），验证集（32），公开测试集（1772），测试集（2000），无标签语料（4251）
    例子：
    {"id": 5, "sentence1": "女孩子到底是不是你", "sentence2": "你不是女孩子吗", "label": "1"}
    {"id": 18, "sentence1": "小影,你说话慢了", "sentence2": "那你说慢一点", "label": "0"}

#### Reading Comprehension Tasks 
##### 7.ChID 成语阅读理解填空 Chinese IDiom Dataset for Cloze Test
    以成语完形填空形式实现，文中多处成语被mask，候选项中包含了近义的成语。 https://arxiv.org/abs/1906.01265
    数据量：训练集（42），验证集（42），公开测试集（2002），测试集（2000），无标签语料（7585）
    
    例子：
    {"id": 1421, "candidates": ["巧言令色", "措手不及", "风流人物", "八仙过海", "平铺直叙", "草木皆兵", "言行一致"],
    "content": "当广州憾负北控,郭士强黯然退场那一刻,CBA季后赛悬念仿佛一下就消失了,可万万没想到,就在时隔1天后,北控外援约瑟夫-杨因个人裁决案(拖欠上一家经纪公司的费用),
    导致被禁赛,打了马布里一个#idiom#,加上郭士强带领广州神奇逆转天津,让...", "answer": 1}

##### 8.CSL 论文关键词识别 Keyword Recognition
    中文科技文献数据集(CSL)取自中文论文摘要及其关键词，论文选自部分中文社会科学和自然科学核心期刊，任务目标是根据摘要判断关键词是否全部为真实关键词（真实为1，伪造为0）。
    数据量：训练集（32），验证集（32），公开测试集（2828），测试集（3000），无标签语料（19841）
    
    例子： 
    {"id": 1, "abst": "为解决传统均匀FFT波束形成算法引起的3维声呐成像分辨率降低的问题,该文提出分区域FFT波束形成算法.远场条件下,
    以保证成像分辨率为约束条件,以划分数量最少为目标,采用遗传算法作为优化手段将成像区域划分为多个区域.在每个区域内选取一个波束方向,
    获得每一个接收阵元收到该方向回波时的解调输出,以此为原始数据在该区域内进行传统均匀FFT波束形成.对FFT计算过程进行优化,降低新算法的计算量,
    使其满足3维成像声呐实时性的要求.仿真与实验结果表明,采用分区域FFT波束形成算法的成像分辨率较传统均匀FFT波束形成算法有显著提高,且满足实时性要求.",
     "keyword": ["水声学", "FFT", "波束形成", "3维成像声呐"], "label": "1"}
     
    每一条数据有四个属性，从前往后分别是 数据ID，论文摘要，关键词，真假标签。

##### 9.CLUEWSC  WSC Winograd模式挑战中文版
    Winograd Scheme Challenge（WSC）是一类代词消歧的任务，即判断句子中的代词指代的是哪个名词。题目以真假判别的方式出现，如：  
    句子：这时候放在[床]上[枕头]旁边的[手机]响了，我感到奇怪，因为欠费已被停机两个月，现在[它]突然响了。需要判断“它”指代的是“床”、“枕头”，还是“手机”？
    从中国现当代作家文学作品中抽取，再经语言专家人工挑选、标注。  
    
    数据量：训练集（32），验证集（32），公开测试集（976），测试集（290），无标签语料（0）
    例子：  
     {"target": 
         {"span2_index": 37, 
         "span1_index": 5, 
         "span1_text": "床", 
         "span2_text": "它"}, 
     "idx": 261, 
     "label": "false", 
     "text": "这时候放在床上枕头旁边的手机响了，我感到奇怪，因为欠费已被停机两个月，现在它突然响了。"}
     "true"表示代词确实是指代span1_text中的名词的，"false"代表不是。 

## 任务构建过程与调查问卷 Construction of Tasks
任务构建过程与调查问卷

    调查问卷
    
    调查背景
    调查问卷主要针对任务和数据集设定进⾏，调查对象为FewCLUE⼩小样本学习交流群，获得35份有效样本。
    
    调查问卷主要反馈： 
    1)希望任务丰富多样、适应真实场景; 
    2)数据集数量量: 提供9个左右数据集；
    3)当个任务数量量:按类别采样16为主; 
    4)半监督学习:⼩小样本测试还应提供⼤大量量⽆无标签数据；
    5)测试零样本学习；
    
   详见：<a href='https://github.com/CLUEbenchmark/FewCLUE/blob/main/resources/questionnaire/FewCLUE%E8%B0%83%E6%9F%A5%E9%97%AE%E5%8D%B7-%E5%8F%8D%E9%A6%88%E4%BF%A1%E6%81%AF.pdf'>FewCLUE调查问卷-反馈信息</a>

## 数据集文件结构 Data set Structure
    5份训练集，对应5份验证集，1份公开测试集，1份用于提交测试集，1份无标签样本，1份合并后的训练和验证集
    
    单个数据集目录结构：
        train_0.json：训练集0
        train_1.json：训练集1
        train_2.json：训练集2
        train_3.json：训练集3
        train_4.json：训练集4
        train_few_all.json： 合并后的训练集，即训练集0-4合并去重后的结果
        
        dev_0.json：验证集0，与训练集0对应
        dev_0.json：验证集1，与训练集1对应
        dev_0.json：验证集2，与训练集2对应
        dev_0.json：验证集3，与训练集3对应
        dev_0.json：验证集4，与训练集4对应
        dev_few_all.json： 合并后的验证集，即验证集0-4合并去重后的结果
        
        test_public.json：公开测试集，用于测试，带标签
        test.json: 测试集，用于提交，不能带标签
        
        unlabeled.json: 无标签的大量样本

## 测评报名|提交 Submit

<a href='https://www.CLUEbenchmarks.com'>提交</a>到测评系统(5月份开放，五一之后)

## 教程 Tutorial
   1.系列PPT分享资料，详见: <a href='https://github.com/CLUEbenchmark/FewCLUE/tree/main/resources/ppt'>PPT</a>
   
   2.教程（Jupyter Notebook/Google Colab），添加中。。。

## 问题 Question
    1. 问：测试系统，什么时候开发？
       答：测评系统在5月1节后才会开放。

## 贡献与参与 Contribution & Participation
    1.问：我有符合代码规范的模型代码，并经过测试，可以贡献到这个项目吗？
     答：可以的。你可以提交一个pull request，并写上说明。
    
    2.问：我正在研究小样本学习，具有较强的模型研究能力，怎么参与到此项目？
      答：发送邮件到 CLUEbenchmark@163.com，标题为：参与FewCLUE课题，并介绍一下你的研究。


## 引用
    @misc{FewCLUE,
      title={FewCLUE:Few-shot learning for Chinese Language Understanding Evaluation},
      author={CLUE benchmark},
      year={2021},
      howpublished={\url{https://github.com/CLUEbenchmark/FewCLUE}},
    }