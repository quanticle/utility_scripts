#! /usr/bin/python
import subprocess
import sys
import os.path
import mutagen.flac 
import mutagen.id3
import mutagen.mp3
import glob
def rip_to_wav(speed=None):
    """Uses subprocess to run CDParanoia to rip the given CD to wav files in the
    current directory"""
    
    if speed == None:
        subprocess.check_call(['cdparanoia', '-B'])
    else:
        subprocess.check_call(['cdparanoia', '-B', '-S', str(rip_speed)])

def rip_to_flac(input_file_name, output_file_name):
    """Uses subprocess to call FLAC to convert the input file (presumably a wav
    file to a FLAC file"""

    subprocess.check_call(['flac', '-o', output_file_name, input_file_name])

def rip_to_mp3(input_file_name, output_file_name):
    """Uses subprocess to call LAME to convert the input file (presumably a wav
    file to an MP3 file"""

    subprocess.check_call(['lame', '--replaygain-accurate', '-q', '2', '-b', '320', input_file_name, output_file_name])

def write_mp3_tags(artist, album):
    """Write the artist and album tags to all MP3 files in the current
    directory"""
    
    mp3_file_list = glob.glob(r'*.mp3')
    lead_artist_tag = mutagen.id3.TPE1(encoding=3, text=artist)
    contributing_artist_tag = mutagen.id3.TPE2(encoding=3, text=artist)
    album_tag = mutagen.id3.TALB(encoding=3, text=album)
    for mp3_file_name in mp3_file_list:
        mp3_tagger = mutagen.mp3.MP3(mp3_file_name)
        mp3_tagger["TPE1"] = lead_artist_tag
        mp3_tagger["TPE2"] = contributing_artist_tag
        mp3_tagger["TALB"] = album_tag
        mp3_tagger.save()

def write_flac_tags(artist, album):
    """Write artist and album tags to all FLAC files in the current directory"""

    flac_file_list = glob.glob(r'*.flac')
    for flac_file_name in flac_file_list:
        flac_tagger = mutagen.flac.FLAC(flac_file_name)
        flac_tagger['artist'] = artist
        flac_tagger['album'] = album
        flac_tagger.save()

def main(artist, album, rip_speed=None):
    if rip_speed == None:
        rip_to_wav()
    else:
        rip_to_wav(speed=rip_speed)
    for wav_file in glob.glob(r'*.wav'):
        output_file_base = os.path.splitext(wav_file)[0]
        rip_to_flac(wav_file, output_file_base + ".flac")
        rip_to_mp3(wav_file, output_file_base + ".mp3")
    write_flac_tags(artist, album)
    write_mp3_tags(artist, album)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:\n  cd_rip.py <artist> <album> [rip speed]"
        sys.exit(1)
    if len(sys.argv > 3):
        main(sys.argv[1], sys.argv[2], rip_speed=int(sys.argv[3]))
    else:
        main(sys.argv[1], sys.argv[2])


