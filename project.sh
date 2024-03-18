#!/bin/bash

if [ -n "$PREFIX" ] && [ "$PREFIX" = "/data/data/com.termux/files/usr" ]
then
    IS_TERMUX=1
else
    IS_TERMUX=0
fi


log_progress() {
    echo -e "🤖 \e[0;33m${1}\e[0;0m"
}


command_exists() {
    command -v "$1" &> /dev/null
}


init() {
    export PROJECT_DIR=$(pwd)
    log_progress "Setting project directory to ${PROJECT_DIR}"
    if ! command_exists poetry
    then
        log_progress 'Install poetry'
        pip install --upgrade pip setuptools
        pip install "poetry"
    fi
    if [ ! -d "${PROJECT_DIR}/.venv" ]
    then
        log_progress 'Creating virtual environment'
        python -m venv "${PROJECT_DIR}/.venv"
    fi
    log_progress 'Activating virtual environment'
    source "${PROJECT_DIR}/.venv/bin/activate"
}


reload() {

    if [ ! -f "${PROJECT_DIR}/.env" ]
    then
        log_progress 'Creating project configuration (.env)'
        cp "${PROJECT_DIR}/template.env" "${PROJECT_DIR}/.env"
    fi

    log_progress 'Loading project configuration (.env)'
    source "${PROJECT_DIR}/.env"

    if [ "$IS_TERMUX" = "1" ]
    then
        log_progress 'Updating Build Flags'
        _OLD_CFLAGS="$CFLAGS"
        export CFLAGS="$_OLD_CFLAGS -Wno-incompatible-function-pointer-types -O0" # ruamel.yaml need this.
        export CFLAGS="$CFLAGS -U__ANDROID_API__ -D__ANDROID_API__=31"      
        _OLD_MATHLIB="$MATHLIB"
        export MATHLIB="m"
        _OLD_LDFLAGS="$LDFLAGS"
        export LDFLAGS="-lm -lpython$(python --version | awk '{print $2}' | cut -d. -f1,2)"
    fi

    log_progress 'Install'
    if [ "$IS_TERMUX" = "1" ]
    then
        poetry install -E openai -E bedrock
    else
        poetry install -E openai -E bedrock -E embedding-cpu
    fi

    if [ "$IS_TERMUX" = "1" ]
    then
        log_progress 'Install required pip packages to build numpy'
        pip install setuptools wheel packaging pyproject_metadata cython meson-python versioneer
        log_progress 'Reinstall numpy'
        pip uninstall -y numpy
        pip install --no-build-isolation --no-cache-dir numpy
        log_progress 'Restoring Build Flags'
        export CFLAGS="$_OLD_CFLAGS"
        export MATHLIB="$_OLD_MATHLIB"
        export LDFLAGS="$_OLDLDFLAGS"
    fi

    _CURRENT_SHELL=$(ps -p $$ | awk 'NR==2 {print $4}')
    case "$_CURRENT_SHELL" in
    *zsh)
        _CURRENT_SHELL="zsh"
        ;;
    *bash)
        _CURRENT_SHELL="bash"
        ;;
    esac
    if [ "$_CURRENT_SHELL" = "zsh" ] || [ "$_CURRENT_SHELL" = "bash" ]
    then
        log_progress "Setting up shell completion for $_CURRENT_SHELL"
        eval "$(_ZRB_COMPLETE=${_CURRENT_SHELL}_source zrb)"
    else
        log_progress "Cannot set up shell completion for $_CURRENT_SHELL"
    fi
}

init
reload
log_progress 'Happy Coding :)'
