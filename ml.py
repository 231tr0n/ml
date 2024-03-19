import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

"""
1,13.83,1.65,2.6,17.2,94,2.45,2.99,.22,2.29,5.6,1.24,3.37,1265
2,12.42,4.43,2.73,26.5,102,2.2,2.13,.43,1.71,2.08,.92,3.12,365
3,12.86,1.35,2.32,18,122,1.51,1.25,.21,.94,4.1,.76,1.29,630
"""
(X, Y) = load_wine(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.20, random_state=4
)

mse = {}

model = LinearRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
mse["lr"] = mean_squared_error(y_test, y_pred)

model = DecisionTreeClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
mse["dt"] = mean_squared_error(y_test, y_pred)

model = KNeighborsClassifier()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
mse["knn"] = mean_squared_error(y_test, y_pred)

model = SVC(max_iter=1000)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
mse["svc"] = mean_squared_error(y_test, y_pred)

plt.bar(list(mse.keys()), list(mse.values()), color="green")
plt.show()
