FROM ubuntu:16.04
MAINTAINER handioh NLPteam <nishikigi.nlp@gmail.com>

# add an user
RUN useradd -m python_user
WORKDIR /home/python_user

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

RUN pyenv install 3.5.2
RUN pyenv global 3.5.2

# install python3 packages
RUN pip install --upgrade pip
RUN pip install mecab-python3

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

WORKDIR /home/python_user
EXPOSE 16000
CMD ["/bin/bash"]

