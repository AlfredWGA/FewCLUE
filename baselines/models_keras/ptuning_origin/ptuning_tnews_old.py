#! -*- coding:utf-8 -*-
# 情感分析例子，利用MLM+P-tuning
# P-tuning: 模板(patter)可以自己学习到，不需要是自然语言；可以只学习少量的（如10个）的embedding，而不用学习所有的embedding.

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import numpy as np
from bert4keras.backend import keras, K
from bert4keras.snippets import sequence_padding, DataGenerator
from bert4keras.snippets import open
import json
import sys
from modeling import tokenizer

label_en2zh ={'news_tech':'科技','news_entertainment':'娱乐','news_car':'汽车','news_travel':'旅游','news_finance':'财经',
              'news_edu':'教育','news_world':'国际','news_house':'房产','news_game':'电竞','news_military':'军事',
              'news_story':'故事','news_culture':'文化','news_sports':'体育','news_agriculture':'农业'}
labels=[label_zh for label_en,label_zh in label_en2zh.items()]
labels_en=[label_en for label_en,label_zh in label_en2zh.items()]

maxlen = 128
batch_size = 16


# 加载数据的方法
def load_data(filename): # 加载数据
    D = []
    with open(filename, encoding='utf-8') as f:
        for i, l in enumerate(f):
            l = json.loads(l)
            label_en=l['label_desc']
            if label_en not in labels_en:
                continue
            label_zh=label_en2zh[label_en] # 将英文转化为中文
            D.append((l['sentence'], label_zh))
    return D


path = '../../../datasets/tnews'
data_num = sys.argv[1]
# 加载数据集
train_data = load_data('{}/train_{}.json'.format(path, data_num))
valid_data = load_data('{}/dev_{}.json'.format(path, data_num))
test_data = load_data('{}/test_public.json'.format(path))


# 对应的任务描述
mask_idxs = [1, 2] # [7, 8] # mask_idx = 1 #5
unused_length=9 # 6,13没有效果提升
desc = ['[unused%s]' % i for i in range(1, unused_length)] # desc: ['[unused1]', '[unused2]', '[unused3]', '[unused4]', '[unused5]', '[unused6]', '[unused7]', '[unused8]']
for mask_id in mask_idxs:
    desc.insert(mask_id - 1, '[MASK]')            # desc: ['[unused1]', '[unused2]', '[unused3]', '[unused4]', '[unused5]', '[unused6]', '[MASK]', '[MASK]', '[unused7]', '[unused8]']
desc_ids = [tokenizer.token_to_id(t) for t in desc] # 将token转化为id

# pos_id = tokenizer.token_to_id(u'很') # e.g. '[unused9]'. 将正向的token转化为id. 默认值：u'很'
# neg_id = tokenizer.token_to_id(u'不') # e.g. '[unused10]. 将负向的token转化为id. 默认值：u'不'


def random_masking(token_ids):
    """对输入进行mask
    在BERT中，mask比例为15%，相比auto-encoder，BERT只预测mask的token，而不是重构整个输入token。
    mask过程如下：80%机会使用[MASK]，10%机会使用原词,10%机会使用随机词。
    """
    rands = np.random.random(len(token_ids)) # rands: array([-0.34792592,  0.13826393,  0.8567176 ,  0.32175848, -1.29532141, -0.98499201, -1.11829718,  1.18344819,  1.53478554,  0.24134646])
    source, target = [], []
    for r, t in zip(rands, token_ids):
        if r < 0.15 * 0.8:   # 80%机会使用[MASK]
            source.append(tokenizer._token_mask_id)
            target.append(t)
        elif r < 0.15 * 0.9: # 10%机会使用原词
            source.append(t)
            target.append(t)
        elif r < 0.15:       # 10%机会使用随机词
            source.append(np.random.choice(tokenizer._vocab_size - 1) + 1)
            target.append(t)
        else: # 不进行mask
            source.append(t)
            target.append(0)
    return source, target


class data_generator(DataGenerator):
    """数据生成器
    # TODO TODO TODO 这里面的每一行代码，，，
    目前看只是将原始文本转换为token id
    负向样本（输入是一个[MASK]字符，输出是特定的字符。对于负样本，采用"不"，正样本，采用“很”）
    """
    def __iter__(self, random=False): # TODO 这里的random是指否需要对原始文本进行mask
        batch_token_ids, batch_segment_ids, batch_output_ids = [], [], []
        for is_end, (text, label) in self.sample(random):
            token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
            if label != 2:
                token_ids = token_ids[:1] + desc_ids + token_ids[1:] # # token_ids[:1] = [CLS]
                segment_ids = [0] * len(desc_ids) + segment_ids
            if random: # 暂时没有用呢
                source_ids, target_ids = random_masking(token_ids)
            else:
                source_ids, target_ids = token_ids[:], token_ids[:]
            #label_ids = tokenizer.encode(label)[0][1:-1] # label_ids: [1092, 752] ;tokenizer.token_to_id(label[0]): 1092. 得到标签（如"财经"）对应的词汇表的编码ID。label_ids: [1093, 689]。 e.g. [101, 1093, 689, 102] =[CLS,农,业,SEP]. tokenizer.encode(label): ([101, 1093, 689, 102], [0, 0, 0, 0])
            # print("label_ids:",label_ids,";tokenizer.token_to_id(label[0]):",tokenizer.token_to_id(label[0]))
            for i,mask_id in enumerate(mask_idxs):
                source_ids[mask_id] = tokenizer._token_mask_id
                target_ids[mask_id] = tokenizer.token_to_id(label[i]) # token_to_id与tokenizer.encode可以实现类似的效果。

            batch_token_ids.append(source_ids)
            batch_segment_ids.append(segment_ids)
            batch_output_ids.append(target_ids)
            if len(batch_token_ids) == self.batch_size or is_end: # padding操作
                batch_token_ids = sequence_padding(batch_token_ids)
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_output_ids = sequence_padding(batch_output_ids)
                yield [
                    batch_token_ids, batch_segment_ids, batch_output_ids
                ], None
                batch_token_ids, batch_segment_ids, batch_output_ids = [], [], []


from modeling import get_model
model, train_model = get_model(pattern_len=unused_length, trainable=True, lr=3e-5)

# 转换数据集
train_generator = data_generator(train_data, batch_size)
valid_generator = data_generator(valid_data, batch_size*10)
test_generator = data_generator(test_data, batch_size*10)


class Evaluator(keras.callbacks.Callback):
    def __init__(self):
        self.best_val_acc = 0.

    def on_epoch_end(self, epoch, logs=None):
        val_acc = evaluate(valid_generator)
        if val_acc > self.best_val_acc: #  保存最好的模型，并记录最好的准确率
            self.best_val_acc = val_acc
            # model.save_weights('best_model_bert_ptuning.weights')
        test_acc = evaluate(test_generator)
        print( # 打印准确率
            u'val_acc: %.5f, best_val_acc: %.5f, test_acc: %.5f\n' %
            (val_acc, self.best_val_acc, test_acc)
        )

def evaluate(data):
    """
    计算候选标签列表中每一个标签（如'科技'）的联合概率，并与正确的标签做对比。候选标签的列表：['科技','娱乐','汽车',..,'农业']
    y_pred=(32, 2, 21128)=--->(32, 1, 14) = (batch_size, 1, label_size)---argmax--> (batch_size, 1, 1)=(batch_size, 1, index in the label)
    :param data:
    :return:
    """
    label_ids = np.array([tokenizer.encode(l)[0][1:-1] for l in labels]) # 获得两个字的标签对应的词汇表的id列表，如: label_id=[1093, 689]。label_ids=[[1093, 689],[],[],..[]]tokenizer.encode('农业') = ([101, 1093, 689, 102], [0, 0, 0, 0])
    total, right = 0., 0.
    for x_true, _ in data:
        x_true, y_true = x_true[:2], x_true[2] # x_true = [batch_token_ids, batch_segment_ids]; y_true: batch_output_ids
        y_pred = model.predict(x_true)[:, mask_idxs] # 取出特定位置上的索引下的预测值。y_pred=[batch_size, 2, vocab_size]。mask_idxs = [7, 8]
        # print("y_pred:",y_pred.shape,";y_pred:",y_pred) # (32, 2, 21128)
        # print("label_ids",label_ids) # [[4906 2825],[2031  727],[3749 6756],[3180 3952],[6568 5307],[3136 5509],[1744 7354],[2791  772],[4510 4993],[1092  752],[3125  752],[3152 1265],[ 860 5509],[1093  689]]
        y_pred = y_pred[:, 0, label_ids[:, 0]] * y_pred[:, 1, label_ids[:, 1]] # y_pred=[batch_size,1,label_size]=[32,1,14]。联合概率分布。 y_pred[:, 0, label_ids[:, 0]]的维度为：[32,1,21128]
        # print("y_pred[:, 0, label_ids[:, 0]]:",y_pred[:, 0, label_ids[:, 0]])
        y_pred = y_pred.argmax(axis=1) # 找到概率最大的那个label(词,如“财经”)所在的索引(index)。
        # print("y_pred:",y_pred.shape,";y_pred:",y_pred) # O.K. y_pred: (16,) ;y_pred: [4 0 4 1 1 4 5 3 9 1 0 9]
        # print("y_true.shape:",y_true.shape,";y_true:",y_true) # y_true: (16, 128)
        # y_true=[batch_size,sequence_length]=(16,128); y_true[:, mask_idxs]=[batch_size,2]
        y_true = np.array([labels.index(tokenizer.decode(y)) for y in y_true[:, mask_idxs]]) # 找到标签对应的ID,对应的文本，对应的标签列表中所在的顺序。 labels=['科技','娱乐',...,'汽车']
        total += len(y_true)
        right += (y_true == y_pred).sum()
    return right / total


if __name__ == '__main__':

    evaluator = Evaluator()

    train_model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=len(train_generator) * 1,
        epochs=20,
        callbacks=[evaluator]
    )

else:

    model.load_weights('best_model_bert_ptuning.weights')