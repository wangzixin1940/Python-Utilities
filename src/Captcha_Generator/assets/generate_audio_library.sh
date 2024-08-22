# Set the language code
export ESLANG=en

# Create a directory for the specified language code
mkdir "$ESLANG"

# Loop through each character (a-z, A-Z, 0-9) and create a directory for each
for i in {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0,1,2,3,4,5,6,7,8,9}; do
    mkdir "$ESLANG/$i"
    espeak -a 150 -s 100 -p 15 -v "$ESLANG" "$i" -w "$ESLANG/$i/orig_default.wav"
    ffmpeg -i "$ESLANG/$i/orig_default.wav" -ar 8000 -ac 1 -acodec pcm_u8 "$ESLANG/$i/default.wav"
    rm "$ESLANG/$i/orig_default.wav"
done

# Tips:
# If you are using Windows, you can run it using Cygwin Terminal, a Unix-Based virtual machine, Microsoft WSL shell (Windows 10+) , or a Unix-Based physical machine.
# If the prompt does not find the command, run the following command (choose one):
###
# sudo apt install espeak ffmpeg           # Advanced Package Tool (or APT)
# brew install espeak ffmpeg               # Homebrew
# pacman -S espeak ffmpeg                  # Arch Linux Pacman Package Manager
# yum install espeak ffmpeg                # CentOS Yum
###


# This script is from: https://captcha.lepture.com/audio/#voice-library

