FROM ubuntu:24.04@sha256:1e622c5f073b4f6bfad6632f2616c7f59ef256e96fe78bf6a595d1dc4376ac02

ENV user=chall
ENV chall_port=44332

USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron socat vim-common bash xxd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1337 -s /bin/bash $user

COPY ./deploy/ /home/$user/
COPY ./makeflag.sh /home/$user/makeflag.sh
COPY mycron /etc/cron.d/mycron

RUN chown -R $user:$user /home/$user && \
    chmod 755 /home/$user && \
    chmod 700 /home/$user/makeflag.sh && \
    chmod 0644 /etc/cron.d/mycron

WORKDIR /home/$user

EXPOSE ${chall_port}
RUN ./makeflag.sh

CMD service cron start && su -s /bin/bash chall -c "exec socat TCP-LISTEN:${chall_port},reuseaddr,fork EXEC:'/home/chall/chal'"
