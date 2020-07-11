from word2vec.trainer import Word2VecTrainer

if __name__ == '__main__':
    from word2vec.trainer  import Word2VecTrainer
    w2v = Word2VecTrainer(input_file="input.txt", output_file="out.vec",
                          side_num=0, neg_num=2, sentences_count=10, emb_size=[1375017],
                          batch_size=1, emb_dimension=100, iterations=3,
                          initial_lr=0.001)
    w2v.train()


