FROM docker.elastic.co/elasticsearch/elasticsearch:7.4.0

RUN yum install -y unzip wget

RUN mkdir -p config/hunspell/ru_RU
RUN wget -O config/hunspell/ru_RU.zip https://bitbucket.org/Shaman_Alex/russian-dictionary-hunspell/downloads/ru_RU_UTF-8_20131101.zip
RUN unzip config/hunspell/ru_RU.zip -d config/hunspell/ru_RU