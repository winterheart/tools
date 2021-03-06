import os
import construct
import argparse
from PIL import Image

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= construct.version[0] and 8 > construct.version[1]:
    raise ValueError("Built for construct >= 2.8 only")
    
g_pal = [
(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0x04, 0x44, 0x20),(0x48, 0x6C, 0x50),
(0x00, 0x50, 0x28),(0x34, 0x64, 0x40),(0x08, 0x3C, 0x1C),(0x00, 0x00, 0x00),
(0x44, 0x30, 0x30),(0x00, 0x00, 0x00),(0x3C, 0x28, 0x24),(0x00, 0x00, 0x00),
(0xBC, 0x80, 0x48),(0x00, 0x00, 0x00),(0x20, 0x10, 0x14),(0x00, 0x00, 0x00),
(0x2C, 0x80, 0x5C),(0x00, 0x00, 0x00),(0x3C, 0x2C, 0x64),(0x00, 0x00, 0x00),
(0x54, 0x2C, 0x0C),(0x00, 0x00, 0x00),(0x64, 0x78, 0x9C),(0x00, 0x00, 0x00),
(0x34, 0x88, 0x5C),(0x00, 0x00, 0x00),(0x44, 0x24, 0x10),(0x00, 0x00, 0x00),
(0x40, 0x3C, 0x38),(0x00, 0x00, 0x00),(0xDC, 0xAC, 0x84),(0x00, 0x00, 0x00),
(0xFC, 0xB0, 0x64),(0xC8, 0x8C, 0x4C),(0x94, 0x68, 0x38),(0x60, 0x44, 0x24),
(0x30, 0x20, 0x10),(0x00, 0x00, 0x00),(0xD0, 0x70, 0x30),(0xB8, 0x60, 0x28),
(0xA0, 0x54, 0x24),(0x88, 0x48, 0x1C),(0x70, 0x3C, 0x18),(0x58, 0x30, 0x10),
(0x40, 0x20, 0x0C),(0x2C, 0x14, 0x08),(0x14, 0x08, 0x04),(0x00, 0x00, 0x00),
(0xAC, 0xC4, 0xE8),(0x40, 0x2C, 0x5C),(0xB4, 0xCC, 0xF0),(0x2C, 0x24, 0x50),
(0x3C, 0x3C, 0x50),(0x1C, 0x1C, 0x28),(0x00, 0x00, 0x00),(0x70, 0x50, 0xBC),
(0x60, 0x44, 0xA4),(0x50, 0x38, 0x8C),(0x44, 0x30, 0x74),(0x34, 0x24, 0x5C),
(0x28, 0x1C, 0x44),(0x18, 0x10, 0x2C),(0x08, 0x04, 0x14),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0xFC),(0xE8, 0xE8, 0xE8),(0xD8, 0xD8, 0xD8),(0xC8, 0xC8, 0xC8),
(0xB8, 0xB8, 0xB8),(0xA4, 0xA4, 0xA4),(0x94, 0x94, 0x94),(0x84, 0x84, 0x84),
(0x74, 0x74, 0x74),(0x60, 0x60, 0x60),(0x50, 0x50, 0x50),(0x40, 0x40, 0x40),
(0x30, 0x30, 0x30),(0x1C, 0x1C, 0x1C),(0x0C, 0x0C, 0x0C),(0x00, 0x00, 0x00),
(0xBC, 0xD4, 0xF8),(0x00, 0x00, 0x00),(0x9C, 0xB8, 0xEC),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0x00),(0xE4, 0xE4, 0x00),(0xCC, 0xCC, 0x00),(0xB4, 0xB4, 0x00),
(0x9C, 0x9C, 0x00),(0x88, 0x88, 0x00),(0x70, 0x70, 0x00),(0x58, 0x58, 0x00),
(0x40, 0x40, 0x00),(0x28, 0x28, 0x00),(0x14, 0x14, 0x00),(0x00, 0x00, 0x00),
(0xFC, 0xE0, 0xBC),(0x84, 0x74, 0x64),(0xFC, 0xF0, 0xCC),(0x70, 0x68, 0x60),
(0xF4, 0xCC, 0xA0),(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0xFC, 0x00, 0x00),
(0xDC, 0x00, 0x00),(0xBC, 0x00, 0x00),(0x9C, 0x00, 0x00),(0x7C, 0x00, 0x00),
(0x5C, 0x00, 0x00),(0x3C, 0x00, 0x00),(0x1C, 0x00, 0x00),(0x00, 0x00, 0x00),
(0xE8, 0xB8, 0x90),(0xCC, 0xA0, 0x80),(0xB4, 0x8C, 0x70),(0x98, 0x78, 0x5C),
(0x80, 0x64, 0x4C),(0x64, 0x50, 0x3C),(0x48, 0x38, 0x2C),(0x30, 0x24, 0x1C),
(0x14, 0x10, 0x0C),(0x00, 0x00, 0x00),(0xD4, 0x80, 0x6C),(0x68, 0x3C, 0x34),
(0x00, 0x00, 0x00),(0xF4, 0x54, 0x00),(0xD4, 0x48, 0x00),(0xB4, 0x3C, 0x00),
(0x94, 0x30, 0x00),(0x78, 0x28, 0x00),(0x58, 0x1C, 0x00),(0x38, 0x10, 0x00),
(0x1C, 0x04, 0x00),(0x00, 0x00, 0x00),(0x00, 0xAC, 0x5C),(0x00, 0x98, 0x50),
(0x00, 0x84, 0x44),(0x00, 0x70, 0x3C),(0x00, 0x5C, 0x30),(0x00, 0x48, 0x24),
(0x00, 0x34, 0x1C),(0x00, 0x24, 0x10),(0x00, 0x10, 0x04),(0x00, 0x00, 0x00),
(0x38, 0x1C, 0x0C),(0x38, 0x74, 0x58),(0x4C, 0x28, 0x0C),(0x2C, 0x80, 0x5C),
(0x00, 0x20, 0x34),(0x38, 0x84, 0x5C),(0x80, 0x38, 0x14),(0x34, 0x88, 0x5C),
(0xC0, 0x98, 0x7C),(0xDC, 0xAC, 0x84),(0x64, 0x38, 0x10),(0x50, 0x2C, 0x64),
(0x4C, 0x14, 0x00),(0x60, 0x3C, 0x8C),(0x3C, 0x30, 0x24),(0x58, 0x18, 0x84),
(0x54, 0x44, 0x30),(0x6C, 0x44, 0x94),(0x70, 0x5C, 0x44),(0x74, 0x4C, 0x9C),
(0x08, 0x2C, 0x18),(0x84, 0x58, 0xA4),(0x6C, 0x20, 0x00),(0x8C, 0x60, 0xB0),
(0x10, 0x08, 0x24),(0x30, 0x28, 0x50),(0x24, 0x18, 0x30),(0x38, 0x28, 0x4C),
(0x20, 0x14, 0x3C),(0x30, 0x2C, 0x48),(0x3C, 0x38, 0x3C),(0x24, 0x24, 0x24),
(0x60, 0x4C, 0x2C),(0x2C, 0x2C, 0x2C),(0x68, 0x54, 0x3C),(0x18, 0x18, 0x18),
(0x28, 0x10, 0x08),(0x78, 0x60, 0x48),(0x30, 0x18, 0x0C),(0x58, 0x48, 0x40),
(0x8C, 0x70, 0x54),(0x38, 0x2C, 0x40),(0xA4, 0x84, 0x60),(0x2C, 0x28, 0x3C),
(0x54, 0x3C, 0x28),(0x24, 0x28, 0x3C),(0x48, 0x48, 0x44),(0x3C, 0x30, 0x48),
(0x58, 0x58, 0x58),(0x3C, 0x2C, 0x44),(0x34, 0x34, 0x34),(0x50, 0xAC, 0x90),
(0x38, 0x28, 0x24),(0x34, 0x94, 0x88),(0x60, 0x24, 0x04),(0x4C, 0x9C, 0x84),
(0x50, 0x18, 0x00),(0x44, 0x34, 0x80),(0x44, 0x10, 0x00),(0x5C, 0x38, 0x98),
(0x34, 0x18, 0x0C),(0x90, 0x50, 0x24),(0x00, 0x40, 0x20),(0xB0, 0x58, 0x20),
(0x2C, 0x28, 0x44),(0x00, 0x00, 0x7C),(0x80, 0x60, 0x34),(0x80, 0x6C, 0xE4),
(0x78, 0x54, 0x28),(0x8C, 0x80, 0xE8),(0xA8, 0x74, 0x40),(0x8C, 0x9C, 0xF8),
(0xBC, 0xB8, 0xDC),(0x00, 0x00, 0x00),(0x8C, 0xAC, 0xDC),(0x00, 0x00, 0x00),
(0x80, 0xA0, 0xD4),(0x00, 0x00, 0x00),(0x70, 0x8C, 0xD0),(0x00, 0x00, 0x00),
(0x78, 0x90, 0xAC),(0x64, 0x78, 0x9C),(0x00, 0x54, 0x28),(0xA0, 0xE8, 0x54),
(0x30, 0x60, 0x34),(0x10, 0x70, 0x5C),(0x58, 0x68, 0x8C),(0x54, 0x54, 0x90),
(0x50, 0x54, 0x88),(0x54, 0x58, 0x94),(0x44, 0x44, 0x80),(0x60, 0x70, 0x8C),
(0xE8, 0x9C, 0x50),(0xF8, 0xD8, 0x00),(0x18, 0xC8, 0x5C),(0xFC, 0xE4, 0x00),
(0x50, 0xDC, 0x44),(0x14, 0x04, 0x00),(0xF8, 0xC4, 0x24),(0x00, 0x00, 0x00),
(0xE4, 0x84, 0x28),(0x00, 0x00, 0x00),(0xF4, 0x7C, 0x1C),(0x00, 0x00, 0x00),
(0xFC, 0xC8, 0x50),(0x00, 0x00, 0x00),(0xFC, 0xA8, 0x3C),(0x00, 0x00, 0x00),
(0xC0, 0x88, 0x30),(0x00, 0x00, 0x00),(0x48, 0x54, 0x68),(0x70, 0x00, 0xC8)]

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

def createdir(dirname):
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)

#
# DAS filename & description
#

das_string_entry = construct.Struct(
    "sizeof"                / construct.Int16ul,            # + 0x00        (sizeof (index) + len(name) + len(desc) + 2)
    "index"                 / construct.Int16ul,            # + 0x02
    "name"                  / construct.CString(),          # + 0x04
    "desc"                  / construct.CString(),          # + 0xXX
)

das_strings = construct.Struct(
    "nb_unk_00"             / construct.Int16ul,                                                # + 0x00
    "nb_unk_01"             / construct.Int16ul,                                                # + 0x02
    "entries_00"            / construct.Array(lambda ctx: ctx.nb_unk_00, das_string_entry),     # + 0x04
    "entries_01"            / construct.Array(lambda ctx: ctx.nb_unk_01, das_string_entry)
)

# cseg01:0004122F 80 7A 06 20                             cmp     byte ptr [edx+6], 20h ; ' '
# cseg01:00041233 74 D8                                   jz      short loc_4120D
# cseg01:00041235 80 7A 06 24                             cmp     byte ptr [edx+6], 24h ; '$'
# cseg01:00041239 74 D2                                   jz      short loc_4120D
# cseg01:0004123B C7 05 2C C7 08 00 00 00+                mov     dword_8C72C, 0
# cseg01:00041245 C7 05 0C C7 08 00 00 00+                mov     dword_8C70C, 0
image_record = construct.Struct(
    "offset_data"           / construct.Int32ul,            # + 0x00
    "length_data_div_2"     / construct.Int16ul,            # + 0x04
    "unk_byte_00"           / construct.Int8ul,             # + 0x06
    "unk_byte_01"           / construct.Int8ul,             # + 0x07
)

anim_das = construct.Struct(
    "field_00"           / construct.Int32ul,               # + 0x00
    "field_04"           / construct.Int16ul,               # + 0x04
    "field_06"           / construct.Int16ul,               # + 0x06
    "field_08"           / construct.Int8ul,                # + 0x08
    "field_09"           / construct.Int8ul,                # + 0x09
    "field_0A"           / construct.Int8ul,                # + 0x0A
    "field_0B"           / construct.Int8ul,                # + 0x0B
    #construct.Probe(),
    # FUCKED DANS ADEMO
    #"addr_delta"         / construct.If(lambda ctx: ctx.field_04 != 0, construct.Array(lambda ctx: (ctx.field_04 / 4) - 5, construct.Int32ul)),
    construct.Int32ul,
    construct.Int32ul,
)

unk_header = construct.Struct(
    "unk_byte_00_f"         / construct.Int8ul,             # + 0x00
    "unk_byte_01_f"         / construct.Int8ul,             # + 0x01
    "width"                 / construct.Int16ul,            # + 0x02
    "height"                / construct.Int16ul,            # + 0x04
    "anim"                  / construct.If(lambda ctx: ctx.unk_byte_01_f & 0x01 != 0x00, anim_das),
    "data"                  / construct.OnDemand(construct.Array(lambda ctx: ctx.width * ctx.height, construct.Byte))
)

#
# DAS file
#
das_file = construct.Struct(
    "signature"             / construct.Const("\x44\x41\x53\x50"),      # + 0x00
    "version"               / construct.Int16ul,                        # + 0x04
    "image_record_length"   / construct.Int16ul,                        # + 0x06
    "image_record_offset"   / construct.Int32ul,                        # + 0x08
    "palette_offset"        / construct.Int32ul,                        # + 0x0C
    "ns_offset_01"          / construct.Int32ul,                        # + 0x10        // length = 0x1000
    "string_table_offset"   / construct.Int32ul,                        # + 0x14
    "string_table_length"   / construct.Int16ul,                        # + 0x18
    "ns_length_02"          / construct.Int16ul,                        # + 0x1A
    "ns_offset_02"          / construct.Int32ul,                        # + 0x1C
    "field_20"              / construct.Int16ul,                        # + 0x20
    "field_22"              / construct.Int16ul,                        # + 0x22
    "ns_offset_03"          / construct.Int32ul,                        # + 0x24        // length = 0x800           || field_34 * 4 (ADEMO.DAS ?!)
    "field_28"              / construct.Int32ul,                        # + 0x28        // length = field_2C
    "field_2C"              / construct.Int32ul,                        # + 0x2C        // length field_28
    "field_30"              / construct.Int32ul,                        # + 0x30
    "field_34"              / construct.Int16ul,                        # + 0x34
    "field_36"              / construct.Int16ul,                        # + 0x36
    "field_38"              / construct.Int32ul,                        # + 0x38        // length = field_3C
    "field_3C"              / construct.Int16ul,                        # + 0x3C        // length field_38
    "field_3E"              / construct.Int16ul,                        # + 0x3E        // length field_40
    "field_40"              / construct.Int32ul,                        # + 0x40        // length = field_3E









    "palette"               / construct.OnDemandPointer(lambda ctx: ctx.palette_offset, construct.String(0x300)),
        # 0x300 + 0x02 + 0x4000 + 0x10000 + 0x100 + 0x100
    "strings"               / construct.OnDemandPointer(lambda ctx: ctx.string_table_offset, das_strings),
    "images"                / construct.OnDemandPointer(lambda ctx: ctx.image_record_offset, 
                                construct.Array(lambda ctx: ctx.image_record_length / 0x08, image_record)),
)

class DAS:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.das_file = das_file.parse_stream(self.stream)

    def get_palette(self):
        if self.das_file.palette_offset != 0x00:
            # palette components is a 6-bit VGA
            pal_0 = self.das_file.palette()
            palette = []
            for i in xrange(0, len(pal_0), 3):
                # scale
                palette.append(((((ord(pal_0[i])) * 255) / 63), (((ord(pal_0[i + 1])) * 255) / 63), (((ord(pal_0[i + 2])) * 255) / 63)))
            return palette
        return g_pal

    #def extract_index(self, index):
    #    if index >= len(self.sfx_file.entry_table()):
    #        return ""
    #    entry = self.sfx_file.entry_table()[index]
    #    return entry.data()
    #
    #def extract_all(self, outdir):
    #    createdir(outdir)
    #    for nb, entry in enumerate(self.sfx_file.entry_table()):
    #        audio_data = entry.data()
    #        wave_output = wave.open(outdir + "/" + sfx.sfx_file.string_table()[nb].name + ".wav", "wb")
    #        # TODO add comment to wave
    #        wave_output.setparams((1, 2, 11025, 0, 'NONE', 'not compressed'))
    #        for i in xrange(0, len(audio_data), 2):
    #            wave_output.writeframes(audio_data[i:i+2])
    #        wave_output.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='das extract launch options')
    parser.add_argument('das_file', action='store', default='', help='dasfile to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=True, metavar='output_directory')

    args = parser.parse_args()

    das = DAS(args.das_file)
    print das.das_file
    createdir(args.output_directory)

    palette = das.get_palette()
    nb = 0
    #print das.das_file.strings()
    str = das.das_file.strings()
    imgs = das.das_file.images()
    for s in str.entries_00 + str.entries_01:
        print s
        continue
        img = imgs[s.index]
        print img
        saved = das.stream.tell()
        das.stream.seek(img.offset_data, 0x00)
        #buf = das.stream.read(0x08)
        #print hexdump(buf)
        #u = unk_header.parse(buf)
        u = unk_header.parse_stream(das.stream)
        print u
        #pixels = das.stream.read(u.width * u.height)
        
        pixels = u.data()
        img_data = ""
        print u.width * u.height
        print len(pixels)
        
        # ANOTHER FUCK DANS ADEMO
        if len(pixels) == 0x00:
            continue
        for i in xrange(0, len(pixels)):
            img_data += chr(palette[(pixels[i])][0]) + chr(palette[(pixels[i])][1]) + chr(palette[(pixels[i])][2])
        i = Image.frombuffer("RGB", (u.width, u.height), img_data)
        if u.unk_byte_01_f & 0x02:
            i = i.transpose(Image.FLIP_TOP_BOTTOM)
        i.save(args.output_directory + "/%s.png" % s.name)
        
        #if u.unk_byte_01_f & 0x02:
        #    img_data = ""
        #    for i in xrange(0, len(pixels)):
        #        img_data += chr(palette[ord(pixels[i])][0]) + chr(palette[ord(pixels[i])][1]) + chr(palette[ord(pixels[i])][2])
        #    i = Image.frombuffer("RGB", (u.width, u.height), img_data)
        #    i = i.transpose(Image.FLIP_TOP_BOTTOM)
        #    i.save(args.output_directory + "/%s.png" % s.name)
        #else:
        #    img_data = ""
        #    for i in xrange(0, len(pixels)):
        #        img_data += chr(palette[ord(pixels[i])][0]) + chr(palette[ord(pixels[i])][1]) + chr(palette[ord(pixels[i])][2])
        #    i = Image.frombuffer("RGB", (u.width, u.height), img_data)
        #    #i = i.transpose(Image.FLIP_TOP_BOTTOM)
        #    i.save(args.output_directory + "/FUCKED/%s.png" % s.name)
        #das.stream.seek(saved, 0x00)
        
        print "-" * 20
    exit(0)
    
    
    for i, img in enumerate(das.das_file.images()):
        if img.offset_data == 0x00:
            continue
        print "index : %d (0x%04X)" % (i, i)
        print img
        saved = das.stream.tell()
        das.stream.seek(img.offset_data, 0x00)
        buf = das.stream.read(0x10)
        print hexdump(buf)
        print unk_header.parse(buf)
        das.stream.seek(saved, 0x00)
        print "-" * 20
        nb = nb + 1
    print "[+] nb : %d (0x%X)" % (nb, nb)