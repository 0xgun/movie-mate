# Movie Review Sentiment Analysis: A Comparative Study of Different Algorithms
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)

## Introduction
Sentiment analysis is a natural language processing technique used to determine whether data is positive, negative or neutral. Sentiment analysis is often performed on textual data to help businesses monitor brand and product sentiment in customer feedback, and understand customer needs.

## Problem Statement
The main objective of this project is to perform sentiment analysis on movie reviews and classify them as positive or negative. The dataset used for this project is the [IMDB Movie Reviews Dataset](https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) from Kaggle. The dataset contains 50,000 movie reviews from IMDB. The dataset is divided into 25,000 training samples and 25,000 testing samples. The training and testing samples are balanced, meaning that there are equal number of positive and negative reviews in both the training and testing samples. The dataset is already preprocessed and each review is encoded as a sequence of indexes corresponding to the words in the review. The words are indexed by their frequency in the dataset, meaning that for instance the integer "3" encodes the 3rd most frequent word in the data. This allows for quick filtering operations such as: "only consider the top 10,000 most common words, but eliminate the top 20 most common words".

## Dataset

### Data Description

The dataset contains 50,000 movie reviews from IMDB. The dataset is divided into 25,000 training samples and 25,000 testing samples. The training and testing samples are balanced, meaning that there are equal number of positive and negative reviews in both the training and testing samples. The dataset is already preprocessed and each review is encoded as a sequence of indexes corresponding to the words in the review. The words are indexed by their frequency in the dataset, meaning that for instance the integer "3" encodes the 3rd most frequent word in the data. This allows for quick filtering operations such as: "only consider the top 10,000 most common words, but eliminate the top 20 most common words".

### Data Dictionary

| Column Name | Description |
| --- | --- |
| review | Textual review of the movie |
| sentiment | Sentiment of the review (0 = negative, 1 = positive) |


### Screen Shots

![Screenshot (1)](https://github.com/0xgun/movie-mate/blob/master/screenshots/UI_1.jpeg)

![Screenshot (2)](https://github.com/0xgun/movie-mate/blob/master/screenshots/UI_2.jpeg )

![Screenshot (3)](https://github.com/0xgun/movie-mate/blob/master/screenshots/UI_3.jpeg )

![Screenshot (4)](https://github.com/0xgun/movie-mate/blob/master/screenshots/UI_4.jpeg )

![Screenshot (5)](
    https://github.com/0xgun/movie-mate/blob/master/screenshots/UI_5.jpeg )