#!/bin/zsh
# s7_intro_3walls.sh CLIP_21x9 WALLDIR OUT [XFADE_S] [HOLD_S]
# Route A (Homie, 7 Oct): the ship intro as ONE picture across the three walls.
#  - scales the 21:9 take to 4680 wide and keeps the centred 4.33:1 band (LEFT 1440 | CENTRE 1800 | RIGHT 1440);
#  - the last XFADE_S seconds dissolve into the three deck walls (WALLDIR/S7-SHIP-{LEFT,CENTRE,RIGHT}_1080.png),
#    held HOLD_S seconds after the clip ends;
#  - the clip's own sound rides through (house rule), padded under the hold.
# Preview/review quality (H.264). Show files are built from the approved 1080p/4K take later.
set -e
CL=$1; WD=$2; OUT=$3; XF=${4:-1.0}; HOLD=${5:-3.0}
TMP=$(mktemp -d)
ffmpeg -v error -y -i "$WD/S7-SHIP-LEFT_1080.png" -i "$WD/S7-SHIP-CENTRE_1080.png" -i "$WD/S7-SHIP-RIGHT_1080.png" \
 -filter_complex "[0][1][2]hstack=3" "$TMP/deck.png"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CL")
OFF=$(python3 -c "print(max(0.0,$DUR-$XF))")
TOT=$(python3 -c "print($DUR+$HOLD)")
ffmpeg -v error -y -i "$CL" -loop 1 -framerate 24 -t $(python3 -c "print($XF+$HOLD+0.5)") -i "$TMP/deck.png" -filter_complex \
 "[0:v]fps=24,scale=4680:-2:flags=lanczos,crop=4680:1080:0:(ih-1080)/2,setsar=1,format=yuv420p[film];\
  [1:v]fps=24,scale=4680:1080,setsar=1,format=yuv420p[deck];\
  [film][deck]xfade=transition=fade:duration=${XF}:offset=${OFF}[v];\
  [0:a]aresample=48000,apad[a]" \
 -map "[v]" -map "[a]" -t $TOT -r 24 -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -c:a aac -b:a 256k \
 -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,width,height:format=duration -of compact "$OUT"
rm -rf "$TMP"
