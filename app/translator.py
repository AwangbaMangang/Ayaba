import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import Config

class MeeteiTranslator:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MeeteiTranslator, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "facebook/nllb-200-distilled-600M"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
    
    def translate(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        outputs = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.lang_code_to_id["mni"],
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Singleton instance
translator = MeeteiTranslator()
