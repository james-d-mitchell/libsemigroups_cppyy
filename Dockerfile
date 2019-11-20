FROM libsemigroups/libsemigroups-cppyy

MAINTAINER J. D. Mitchell <jdm3@st-andrews.ac.uk>

COPY --chown=1000:1000 . $HOME/libsemigroups_cppyy

RUN sudo pip3 install ipywidgets RISE

RUN jupyter-nbextension install rise --user --py

RUN jupyter-nbextension enable rise --user --py

USER libsemigroups_cppyy

WORKDIR $HOME/libsemigroups_cppyy
