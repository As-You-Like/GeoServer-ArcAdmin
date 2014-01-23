###############################################################################
#																			  #
# Yazar: Mehmet Selim BILGIN	mselimbilgin[at]yahoo.com					  #
# Tarih: 25 Aralik 2013														  #
# Dosya adi: rasterYukle.py											 		  #
# Aciklama: GeoServer 'a raster veri (TIFF) yuklemek icin kullanilir. 		  #
# Lisans: GPL v2															  #
#																			  #
###############################################################################


import urllib2
import os
import tempfile
import zipfile
import arcpy

katmanAdi = str(arcpy.GetParameterAsText(0))
geoserverRestUrl = str(arcpy.GetParameterAsText(1))
workspaceAdi = str(arcpy.GetParameterAsText(2))
kAdi = str(arcpy.GetParameterAsText(3))
sifre  = str(arcpy.GetParameterAsText(4))

tempKlasor = tempfile.mkdtemp("gecici")
sadeKatmanAdi = os.path.splitext(os.path.basename(katmanAdi))[0]

geciciTif = tempKlasor + os.sep + sadeKatmanAdi + '.tif'   #Eger katmanAdi uzantiya sahip degilse (ornegin FGDB den geliyorsa) tif uzantisi eklenir. 
arcpy.management.CopyRaster(katmanAdi, geciciTif)							

zipDosya = zipfile.ZipFile((tempKlasor + os.sep + sadeKatmanAdi + '.zip'), 'w', zipfile.ZIP_DEFLATED) #zip dosyasinin adi direk olarak tif dosyasindan gelmektedir.
zipDosya.write(geciciTif, os.path.basename(geciciTif)) #zip dosyasi i�erisine direkt olarak tif dosyasi eklenir. Klasor yolu eklenmez.
zipDosya.close()

binaryVeri = open(zipDosya.filename, 'rb').read()

girisBasic = 'Basic ' + (kAdi + ':' + sifre).encode('base64').rstrip()
	
url = geoserverRestUrl + '/workspaces/' + workspaceAdi + '/coveragestores/' + sadeKatmanAdi + '/file.geotiff'	#Burada ise katmanAdi degiskeni uzanti tasiyorsa uzantisi alinmaz.
istek = urllib2.Request(url)
istek.add_header("Authorization", girisBasic)
istek.add_header("Content-type", "application/zip")
istek.add_header("Accept", "*/*")
istek.add_data(binaryVeri)
istek.get_method = lambda: 'PUT'
urllib2.urlopen(istek)
