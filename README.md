# VISAT DATA PIPELINE - A VISUALIZATION OF SATELLITE DETECTED OBJECTS PROGRAM
A python project that reads and writes satellite data, as well as read and process labels

## Usage
If you want to process data locally, try the following command

```bash
labellize.py <IMAGE-ID> <SAT-IMAGES-FOLDER> <JSON-FILE-LABELS>
```

## Build and run the project on Docker 
Inside the project folder, run the following docker command to build an image of the project:

```bash
docker image build -t labellize .
```
To be able to visualize the labels from the container, you need to have [XQuartz](https://www.xquartz.org/) installed on your machine.

Once running you open XQuartz terminal and run:

```bash
xhost +
```
Next open a new terminal session and set a variable environment called $IP to serve the connection between the container and the x11 GUI. Use the following command:

```bash
export IP=$(/usr/sbin/ipconfig getifaddr en0)
echo $IP
```
Now Execute the docker run command, which also mount the folder where the levels and images exists to the home folder of the container:

```bash
docker run -it -e DISPLAY="${IP}:0" -v /tmp/.X11-unix:/tmp/.X11-unix -v <DATA-FOLDER>:/home labellize <IMAGE-ID> <SAT-IMAGES-FOLDER> <JSON-FILE-LABELS>
```

## License
[MIT](https://choosealicense.com/licenses/mit/)