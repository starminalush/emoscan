import matplotlib.pyplot as plt
import streamlit

x = [
    "2023-04-05",
    "2023-04-06",
    "2023-04-07",
    "2023-04-08",
    "2023-04-09",
    "2023-04-10",
    "2023-04-11",
    "2023-04-12",
    "2023-04-13",
    "2023-04-14",
]
y1 = [1, 2, 1, 3, 4, 9, 7, 5, 1, 3]
y2 = [5, 1, 3, 4, 1, 5, 4, 6, 2, 7]
y3 = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
plt.plot(x, y1, label="счастливое")
plt.plot(x, y2, label="негативное")
plt.plot(x, y3, label="нейтральное")
plt.legend()
plt.ylabel("Количество учеников")
plt.xlabel("Даты")
plt.xticks(rotation=45)
plt.show()
streamlit.pyplot(plt)
