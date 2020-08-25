# P!XAR

###### The project aims at enhancing the quality of low light images and reduce noise in those images.

## Getting started

### 0. Install anaconda and git if not already installed.

### 1. Clone this repository

`git clone https://github.com/bokaderohit98/low-light-image-enhancement.git`

### 2. Open terminal and cd into the cloned repository.

`cd low-light-image-enhancement`

### 3. Install Dependencies using anaconda

`conda create --name <env_name> --file requirements.txt`

Note: <env_name> can be anything depending upon you what you want to name your environment.

### 4. Once the environment is created switch to the environment.

`conda activate <env_name>`

Note: <env_name> is same as above

### 5. Start development server

`python server.py`


### 6. Head over to localhost:5000 to see the app in action.

###### For Client side development clone [this repository](https://github.com/bokaderohit98/pixar-ui) in current folder. i.e. in pixar. And follow the instructions give in the repository.

---
## API Reference 

### /
- Home endpoint
- returns index.html

### /path:path_name
- Endpoint to serve static files
- path_name is the path to any static file on server

### /api
- Api endpoint to Enlighten an image.
