import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import AutoModel, BertTokenizerFast

#Class mapping
info = {0:'Severity level 1', 
        1:'Severity level 2', 
        2:'Severity level 3',
        3:'Severity level 4',
        4:'Severity level 5'}

class BERT_Arch(nn.Module):
    def __init__(self, bert):  
        super(BERT_Arch, self).__init__()
        self.bert = bert 
        self.dropout = nn.Dropout(0.1)
        self.relu =  nn.ReLU()
        self.fc1 = nn.Linear(768,512)
        self.fc2 = nn.Linear(512,5)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
        _, cls_hs = self.bert(sent_id, attention_mask=mask)
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

class bertInference:
    def __init__(self, model_file_path='saved_weights_5Class.bin', max_seq_len=100):
        self.tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        bert = AutoModel.from_pretrained('bert-base-uncased')
        for param in bert.parameters():
            param.requires_grad = False
        model = BERT_Arch(bert)
        self.model = model.to(self.device)
        model.load_state_dict(torch.load(model_file_path, map_location=torch.device(self.device)))
        self.max_seq_len = max_seq_len
        
    def __call__(self, text):
        tokens_test = self.tokenizer.batch_encode_plus(
            [text],
            max_length = self.max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )

        test_seq = torch.tensor(tokens_test['input_ids'])
        test_mask = torch.tensor(tokens_test['attention_mask'])
        with torch.no_grad():
            preds = self.model(test_seq, test_mask)
            preds = preds.detach().cpu().numpy()

        preds = np.argmax(preds, axis = 1)
        print("Class for document --->", info[preds[0]])
        return info[preds[0]]


if __name__ == "__main__":
    text = "National Cyber Security Awareness Month (NCSAM) is a government and private sector partnership that raises awareness about cybersecurity and stresses the collective effort required to stop cyber crimes, online thefts, and scams . The FBI and partner agencies remind you to do your part and #BeCyberSmart all year long ."
    bt = bertInference()
    bt(text)