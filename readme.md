# P!XAR

###### The project aims at enhancing the quality of low light images and reduce noise in those images.

## Getting started

### 1. Install Dependenciesconda 

`conda create --name <env_name> --file requirements.txt`


### 2. Start development server

`python server.py`


### 3. Head over to localhost:5000 to see the app in action.

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