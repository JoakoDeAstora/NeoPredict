import torch
import torch.nn as nn

class HybridPredictor(nn.Module):
    def __init__(self, numeric_input_size=5, text_embedding_size=768, hidden_lstm=64, hidden_dense=32):
        super(HybridPredictor, self).__init__()
        
        # Branch A: LSTM for Numerical Data (Price, Volatility, etc.)
        # Input shape: (Batch, Sequence_Length, Features)
        self.lstm = nn.LSTM(
            input_size=numeric_input_size,
            hidden_size=hidden_lstm,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )
        
        # Branch B: Text Processed externally -> Embedding Input
        # We assume the text embedding comes pre-computed from the Transformer service
        self.text_fc = nn.Linear(text_embedding_size, hidden_dense)
        self.text_relu = nn.ReLU()
        
        # Fusion Layer
        fusion_input_size = hidden_lstm + hidden_dense
        self.fusion_fc1 = nn.Linear(fusion_input_size, 64)
        self.fusion_drop = nn.Dropout(0.3)
        self.fusion_relu = nn.ReLU()
        
        # Output Layer (3 classes: Bearish, Neutral, Bullish)
        self.output_fc = nn.Linear(64, 3)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, numeric_seq, text_embedding):
        """
        numeric_seq: Tensor (Batch, Seq_Len, 5) -> [Close, Volume, Volatility, High, Low]
        text_embedding: Tensor (Batch, 768) -> BERT CLS token
        """
        # LSTM Pass
        # We only care about the final hidden state of the sequence for prediction
        lstm_out, (h_n, c_n) = self.lstm(numeric_seq)
        # h_n[-1] is the hidden state of the last layer
        lstm_feature = h_n[-1] 
        
        # Text Pass
        text_feature = self.text_relu(self.text_fc(text_embedding))
        
        # Fusion
        combined = torch.cat((lstm_feature, text_feature), dim=1)
        x = self.fusion_relu(self.fusion_fc1(combined))
        x = self.fusion_drop(x)
        
        # Output
        logits = self.output_fc(x)
        probs = self.softmax(logits)
        
        return probs
