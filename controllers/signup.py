import numpy as np
import pandas as pd

from controllers import _Controller
from utils import answer_question


class FrequentlyAskedQuestionController(_Controller):
    def _post(self):
        df = pd.read_csv('./files_for_model_training/embeddings.csv', index_col=0)
        df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
        return {"answer": answer_question(df, question=self.request.json['question'])}
