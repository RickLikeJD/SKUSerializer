import os, struct, zlib, shutil, pathlib
from tkinter import *
from tkinter import filedialog

print("Skuscene Serializer by RickL\nBased on JackLSummer SkuENC")

map_count=0
i=0 #conta os mapas apenas para eu ter certeza :)
contagem = 1 #questão de ficar bonitinho

try:
	os.mkdir('output')
	
except:
	pass

# Initializes Tkinter (file picker)
openFile = Tk()
openFile.title('')

# Searches for the necessary folder
directory = filedialog.askdirectory(initialdir=str(pathlib.Path().absolute()), title="Select your IPK folder")

# Destroys Tkinter
openFile.destroy()

skuenc=open("output/skuscene_maps_pc_all.isc.ckd","wb")

skudb="skuscene_db"
skubasetpl="skuscene_base.tpl"
skubasepath="world/skuscenes/"

# header
skuenc.write(struct.pack(">I", 1))
skuenc.write(bytes.fromhex("00033E9E000000000000000000000000"))
for filename in os.scandir(directory):
    if filename.is_file() and filename.name.lower().endswith('.ipk'):
        i += 1
skuenc.write(struct.pack(">I",1+int(i)))
# end of header

# skuscene base & skuscene db + things ^^
skuenc.write(bytes.fromhex("97CA628B000000003F8000003F800000000000000000000B736B757363656E655F6462FFFFFFFF0000000000000000000000000000000000000000FFFFFFFF0000000000000011736B757363656E655F626173652E74706C00000010776F726C642F736B757363656E65732F0C1C9B77000000000000000000000001405579FB"))
after_mapname = "97CA628B000000003F8000003F80000000000000"
before_mapname = "FFFFFFFF0000000000000000000000000000000000000000FFFFFFFF00000000"
before_sdpath = "000000020000000000000001E07FCC3F"
# end

for filename in os.scandir(directory):
    if filename.is_file() and filename.name.lower().endswith('_wii.ipk'):
        bundlename = filename.name.replace('_wii.ipk', '')  # Remove the "_wii.ipk" suffix
        print(str(contagem) + " | adding " + bundlename)
        songdesctpl = "songdesc.main_legacy.tpl"
        songdescpath = "cache/legacyconverteddata/" + bundlename + "/"
        skuenc.write(bytes.fromhex(after_mapname))
        
        skuenc.write(struct.pack(">I", len(bundlename)) + bundlename.encode())

        skuenc.write(bytes.fromhex(before_mapname))

        skuenc.write(struct.pack(">I", len(songdesctpl)) + songdesctpl.encode())

        skuenc.write(struct.pack(">I", len(songdescpath)) + songdescpath.encode() + struct.pack("<I", zlib.crc32(songdescpath.encode())))

        skuenc.write(bytes.fromhex(before_sdpath))
        contagem += 1
        map_count += 1

skuenc.write(bytes.fromhex("000000000000000000000001F878DC2D0000000E6A64323032302D7769692D6E6F61000000044E43534100000013726174696E675F657372625F3136392E69736300000025776F726C642F75692F73637265656E732F626F6F7473657175656E63652F726174696E672F8ACD0EAD00000000"))
skuenc.write(struct.pack(">I",int(i)))

for filename in os.scandir(directory):
    if filename.is_file() and filename.name.lower().endswith('_wii.ipk'):
        bundlename = filename.name.replace('_wii.ipk', '')  # Remove the "_wii.ipk" suffix
        covergenericact = bundlename + "_cover_generic.act"
        menuartpath = "world/maps/" + bundlename + "/menuart/actors/"
        
        skuenc.write(struct.pack(">I", len(bundlename)) + bundlename.encode())

        skuenc.write(struct.pack(">I", len(covergenericact)) + covergenericact.encode())

        skuenc.write(struct.pack(">I", len(menuartpath)) + menuartpath.encode() + struct.pack("<I", zlib.crc32(menuartpath.encode())))
        skuenc.write(struct.pack(">q", 0))
    
        map_count += 1
skuenc.write(struct.pack(">I", 0))
skuenc.close()

pcisc="output/skuscene_maps_pc_all.isc.ckd"
wiinoaisc="output/skuscene_maps_wii_noa.isc.ckd"

shutil.copy(pcisc,wiinoaisc)

if map_count == 0:
    print("não há mapas")
    os.system("pause")
    shutil.rmdir("output")
    
else:
    print("todos os "+str(i)+" mapas foram adicionados!")
    os.system("pause")
