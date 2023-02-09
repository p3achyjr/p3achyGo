'''
Hyperparameters for training.
'''


class TrainingConfig:

  def __init__(self,
               init_learning_rate=1e-2,
               batch_size=32,
               epochs=10,
               ds_shuffle_size=1000):
    self.kInitLearningRate = init_learning_rate
    self.kBatchSize = batch_size
    self.kEpochs = epochs
    self.kDatasetShuffleSize = ds_shuffle_size