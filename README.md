# BERT Serving
BERT:(如果要現場train model才要開，只是demo應該不用)
pip install bert-serving-server
pip install bert-serving-client
下載bert的中文模型：(https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)
解壓縮至相同路徑底下

# LINE Serving
LINE-BOT:
pip install line-bot-sdk

# 啟動服務
$ bert-serving-start -model_dir 你的中文模型路徑 -num_worker=1

# server
暫時先用ngrok.  please open ngrok.exe
