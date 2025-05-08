import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier

def main():
    # Load the model
    with open('decision_tree_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    # Example input: Four feature values (e.g., [Light, Temperature, Humidity, Soil Moisture])
    test_input = np.array([[15000, 0, 60, 30]])  # Replace with actual values

    # Predict the label using the model
    prediction = loaded_model.predict(test_input)

    # Output the prediction result
    print("Prediction:", prediction)  # Output will be 'Normal' or 'Not Normal'
    # print("pre type:", type(prediction))

    print("Prediction:", prediction[0])  # Output will be 'Normal' or 'Not Normal'
    # print("pre type:", type(prediction[0]))
    # for x in prediction:
    #     print("pre: ", x)  # Output will be 'Normal' or 'Not Normal'

if __name__ == "__main__":
    main()