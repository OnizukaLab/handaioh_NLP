from gensim.models import KeyedVectors


model = KeyedVectors.load_word2vec_format('./data/word2vec.300d.ja.txt')
def Candidate_selector(word, topn=3):
    return [word for (word, _) in model.most_similar(word, topn=topn)] if word in model.wv.vocab else None

if __name__ == '__main__':
    Candidate_selector('NASA')

