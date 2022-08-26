from happytransformer import TTTrainArgs, HappyTextToText

happy_tt = HappyTextToText("google/mt5-base", "JorgeSarry/est5base")
args = TTTrainArgs(batch_size=1, num_train_epochs=5,)

happy_tt.train("./data/train_aug.csv", args=args)

happy_tt.save("./model/")