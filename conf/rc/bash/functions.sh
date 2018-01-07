jmp() {
    if test $# -eq 0 ;then
        cat $REPOS/mgtools/conf/jmp.conf
    elif test $1 = "add" ;then
        echo $2 >> $REPOS/mgtools/conf/jmp.conf
    else
        cat $REPOS/mgtools/conf/jmp.conf | grep -oP "^$1:.*$" | perl -pe "s@$1:(.*)@\1@g" > $REPOS/mgtools/.tmp/jmp.tmp
        echo "cd "$(cat $REPOS/mgtools/.tmp/jmp.tmp) > $REPOS/mgtools/.tmp/jmp.tmp.tmp
        mv $REPOS/mgtools/.tmp/jmp.tmp.tmp $REPOS/mgtools/.tmp/jmp.tmp
        source $REPOS/mgtools/.tmp/jmp.tmp
    fi
}

recgif(){
    export WINDOWID=$(xdotool getwindowfocus)
    ttyrec /tmp/.gif_record
}

mkgif(){
    export WINDOWID=$(xdotool getwindowfocus)
    ttygif /tmp/.gif_record
    if test $# -ge 1 ;then
        mv tty.gif $1
        echo "[+]mv tty.gif "$1
    fi
    rm -rf /tmp/.gif_record
}

repobase(){
    now=$(pwd)/
    if test "$(echo $now | rg "/mnt/c/Users/miyagaw61/home/")" ;then
        now=$(echo $now | rg "/mnt/c/Users/miyagaw61/home/" -r "/home/miyagaw61/")
    fi
    now=$(echo "$now" | sed -E "s@$REPOS@@g")
    now=$(echo "$now" | sed -E "s@^/@@g")
    repo=$(echo "$now" | sed -E "s@/.*@@g")
    cd $REPOS/$repo
}

nv(){
    if test $# -eq 0 ;then
        nvr -c "Denite buffer"
    fi
    nvr -c "e "$(realpath $1)
}

nd(){
    nvr -c "cd "$(realpath $1)
}

repos(){
    var=$(rg --files $REPOS | rsed '[^/]*$' '' | sort | uniq | fzf2nd)
    if test "$var" ;then
        cd $var
    fi
}

#readline_injection() {
#  READLINE_LINE="$READLINE_LINE | hoge"
#  READLINE_POINT=${#READLINE_LINE}
#}
#bind -x '"\C-j":readline_injection'
