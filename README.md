# kopo - Data Mining Project
This is a data mining project from the University of Illinois Urbana-Champaign from Coursera using [Yelp Dataset]() 

<img width="960" alt="yelp" src="https://github.com/user-attachments/assets/c66c331d-6120-4f66-abe5-92e6d39a29a2">


## Overview
The goal of the Data Mining Project is to provide us with an opportunity to synthesize the knowledge and skills we’ve learned from the courses and apply them to solve real-world data mining challenges. We will be given a restaurant review data set from Yelp and mine this dataset to discover interesting and useful knowledge to help people make dining decisions, including constructing a cuisine map to help people understand the landscape of different cuisines, mining popular dishes of a given cuisine, recommending (i.e., ranking) restaurants for a given dish, and predicting hygiene of a restaurant.

**Dataset**  
Name: Yelp Dataset  
Contents: Restaurant Review  
  - Business info
  - Review
  - Check-in
  - Tip
  - User
Size: 1.2 GB (40K++ business)

## 1.Topic Extraction 
### 1.1 Popular Topics
Here, we're choosing the LDA model since we have a large dataset in JSON file format which is known for its ability to handle large datasets and produce high-quality topics. LDA is generally considered a more robust and flexible model than PLSA due to its use of Dirichlet priors, which help manage uncertainty and improve topic coherence. 

From all the restaurant's data, we chose 10 samples of topics as shown by the radial dendrogram below. This is the visualization of what people have discussed in restaurant reviews on 10 topics using library D3 from JavaScript.

<img width="489" alt="image" src="https://github.com/user-attachments/assets/88c113f0-11d3-4bb7-9415-936ccb061088">  

Here's the visualization of the topic clusters. The visualization provides a clear overview of how often each topic appears in the dataset and their relative importance. This can help identify key themes and topics of interest within the text data, guiding further analysis or action based on the prominence of each topic.  

![task1 1-topic clusters](https://github.com/user-attachments/assets/8ed19c46-3440-4c91-849f-2e4f63e0dae3)
<br>

### 1.2 Comparing Some Restaurants  
Then, let's take a look at the sample restaurant we have. We chose 3 restaurants for Mexican food to see how the reviews were. They are Filiberto's Mexican Food, Elvira's Mexican Food, and Carolina's Mexican Food. The dendrogram shows the topics that are most frequently reviewed by the customers from each rating, 1 to 5 using the LDA model after preprocessing the data.  
<br>
<img width="410" alt="task1 2-3samplerestaurants" src="https://github.com/user-attachments/assets/a90b458a-5638-4d9a-bd48-f35a94951833">

<br>

## 2. Cuisine Exploration  
In this step, we will work on mining this data set to discover knowledge about cuisines. In the Yelp data set, businesses are tagged with categories. For example, the category "restaurant" identifies all the restaurants. Specific restaurants are also tagged with cuisines (e.g., "Indian" or "Italian"). This provides an opportunity to aggregate all the information about a particular cuisine and obtain an enriched representation of a cuisine using, for example, review text for all the restaurants of a particular cuisine. Such a representation can then be exploited to assess the similarity between two cuisines, which further enables the clustering of cuisines.  

The goal of this task is to mine the data set to construct a cuisine map to visually understand the landscape of different types of cuisines and their similarities. The cuisine map can help users understand what cuisines are available and their relations, which allows for the discovery of new cuisines, thus facilitating an exploration of unfamiliar cuisines.  

### 2.1 Visualization of Cuisine Map
From 715 categories/cuisines, we selected 20 cuisines to be compared.  
1. We extract all the businesses according to the selected cuisines.
2. Collect all the reviews corresponding to each cuisine.
3. We store all the reviews from all the restaurants for each cuisine.
4. Preprocessing the text like lowercase, removing punctuation, etc.
5. Vectorize the preprocessed text for each category using TF-IDF.
6. Calculate the similarities and visualize them using the heatmap.

![Screenshot 2024-10-01 192828](https://github.com/user-attachments/assets/b6c68730-c979-4737-9160-44cc7ac46025)

**Key Insight**:
1. Highly Similar Categories:
Categories like Pizza, Mexican, and Italian show high similarity, which makes sense since they may share common ingredients or food types. Sushi Bars and Japanese are also highly similar, as expected. From these samples, we know that the original cuisines from its countries have high similarities to the country restaurants. For example, sushi and Japanese, where sushi is originally from Japan and Japanese restaurants may have sushi menus.

2. Dissimilar Categories:
Categories like Ramen and Australian or Cupcakes and Ramen show much lower similarity, indicating that the types of food and reviews are very different.

3. Clustered Relationships:
Categories that are typically similar in cuisine style (like Sushi Bars and Japanese, or Ice Cream & Frozen Yogurt and Desserts) have high cosine similarity, suggesting common features in their reviews.

### 2.2 Analyze the Similarities Between Cuisines  
We're using LDA (Latent Dirichlet Allocation) model to explore the categories that show high similarity based on the cosine similarity matrix. This approach will help us uncover why certain categories are similar by identifying common topics or themes in their reviews.  
Here are the samples of similar categories and the topic based on their reviews. 

| Japanese-Sushi                          | Italian-Pizza                           |
| ----------------------------------- | ----------------------------------- |
| ![Screenshot 2024-10-02 212257](https://github.com/user-attachments/assets/1cd53172-1577-40cd-a1e5-ed7994e537b3) |![Screenshot 2024-10-02 212147](https://github.com/user-attachments/assets/900180e6-6333-410f-9ab5-2de7643bda57)  

From the samples above, now we know what common topics in the categories make them similar, such as the main menu, reviews, or the restaurants' services.

## 3. Mining Dishes in Specific Cuisine  
The goal of this task is to mine the data set to discover the common/popular dishes of a particular cuisine. Typically when we go to try a new cuisine, we don’t know beforehand the types of dishes that are available for that cuisine. For this task, we would like to identify the dishes that are available for a cuisine by building a dish recognizer. In this case, we chose American (New) cuisine.  

### 3.1 Manual Tagging 
We have an American (New) dish, which is frequent (at least 10 times in the corresponding corpus), automatically generated by the auto-labeling process of SegPhrase.  Some of the dish names are verified by an outside knowledge base such that they are all good phrases, and some of them might be good dish names. However, some of the labels might be wrong. Therefore, we have to refine the label list for one cuisine using manual tagging. An example of this step is removing a false positive non-dish name phrase (recommended), e.g., Hong Kong 1 could be removed in Chinese cuisine. Change a false positive non-dish name phrase to a negative label, e.g., Hong Kong 1 could be modified as Hong Kong 0.  

### 3.2  
Once we have a list of dish names, it is likely that many dish names are still missing. In this step, we would expand the list of dishes by using other pattern-mining techniques like TopMine or SegPhrase and/or word association methods. In this case, we'll use a state-of-the-art method, Word2Vec. 

- Preprocessing the data like handling multi-word phrases, removing punctuation, tokenizing, etc.
- Checking if samples of dishes are present in our raw data and our corpus to ensure that the data has been preprocessed well.
- Training the Word2Vec model using the total corpus.   
- Word2Vec captures semantic relationships between words based on their context within a large corpus of text. This means that words with similar meanings are mapped to nearby points in the vector space. Since we have a 1,527,498 corpus size from review and tip datasets, Word2Vec is the right approach.
- We got the expanded list of dish   

## 4. Ranking of the Dishes  
In this task, we will create a visualization showing a ranking of the dishes for a Yelp cuisine of our choice. In the task 3, we chose to work on American cuisine, so we will deep dive into this cuisine.  

###  Step 1: Frequency Count to Select Top 50 Dishes  
Count mentions for each dish in the American cuisine reviews and select the top 100 dishes.

### Step 2: Weighted Frequency by Rating  
Rank the dishes only using the frequency count seems not relatively correct because it can caused by many factors, maybe positive review pr negative reviews. So, we will calculate an average weighted frequency for each dish, multiplying each mention by the rating (e.g. 1 star: 100x1=100, 2 stars: 60x2=120, etc).

### Step 3: Visualize Rating Distribution for Each Dish  
Then, we visualized the top 50 dishes based on the frequency count and the average rating (1 of 5) and then selected the top 20 to see the star distribution (from 1 to 5) like the images below.
<br>
![top50dish_average rating](https://github.com/user-attachments/assets/ab758f7f-14be-4689-8607-1b6a2c81a6a7)
<br>
Based on the visualization of the top 50 dishes for American (New) cuisine by mention count and average star rating, here are some key insights:  

**1. Most Popular Dishes by Mention Count**:  
Rice, Cheese, and Chicken are the top three most mentioned dishes, indicating that these items are highly popular and frequently reviewed within this cuisine. Other dishes like Burger, Appy, and Bread also have high mention counts, suggesting they are staple items in American (New) cuisine.  

**2. Average Star Ratings Across Dishes**:  
Fanta and Scallops received the highest average star ratings, with 4.32 and 4.12 respectively. These items may be associated with positive experiences among reviewers, as they stand out for their higher ratings.  

**3. Distribution of Mention Count vs. Average Rating**:  
High mention counts do not necessarily correlate with high ratings. For example, Rice has one of the highest mention counts but a moderate average rating of 3.60. Conversely, Scallops has a high average rating but a lower mention count, suggesting it may be highly regarded by a smaller group of reviewers.

**4. Variety in Popular Dishes**:
The list includes a mix of both entrees (e.g., Steak, Burger) and side dishes/snacks (e.g., Fries, Cheese). This suggests that American (New) cuisine reviews cover a broad range of meal types, indicating varied consumer interests. Dessert items like Chocolate, Cheesecake, and Ice Cream appear frequently, suggesting a strong preference for sweet dishes in American dining experiences.
<br>
![top20_dish_ranking_visualization](https://github.com/user-attachments/assets/c690a709-6a03-4bef-ae84-eb0d4100704c)


Here are some key insights based on the rating distribution by stars for the top 20 dishes in American (New) cuisine:

**1. Diverse Rating Distribution Across Popular Dishes**:  
Most dishes have a significant portion of 4 and 5-star ratings, showing overall customer satisfaction. For instance, Rice has 24.8% 5-star ratings and 35.0% 4-star ratings, making it a well-liked dish despite lower ratings in other categories. Dishes like Fanta and Cake have higher percentages of 5-star ratings (52.0% and 34.5% respectively), indicating that these items receive a higher level of customer appreciation relative to other dishes.  

**2. High Variability in Customer Preferences**:  
Some dishes, such as Gin and Tart, exhibit a more balanced rating distribution across all star categories. This suggests a varied response, potentially reflecting differences in taste preferences or quality consistency.   

**3. Strength in Dessert and Snack Items**:
Dessert items like Cake, Appetizer, and Fries generally receive more favorable ratings, with a good proportion of 4 and 5-star ratings. This might indicate a preference for sweet and snack items in American (New) cuisine. Fanta stands out with a substantial 52.0% in the 5-star category, suggesting a strong positive response for this beverage item.

### Step 4: Sentiment Analysis on Dish Mentions  
Analyze sentiment for sentences mentioning each dish and add sentiment scores to our ranking. We used VADER (Valence Aware Dictionary and Sentiment Reasoner). VADER is a popular tool for sentiment analysis, especially well-suited for social media text, reviews, and other types of informal language.  
<br>
<img width="159" alt="image" src="https://github.com/user-attachments/assets/a0579199-5d3f-4be8-a162-4f6134ddabca">  
<br>
Based on the sentiment analysis score, we can conclude that there is generally an alignment between the average star ratings and sentiment analysis scores for the dishes.

## 5. Restaurants Recommendation  
In this task, our goal is to recommend good restaurants to those who would like to try one or more dishes in a cuisine. In this case, we will work on American (New) Cuisine for Burger and Chicken.

Given a particular dish, the general idea of solving this problem is to assess whether a restaurant is good for this dish based on the reviews of a candidate restaurant. Something to consider is to make our visualization general enough that it could be used in a search engine or system and generate something useful for users by recommending popular restaurants based on different dishes.  

### 5.1. Top Restaurants in American (New) Cuisine  
<br>
<img width="528" alt="Top 10 Restaurants in American Cuisine" src="https://github.com/user-attachments/assets/605c1fa0-8d01-4dc2-9034-8a8f1d987243">  

The restaurants are recommended based on ratings and reviews. If we give the recommendation based on the highest reviews, many restaurants have an average rating of less than 4. So, the high ratings may help people to try new restaurants in American cuisine.  

### 5.2. Top Restaurants for Burger  
For restaurant recommendations for burgers, we tried to give 2 perspectives: based on reviews then calculating the average rating and based on high ratings then reviews.  

**Restaurants for Burger Based on Reviews**  
<br>
![top 25 burger restaurants](https://github.com/user-attachments/assets/34e2cf3d-d228-4525-a19c-5904bff33ed8)
From the chart above we found 25 restaurants with hot topics, but the rating seems low. It shows that many customers have their own opinions about the burgers.  

**Restaurants for Burger Based on Ratings**  
<br>
![Picture1](https://github.com/user-attachments/assets/1d522b34-37b3-4442-9b39-f5939ff56bee)  
These recommendations are based on the high rating first then consider the review count, making the restaurants not only have the high rating but can be recommended based on burger and total reviews.  

### 5.3. Top Restaurants for Chicken  
We also do the same for restaurants' recommendations for chicken.  

**Restaurants for Chicken Based on Reviews**  
<br>
![top 25 chicken restaurants](https://github.com/user-attachments/assets/b47ba364-73c6-4126-b88a-186d447752d9)
The same thing also happened to restaurants that have many reviews but low ratings. This may be due to the popularity of the restaurant but after trying it, many customers are dissatisfied.  

**Restaurants for Chicken Based on Ratings**  
<br>
![Picture2](https://github.com/user-attachments/assets/d674ae6a-c5b2-4db0-ae43-68972039571e)  
So, we take a recommendation based on high ratings and reviews to give recommendations for people to try. 
