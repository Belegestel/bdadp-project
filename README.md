# How to run the project

Try `./run.sh`. If there are any issues, `./start.sh` should be sufficient to set the environment up appropriately. After that, `./run.sh` again.

# Dataset used

https://www.kaggle.com/datasets/tawfikelmetwally/automobile-dataset

# Usage

When executing `main.py`, the user is able to choose one out of a number of prepared rankings, that are then used to construct a query and get the data from the distributed database. Moreover, the user has an option to interactively create a custom query with custom rankings.
The recommendation system is based on returning the cars from the dataset in the desired order - the car fitting the user requirements the best will be on the top of the list.
