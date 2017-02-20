#!/bin/bash
#
#  Update some handy stuff
#

gIconsURL='https://gsuite.google.com/setup/assets/downloads/google-product-logos.zip'
mimeTypesURL='http://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types'

gMapsIconURL='https://lh3.googleusercontent.com/h2xmmkP-_RPM8kimxiZ0brUD_O16N5YsSrJA8srYewnR4Ay0fSevp51AKpIItoQY9ndhdGZFoi-wyAXNxE5mI_xQRVMdJtbAmStE1g=h'

gDrawingsIconURL='https://lh3.googleusercontent.com/flHLQ2o9o8gGi2lHhT5QeZT3fC04iz-gTgOhgTDMgP9l2iiXAWFrvEiPKPGcQ1hgVNBJ2j8dpa-XpJ3rGkIUxBXh63rtfdImVnTjMA=h120'

gScriptIconURL='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGYAAABmCAMAAAAOARRQAAAAolBMVEX////y8vJGh/RGiPRHiPRPjfVPjvVMjPVOjfVQjvVFh/RNjPVIifTx8fFRj/Xw9f6mxfqLrvCqyPp9qvfd5PKArPc9hPT49fHC0fOFrvOgwfmDpug7gfREfeVCed8xfvRActVjmfRBdNzI2fjR3fgoduykvvKcuvJdlfX3+v6TtfeyyPO9zvPh6vqkxPtTiulokONvofRymOR8n+bX5P0+eOS9lSC/AAAEAUlEQVRoge3aa2/aMBQG4CZ2IIkd6EpJaBfKKC29d+va/f+/ttiQxpfj5NgwaZP2foxUHh2/ttIETk7+55/K9OPp9XI4z4cpH7O0CRsD4W1iQvK3zcMBymadTVzJREZNkiThs7NNuPLy5lZM5jTceRq7FYt5DXUeHlMcwwRzehrYz/SiZ80mrdIxges2nXsyYQ6OSRQmqJ9eJoOYoH6m88SbCVi3QWYEMP7rhmISg2kcz3XrYzIn493PdO4+nn2MZz89TKZWYzF+/WCYBGL8+nEz+jA249VPP9MpKcB49ONkMgSD78fFmErK2JvF4PtxMBnA3L/aDraf6ZyhlDRJkwuAQfYDMooy2itps9W+PwLO5SKUMRXJNHuAf/9yCfSzQKwbwDiUJnz54/2rlfenYWc6H0OIpewYvvxm5/rn1JfJbKUbho05W15d60YTXyZzKi3DGb+6NuPBZEpGLkVC/MoIjmGZnpFTacLE/+3LIzC9ypgBzq93b2bUr4z3FS3V+DEjJYmlsE6RG1tlZqgtMDKjIYAiD+qhTOJUVEZ1ApjErTBVUR0/JlGS9s4iGe7LJGZSQGGm8unguuEDiGMWERrOpINK9xjP4xAmTS2jfVsAzSLGocs4LvFMqoepCnfNIudBM6kVbZTyY0LhWXYDhTLaKA1TLe6pm+E092bUXdu+t6mraDHhToVzP4YxCBmzhok2NXcqSIYyOx3CJFNtJsSlcFw3NjNWFclEUdMPjAQx6su0/aUdI/qBQz0Z45Ud05loU8IKkiHQa0HlQLaM6AdSApm81HO7Z0Q/lkNDmfunhZ7nT8buhwYxYs+uzysjURejH+rJdE3Q9XnkTtNPbioEx8TameG9jOgn1pU/wRRFsUiJrhyfaZSi6SfXFBwzwzOFzK6fTkEyOZYp9hHnR1GOyxRdok0Sdwru7oljClWJtpR0ijcjm4WYQlOKuzxWFCyjH2ybKfREdyRXleMwJlJtc105BlOYSrSVs5BOCWKIypiI7MVUDmMKG2l7IZqShzDAjcDsxVDCmMn8Qs+sdfa9mEoYQ8VfqllVai8WEshYaZlK9AIoSCZGMbIXAinInTbAUMlERdMLrByFoZKRvUBIHnhudEJEMKIXDVGUwxjaZlV1vQDIIQxV0kxz16cEMlQPWVWGkusK9txQd+StfrfH4tihIJmyh5DheWfYyGEMUWMhqhLMEIJD9hdqH4aA6VbLheQlkoEB3bCRT+UwJgYRcxTxaBfMxPEAoioo5uGxdHy4SeT2xd3Daf2I+ALnrAY/Ho2U5epsWDl5WZeDBLRcn0q9fkEwJ4sYcByGPUpZU9SXa+JnQ7d12ZfandXtGv8V6832S2C2N8O77H/+qvwGS84V5EjDILcAAAAASUVORK5CYII='

if [ ! -e google-product-logos.zip ]; then
    wget ${gIconsURL}
fi

if [ ! -d google-product-logos ]; then
    unzip google-product-logos.zip
fi

if [ ! -d google-logos ]; then
    mkdir google-logos
    mkdir google-logos/32px
    mkdir google-logos/48px
    mkdir google-logos/64px
    mkdir google-logos/128px
fi

#mv google-product-logos/*32px*  google-logos/32px
#mv google-product-logos/*48px*  google-logos/48px
#mv google-product-logos/*64px*  google-logos/64px
#mv google-product-logos/*128px* google-logos/128px

# maps icon
#for px in 32 48 64 128; do
#    echo "Getting ${px}"
#    wget -O google-logos/${px}px/logo_maps_${px}px.png ${gMapsIconURL}${px}
#done

# drawings icon
for px in 32 48 64 120; do
    echo "Getting ${px}"
    wget -O google-logos/${px}px/logo_draw_${px}px.png ${gDrawingsIconURL}${px}
done
