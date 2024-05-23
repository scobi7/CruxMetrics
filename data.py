import pandas as pd
import h5py

# tonic imports
import tonic
import tonic.transforms as transforms  
from tonic import DiskCachedDataset # alt: MemoryCachedDataset leaving this here incase we wanna use a cache

# torch imports
import torch
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import random_split
import torch.nn as nn

class CruxDataset(Dataset):
    def __init__(self, h5_file):
        self.h5_file = h5_file
        with h5py.File(h5_file, 'r') as f:
            self.holds = f['holds']
            self.labels = f['labels']
            self.length = len(self.holds)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return {'holds': torch.tensor(self.holds[idx], dtype=torch.float32),
                'labels': torch.tensor(self.labels[idx], dtype=torch.long)}

def dataloader(config):
    batch_size = config['batch_size']
    dataset = CruxDataset(config['data_file'])

    train_size = int(0.8 * len(dataset)) #training to testing dataset ratio. we can always change this
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader

# Define configuration parameters
config = {
    'batch_size': 64,
    'data_file': 'data.h5',  
}

# Call the dataloader function
train_loader, test_loader = dataloader(config)

# Check the length of the loaders for more information
print(f"Number of batches in train loader: {len(train_loader)}")
print(f"Number of batches in test loader: {len(test_loader)}")


