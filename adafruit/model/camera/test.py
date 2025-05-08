
import numpy as np
from sklearn.utils import shuffle

# Example data: train_samples and train_labels
train_samples = np.array([1, 2, 3, 4, 5])  # These represent your sample inputs
train_labels = np.array([10, 20, 30, 40, 50])  # These represent the corresponding labels

# Shuffle while maintaining alignment
train_samples, train_labels = shuffle(train_samples, train_labels)

print("Shuffled train_samples:", train_samples)
print("Shuffled train_labels:", train_labels)


# normalize function
scaler = MinMaxScaler(feature_range=(0, 1))
scaler_train_samples = scaler.fit_transform(train_samples.reshape(-1, 1))