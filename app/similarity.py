from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

# Load English model
model_name_en = 'sentence-transformers/all-MiniLM-L6-v2'
tokenizer_en = AutoTokenizer.from_pretrained(model_name_en)
model_en = AutoModel.from_pretrained(model_name_en)

# Placeholder for Kannada (extendable)
tokenizer_kn = None
model_kn = None

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def calculate_similarity(text1, text2, language='en'):
    tokenizer = tokenizer_en if language == 'en' else tokenizer_kn
    model = model_en if language == 'en' else model_kn

    if tokenizer is None or model is None:
        return None

    encoded_input = tokenizer([text1, text2], padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)

    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    embeddings = F.normalize(embeddings, p=2, dim=1)
    similarity = F.cosine_similarity(embeddings[0], embeddings[1], dim=0)
    return round(similarity.item(), 4)