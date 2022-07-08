#!/usr/bin/bash -x

base_path="../${PWD}/fixtures_data"
function create_debian() {
    export DEBIAN_PATH=$1/"debian"
    mkdir -p $DEBIAN_PATH
    debootstrap stable ${DEBIAN_PATH} &> /dev/null
    echo ${DEBIAN_PATH}
}

function create_archlinux() {
    export ARCHLINUX_PATH=$1/"archlinux"
    mkdir -p $ARCHLINUX_PATH
    pacstrap archlinux base &> /dev/null
    echo ${ARCHLINUX_PATH}
}

export DEBIAN_PATH=$(create_debian ${base_path} ) &
export ARCHLINUX_PATH=$(create_archlinux ${base_path}) &
wait
