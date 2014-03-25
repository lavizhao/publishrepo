#coding: utf-8
from read_conf import config

def corpus(file_dir,name):
    f = open(file_dir)
    result = f.readlines()
    if name == "my":
        result = [i.split(":")[0] for i in result]
    else:
        result = [i.split()[0] for i in result]
    return set(result)

if __name__ == '__main__':
    conf = config("lda.conf")
    my_dir = conf["words_dir"]
    blei_dir = "/home/lavi/publishrepo/lda/ap/vocab.txt"

    my_corpus = corpus(my_dir,"my")
    blei_corpus = corpus(blei_dir,"blei")
    common = 0
    for word in my_corpus:
        if word in blei_corpus:
            common += 1
    print "my:%s"%(1.0*common/len(my_corpus))
    print "blei:%s"%(1.0*common/len(blei_corpus))
    
    
