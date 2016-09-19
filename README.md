## Saffron's Pairing Service

This is a microservice that recommends ingredients for the app Saffron.


## Notebooks

I recommend that checking out the jupyter notebooks I've thoroughly annotated my thought process in. It shows how I use Dijkstra's algorithm to recommend ingredient pairings [here](https://github.com/alberth8/PairingService/blob/master/dijkstras.ipynb) and my approach to ranking ingredients [here](https://github.com/alberth8/PairingService/blob/master/intersection.ipynb).


## Motivation


At some point in my career as a homecook, I grew tired of cooking from recipes. I wanted to create my own recipes and experiment with new flavor profiles. The problem was that there didnt' seem to be a comprehensive resource that could answer the question of what other ingredients paired well with a given set of ingredients.

If one could imagine a database where every single table represented an ingredient, and listed in each table was every ingredient that ingredient had ever been paired with (possibly in a ranked order), then finding what paired well with a given set would simply be finding an intersection. Surely the schema design could be greatly improved, but the end result would essentially be an intersection. Not so interesting.

Thus, this microservice seeks to this problem in a more interesting way.

## Technologies


- Analysis: NumPy, SciPy, pandas
- Server: Flask
- Database: PyMongo, MongoDB 
- Deployment: DigitalOcean, Docker


## API Reference


My microserivce is on docker, so you can see the results by visiting
`http://45.55.232.155:5000`.

`/` (GET): Returns "This is a test."

`/api/path` (POST): Returns ingredient path determined by Dijkstra's algorithm.

- request body: 


        {
            "ingredients": ["ingredient_source", "ingredient_sink"]
        }
    Note: assumes ingredients provided are semantically correct and exist in the database.
    
    
- response body: a path of ingredients


        {
            "path": [
                "ingredient_source",
                ...,
                "ingredient_i",
                ...,
                "ingredient_sink"
            ]
        }

`/api/intersection` (POST): Returns a list of ranked ingredients in the intserction of the user's selected ingredients

- request body:


        {
            "ingredients": [
                'ingredient_0',
                ...,
                'ingredient_j']
        }

- response body:
    

        ['ingredient_a', 'ingredient_1', ... , 'ingredient_{n-1}', 'ingredient_b']
    
        
`/api/update` (POST): This API is used to update the database with results from Saffron's web scraper.

Currently, I've stopped my DigitalOcean droplet (cost reasons), so you won't be able to access these api endpoints.

## Installing


If instead you would like to download the code, simply do the following in the command line

    $ git clone https://github.com/alberth8/PairingService.git
    $ cd PairingService

In the root directory,

    $ export FLASK_APP=app.py
    $ flask run

At the bottom of `app.py`, delete `port='0.0.0.0'` so that it defaults to `127.0.0.1`. Then enter `127.0.0.1:5000` in your browser and you should be able to play with it.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
