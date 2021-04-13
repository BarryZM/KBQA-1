from transformers import BertTokenizer
import tensorflow as tf
from tensorflow.keras import Model
from transformers import TFBertModel
import numpy
import os
# from FAQ.faq_match import FAQ_BASE_DIR

FAQ_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vocab_file = os.path.join(FAQ_BASE_DIR, 'bert_ch/vocab.txt')
bert_model = os.path.join(FAQ_BASE_DIR, 'bert_ch')

class BertVector():
    def __init__(self):
        self.tokenizer = BertTokenizer(vocab_file)
        self.model = SentenceVector()

    def encode(self, sentence, max_sentence_len):
        bert_input = self.tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=max_sentence_len,
            padding='max_length',
            # return_attention_mask=True
        )
        input_ids = tf.convert_to_tensor([bert_input['input_ids']])
        token_type_ids = tf.convert_to_tensor([bert_input['token_type_ids']])
        attention_mask = tf.convert_to_tensor([bert_input['attention_mask']])
        outputs = self.model(input_ids,token_type_ids,attention_mask)

        return outputs.numpy()


class SentenceVector(Model):
    def __init__(self):
        super(SentenceVector, self).__init__()
        self.Bert_Model = TFBertModel.from_pretrained(bert_model)

    def call(self, input_ids, token_type_ids, attention_mask):
        outputs = self.Bert_Model([input_ids, token_type_ids, attention_mask])
        # sentence_vector = outputs[0][-2][0][0]
        # for each_vector in outputs[0][-2][0]:
        #     sentence_vector = sentence1_vector + each_vector

        sentence_vector = outputs[0][0][0]
        return sentence_vector



if __name__ == '__main__':
    bv = BertVector()
    message = '今天天气怎么样'
    message_vec = bv.encode(message, 16)
    print(message_vec)

