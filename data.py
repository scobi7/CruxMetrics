import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

class CruxDataset(Dataset):
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = torch.tensor(self.data.iloc[idx].values)#, dtype=torch.float)
        return sample
    
dataset = CruxDataset('routes.csv')

dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
