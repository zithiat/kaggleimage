FROM kaggle/python
EXPOSE 8888
EXPOSE 5000

WORKDIR /notebook

RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
RUN mkdir /notebook/log
RUN mkdir /notebook/input
RUN mkdir /notebook/flask_app

COPY ./app.py /notebook/flask_app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./supervisord.conf /etc

RUN pip install --upgrade pip
RUN pip install flask flask_cors jsonify numpy pandas
RUN pip install kaggle

# Setup Kaggle credentials
RUN mkdir ~/.kaggle
RUN echo "{\"username\":\"zithiat\",\"key\":\"3f02afd82b108665dcc82587d1d3a880\"}" > ~/.kaggle/kaggle.json
RUN chmod 600 ~/.kaggle/kaggle.json
RUN export KAGGLE_USERNAME=zithiat
RUN export KAGGLE_KEY=3f02afd82b108665dcc82587d1d3a880

# Download datasets and notebook from Kaggle
RUN mkdir /notebook/input/movielens-100k-dataset
RUN kaggle datasets download -d prajitdatta/movielens-100k-dataset
RUN unzip movielens-100k-dataset.zip -d /notebook/input/movielens-100k-dataset
RUN rm movielens-100k-dataset.zip

RUN mkdir /notebook/input/the-movies-dataset
RUN kaggle datasets download -d rounakbanik/the-movies-dataset
RUN unzip the-movies-dataset.zip -d /notebook/input/the-movies-dataset
RUN rm the-movies-dataset.zip

RUN mkdir /notebook/input/tmdb-movie-metadata
RUN kaggle datasets download -d tmdb/tmdb-movie-metadata
RUN unzip tmdb-movie-metadata.zip -d /notebook/input/tmdb-movie-metadata
RUN rm tmdb-movie-metadata.zip

RUN mkdir /notebook/movie_recommendation
#RUN kaggle kernels pull melkhouly/movie-recom
#RUN mv movie-recom.ipynb /notebook/movie_recommendation
COPY ./movie-recom.ipynb /notebook/movie_recommendation

ENTRYPOINT /usr/bin/supervisord
CMD ["/usr/bin/supervisord"]



