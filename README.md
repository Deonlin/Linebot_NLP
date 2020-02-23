# Linebot_NLP
必須再去下載BERT SERVING
$ pip install bert-serving-server # server
$ pip install bert-serving-client # client, independent of 'bert-serving-server'
下載bert的中文模型：[[Bert-Base, Chinese]] (https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)

啟動服務
$ bert-serving-start -model_dir 你的中文模型路徑 -num_worker=1
