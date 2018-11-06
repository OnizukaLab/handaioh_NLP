FROM ubuntu:16.04
MAINTAINER handioh NLPteam <nishikigi.nlp@gmail.com>

# apt-get
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install git vim curl locales mecab libmecab-dev mecab-ipadic-utf8 make xz-utils file sudo bzip2 wget python3-pip

# install pyenv
ENV HOME /root
RUN git clone https://github.com/yyuu/pyenv.git $HOME/.pyenv
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    eval "$(pyenv init -)"

RUN pyenv install anaconda3-4.2.0
RUN pyenv global anaconda3-4.2.0

# install python3 packages
RUN pip3 install --upgrade pip
RUN pip3 install mecab-python3

# character encoding
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# add MeCab Neologd
WORKDIR /usr/src/
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /usr/src/mecab-ipadic-neologd && \
/usr/src/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y
RUN mecab -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/

RUN git clone -b develop https://github.com/OnizukaLab/handaioh_NLP.git /home/handaioh/
ADD ./mysite/handaioh_NLP/utils/data/ /home/handaioh/mysite/handaioh_NLP/utils/data/

WORKDIR /home/handaioh/
CMD ["/bin/bash"]

