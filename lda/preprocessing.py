#coding: utf-8

'''
这个文件的主要作用是将语料库转换成blei转换的形式，在lda的时候调用该函数进行读取
语料库的形式采取AP语料库的形式，可能会有一点麻烦，但是应该很好用
先不去停顿词表，看看效果
'''
from read_conf import config
import sys

#这个函数主要是stem每个词
#按照以下规则过滤
#1.全部小写
#2.去掉所有不是字母的，对于I'm这种形式，保留成im
#3.去掉停顿词
#4.去掉长度小于等于2的词（其实这么做有可能不好）
def stem_line(line,stop_list):
    #先全部小写
    line = line.lower()
    line = line.split()
    result = []

    g = lambda x:x.isalpha()
    for word in line:
        nw = filter(g,word)
        if len(nw)>=3 and word not in stop_list:
            result.append(nw)
    return result

#这个函数的主要作用是读取每篇文章的内容
def make_line(f,stop_list):
    doc_num = "-1"
    line = f.readline()
    if line.startswith("<DOCNO>"):
        doc_num = line.split()[1]
    else:
        print "something error"
        sys.exit(1)

    line = f.readline()
    if line.startswith("<TEXT>"):
        pass
    else:
        print "something error"
        sys.exit(1)

    sentence = f.readline()
    sl = stem_line(sentence,stop_list)
    #print sl
    #print "%s"%(sentence)    

    f.readline()
    f.readline()

    return doc_num,sl

#这个函数的主要作用是数每个文章中的词频
def count_words(word_list,wd):
    result = {}
    for word in word_list:
        if word in wd:
            indx = wd[word]
            result.setdefault(indx,0)
            result[indx] += 1
    return result


#这个函数的作用是用df滤一遍词表(这个我写错了，实际上是按照tf滤的)
def filter_df(docs,min_df):
    word_dict = {}
    for doc in docs:
        for word in doc:
            word_dict.setdefault(word,0)
            word_dict[word] += 1
    #这个是新的词表-每个词对应这个数
    nwd = {}
    for word in word_dict:
        count = word_dict[word]
        if count <= min_df:
            pass
        else:
            nwd[word] = count
    return nwd
    
#这是预处理的主函数
def transform_blei_format(conf):

    #=======读取停顿词表===========
    print "读取停顿词表"
    stop_dir = conf["stop_dir"]
    sf = open(stop_dir)
    stop_list = []
    for line in sf.readlines():
        word = line.split()[0]
        if len(word)>0:
            stop_list.append(word)
    stop_list = set(stop_list)

    #=======返回每一篇经过stem后的文章（文章存在了list里）========
    corpus_dir = conf["corpus_dir"]
    corpus = []
    f = open(corpus_dir)
    print "读文件，stem每个词"
    documents = []
    a = 0
    line = "-1"
    while line!="":
        line = f.readline()
        if line.startswith("<DOC>"):
            doc_num,sl = make_line(f,stop_list)
            documents.append(sl)
        a += 1
        if a % 100 == 0:
            pass

    #========通过df进行第一遍过滤===================
    min_df = int(conf["min_df"])
    word_dict = filter_df(documents,min_df)
    
    #========给词表建立索引=================
    print "转化词索引，将词表写入文件"
    wd = {}
    words = sorted(set(word_dict.keys()))
    words_dir = conf["words_dir"]
    f1 = open(words_dir,"w")
    a = 0
    for word in words:
        f1.write("%s:%s\n"%(word,a))
        a += 1
        wd[word] = a

    #存起来
    blei_dir = conf["blei_dir"]    
    f2 = open(blei_dir,"w")

    print "将文档转化成blei的形式存起来"
    for word_list in documents:
        result = count_words(word_list,wd)
        for word in result:
            count = result[word]
            f2.write("%s:%s "%(word,count))
        f2.write("\n")

    print "统计结果："
    print "文档数：%s"%(len(documents))
    print "词表数：%s"%(len(wd))

    
    
if __name__ == '__main__':
    print "hello"
    conf = config("lda.conf")
    transform_blei_format(conf)
    
