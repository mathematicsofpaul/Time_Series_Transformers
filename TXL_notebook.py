# %%
import os
import numpy as np
import pandas as pd
import torch

import pytorch_lightning as pl
from pytorch_lightning.loggers import TestTubeLogger

from TXL_model import TransformerXL_Trainer, GlobalState

# %% Load input
data_set_name = "etf"
data_set = pd.read_pickle(f"data/{data_set_name}/allData.pickle")

# Fill NA's with 0.0 and convert to tensor (although probably not necessary)
data_set = data_set.fillna(0.0).values[:, 1:].astype(np.float64)
data_set = torch.tensor(data_set)

# %%
global_state = GlobalState(data=data_set, debug=False)
global_state.num_workers = 4
global_state.dataset_size = 1_500
global_state.n_layer = 3
global_state.n_head = 4
global_state.d_head = 8
global_state.n_model = 20
global_state.d_pos_enc = 20
global_state.d_FF_inner = 50
global_state.n_val=8
global_state.n_test=16
global_state.n_batch=32
global_state.dropout=0.2
global_state.dropout_attn=0.2
global_state.n_predict=8
global_state.n_mems=16



# %%
# Create a new transformer_model to be trained
transformerxl_model = TransformerXL_Trainer(global_state)

# %%
# Logging backend
TB_logger = TestTubeLogger(
    save_dir=os.path.join(os.getcwd(), global_state.work_dir, data_set_name),
    name='transformerxl_trainer_logs'
)

# %%
# Actual Trainer() method
# Avoids preliminary runs of validation before training
transformerxl_trainer = pl.Trainer(logger=TB_logger, num_sanity_val_steps=0)

# %%
pl.seed_everything(global_state.seed)
transformerxl_trainer.fit(transformerxl_model)
