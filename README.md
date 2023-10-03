# Music Recommendation Using Spotify Million Playlist Dataset

[Slides](https://docs.google.com/presentation/d/1ecWfFkn9KhqBlpo_bE-1zvL_RSZFfAWjZK_HFz3N0BU/edit?usp=sharing), [Report](https://docs.google.com/document/d/1o7_80qezwflZwY2l8-gyAfHA2kHTRYfPu1GkQgcSPeo/edit?usp=sharing)

Enjoy exploring among about 2 million songs...

## Overview

### The architecture diagram of our system
<img width="836" alt="image" src="https://user-images.githubusercontent.com/23244168/232262185-f297f8d0-004b-44f3-b73d-440c95619634.png">


Our project focuses on developing a Music Recommendation System using the Spotify Million Playlist Dataset. We processed approximately two million unique songs to create feature vectors for each of them. Users can search for songs by track name and artist name, select their preferred songs from the list, and receive relevant recommendations from the system.

### Preprocessing stages
<img width="951" alt="image" src="https://user-images.githubusercontent.com/23244168/232262227-11a4b50b-039d-48f7-a3e8-5e3deea7c710.png">

Data preprocessing included cleaning 32GB of raw data and performing sentiment analysis on Dataproc. Feature vectors were obtained from the Spotify API for 1,998,516 unique songs. Features were joined and saved in MongoDB for further processing.

### Recommendation Method

To find similar songs, we calculated the cosine similarity between the mean feature vector of selected songs by the user and all feature vectors in our database. Each feature vector comprises 27 features, including danceability, energy, loudness, speechiness, and more. 

### Components Used

- Flask: Framework for developing the REST-Server.
- HTML, CSS, and JS: Used for the frontend UI.
- Pyspark: Utilized for preprocessing the Spotify Million Playlist Dataset.
- APIs: Spotify API for extracting features and cover art images.
- Redis: for message queuing.
- MongoDB: Storage for extracted features.
- Google Storage Bucket: Used to store raw data.
- Docker and Kubernetes: Deployment of the application.
