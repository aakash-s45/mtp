FROM python:3.9.16-bullseye

WORKDIR /mtp/code

COPY . .

RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev python3-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip install "setuptools<58.0"
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}') --global-option=build_ext --global-option="-I/usr/include/gdal"
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0"]