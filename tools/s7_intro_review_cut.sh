#!/bin/zsh
# review_cut.sh FLIGHT TRIM_FRAMES LAND OUTDIR WALLDIR
#  A: S7-INTRO_review_v1.mp4  = flight frames [0, TRIM) + land (whole), 1920x1080 centre-cropped to 5:3 1800x1080 (CENTRE),
#     sound kept (both clips' generated audio, joined).
#  B: S7-INTRO_review_v1_3walls_4680.mp4 = A on CENTRE between dark side walls (the side-wall sea loops don't exist yet),
#     then the wing's last frame dissolves (0.5 s) into the three DAY deck walls (3_walls/assembled_v1), held 4 s.
set -e
FL=$1; TRIM=$2; LD=$3; OD=$4; WD=$5
TMP=$(mktemp -d)
TT=$(python3 -c "print(f'{$TRIM/24:.6f}')")
A="$OD/S7-INTRO_review_v1.mp4"
ffmpeg -v error -y -i "$FL" -i "$LD" -filter_complex \
 "[0:v]trim=end_frame=$TRIM,setpts=PTS-STARTPTS,crop=1800:1080:60:0,setsar=1,format=yuv420p[v0];\
  [0:a]atrim=end=$TT,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a0];\
  [1:v]setpts=PTS-STARTPTS,scale=1920:1080,crop=1800:1080:60:0,setsar=1,format=yuv420p[v1];\
  [1:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a1];\
  [v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" -r 24 -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "$A"
NF=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$A")
ffmpeg -v error -y -i "$A" -vf "select=eq(n\,$((NF-1)))" -frames:v 1 "$TMP/last.png"
ffmpeg -v error -y -i "$TMP/last.png" -vf "pad=4680:1080:1440:0:color=0x0b0b0b" "$TMP/last3.png"
ffmpeg -v error -y -i "$WD/S7-SHIP-LEFT_1080.png" -i "$WD/S7-SHIP-CENTRE_1080.png" -i "$WD/S7-SHIP-RIGHT_1080.png" \
 -filter_complex "[0][1][2]hstack=3" "$TMP/deck.png"
B="$OD/S7-INTRO_review_v1_3walls_4680.mp4"
DA=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$A")
ffmpeg -v error -y -i "$A" -loop 1 -framerate 24 -t 0.5 -i "$TMP/last3.png" -loop 1 -framerate 24 -t 4.5 -i "$TMP/deck.png" \
 -filter_complex \
 "[0:v]pad=4680:1080:1440:0:color=0x0b0b0b,setsar=1,format=yuv420p[film];\
  [1:v]format=yuv420p,setsar=1[t1];[2:v]format=yuv420p,setsar=1[t2];\
  [t1][t2]xfade=transition=fade:duration=0.5:offset=0[end];\
  [film][end]concat=n=2:v=1:a=0[v];[0:a]apad=pad_dur=4.5[a]" \
 -map "[v]" -map "[a]" -r 24 -t $(python3 -c "print($DA+4.5)") -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p \
 -c:a aac -b:a 256k -movflags +faststart "$B"
for f in "$A" "$B"; do ffprobe -v error -show_entries stream=codec_type,width,height,nb_frames:format=duration -of compact "$f"; done
rm -rf "$TMP"
