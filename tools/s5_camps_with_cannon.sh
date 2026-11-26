#!/bin/zsh
# S5 alternate: full camps + cannon v10 in ONE file per wall (1080, ProRes 422 HQ, 25 fps, sound in).
set -e
S="/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05_the-camps"
O="/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S5_camps_with_cannon"
K=10657   # cannon f0 == camps f10657 (fallback_v10 measure.txt)
mkdir -p "$O"
for w in CENTRE LEFT RIGHT FLOOR; do
  echo "== $w $(date +%T)"
  ffmpeg -v error -y -i "$S/S5_${w}_camps.mov" -map 0:v:0 -frames:v $K -c:v copy "$O/_a_$w.mov"
  ffmpeg -v error -y -i "$S/S5_${w}_cannon.mov" -map 0:v:0 -vf "scale=1920:1080:flags=lanczos,format=yuv422p10le" \
    -c:v prores_ks -profile:v 3 -vendor apl0 -r 25 "$O/_b_$w.mov"
  printf "file '%s'\nfile '%s'\n" "$O/_a_$w.mov" "$O/_b_$w.mov" > "$O/_list_$w.txt"
  ffmpeg -v error -y -i "$S/S5_${w}_camps.mov" -i "$S/S5_${w}_cannon.mov" -filter_complex \
    "[0:a]atrim=end_sample=$((K*1920)),asetpts=N/SR/TB[a0];[1:a]asetpts=N/SR/TB[a1];[a0][a1]concat=n=2:v=0:a=1[a]" \
    -map "[a]" -c:a pcm_s24le "$O/_s_$w.wav"
  ffmpeg -v error -y -f concat -safe 0 -i "$O/_list_$w.txt" -i "$O/_s_$w.wav" -map 0:v -map 1:a -c copy \
    "$O/S5_${w}_camps-with-cannon.mov"
  rm "$O/_a_$w.mov" "$O/_b_$w.mov" "$O/_list_$w.txt" "$O/_s_$w.wav"
  ffprobe -v error -count_packets -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_packets:format=duration \
    -of compact "$O/S5_${w}_camps-with-cannon.mov"
done
echo "DONE $(date +%T)"
