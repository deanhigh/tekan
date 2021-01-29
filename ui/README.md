#User interface 

The package.json contains all the dependencies. 
`npm install`

To build and develop you need to run gulp
`gulp build`

To build the docker image 
`docker build ta/ui .`

and run it 
`docker run -v $(pwd):/usr/src/app -p 8080:8080 ta/ui`