# Spotify Music Recommender

[Slides](https://docs.google.com/presentation/d/1ecWfFkn9KhqBlpo_bE-1zvL_RSZFfAWjZK_HFz3N0BU/edit?usp=sharing), [Report](https://docs.google.com/document/d/1o7_80qezwflZwY2l8-gyAfHA2kHTRYfPu1GkQgcSPeo/edit?usp=sharing)

## Overview

### The architecture diagram of our system
<img width="836" alt="image" src="https://user-images.githubusercontent.com/23244168/232262185-f297f8d0-004b-44f3-b73d-440c95619634.png">


The goal of a recommendation system is to recommend or predict items a user might like based on their data or based on the entire user database. A general recommendation system pipeline includes steps such as Data Extraction, Data Preprocessing, Recommendation algorithm, and Output Recommendations. In this project we developed a Music Recommendation System Using the famous Spotify Million Playlist Dataset. We pre-processed about two million unique songs and find a feature vector for each of them. The user searches for songs by track name and artist name. Then, the user selects their desired songs from the list based on which the system returns relevant recommendations. 

### Preprocessing stages
<img width="951" alt="image" src="https://user-images.githubusercontent.com/23244168/232262227-11a4b50b-039d-48f7-a3e8-5e3deea7c710.png">
