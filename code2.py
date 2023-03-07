from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

df = pd.read_csv("C:/Users/Baptiste/Documents/Prepa/1.MPI/TIPE/Donnéees_synopopendata_2018-2020/donnees-synop-essentielles-omm.csv")

# Select the features (weather variables) and labels (whether it rained)
X = df[["temperature", "humidity", "wind_speed", "pressure"]]
y = df["rain"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a decision tree model on the training data
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate the model's performance on the testing data
accuracy = model.score(X_test, y_test)
print("Accuracy: {:.2f}".format(accuracy))

# Use the trained model to make rain predictions
predictions = model.predict(X_test)
