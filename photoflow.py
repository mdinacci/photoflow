#!/usr/bin/python

# This script is released under the Apache 2.0 License.
# I'm too lazy to paste the license text here.
#
# Author: Marco Dinacci - www.intransitione.com -

import os, time, shutil

MEDIA_DIR = "/media"
LAST_MOD_FILE = ".lastmod"

class MediaManager(object):
    last_image_name = ""

    def list(self):
        join = os.path.join
        all_medias = os.listdir(MEDIA_DIR)
        
        available_medias = []
        
        for media in all_medias:
            media = join(MEDIA_DIR,media)
            if os.path.isdir(media) and not os.path.islink(media):
                available_medias.append(media)
                
        return available_medias

    def import_content(self):
        join = os.path.join
        
        def import_image(image, dest):
            mod_time = os.path.getmtime(image)
            time_struct = time.gmtime(mod_time)
            day = str(time_struct.tm_mday)
            month = str(time_struct.tm_mon)
            year = str(time_struct.tm_year)
            
            # image is new, check if destination directories exists
            
            dest_dir = join(dest, year)
            if os.path.exists(dest_dir):
                dest_dir = join(dest, year, month)
                if os.path.exists(dest_dir):
                    dest_dir = join(dest, year, month, day)
                    if not os.path.exists(dest_dir):
                        print "Creating directory %s" % dest_dir
                        os.mkdir(dest_dir)
                else:
                    dir = join(dest, year,month)
                    print "Creating directory %s" % dir
                    os.mkdir(dir)
                    dir = join(dest,year,month,day)
                    print "Creating directory %s" % dir
                    os.mkdir(dir)
            else:
                dir = join(dest,year)
                print "Creating directory %s" % dir
                os.mkdir(dir)
                dir = join(dest,year,month)
                print "Creating directory %s" % dir
                os.mkdir(dir)
                dir = join(dest,year,month,day)
                print "Creating directory %s" % dir
                os.mkdir(dir)
            
            final_dest = join(dest, year, month, day, os.path.basename(image))
            print "Copying %s to %s" % (image, final_dest)
            shutil.copyfile(image, final_dest)

        def is_image(image):
            return image.endswith(".JPG")

        def scan(media, temp_last_image):
            target = ""
            for f in os.listdir(media):
                target = join(media, f) 
                if os.path.isdir(target):
                    scan(target,"")
                else:
                    if f > self.last_image_name and is_image(f):
                        import_image(target, self.destination)
                        if f > temp_last_image:
                            temp_last_image = f
                            self.temp_last_image_name = temp_last_image
        
        scan(self.media, "") 
        
        # update LAST_MOD_FILE
        if hasattr(self, "temp_last_image_name"):
            print "Updating last image name"
            f = open(self.last_mod_file,"w")
            f.write(self.temp_last_image_name)
            f.close()
        else:
            print "Photos are up to date"
        
        
    def select_source(self, media):
        self.media = media

    def select_destination(self, dest):
        self.destination = dest
        self.last_mod_file = os.path.join(self.destination, LAST_MOD_FILE)
        if os.path.exists(self.last_mod_file):
            f = open(self.last_mod_file)
            self.last_image_name = f.readline()
        else:
            f = open(self.last_mod_file,"w")
            
        f.close()
 
    def copy(self, src, dest):
        pass
        
        
if __name__ == "__main__":
    import sys
    from optparse import  OptionParser

    parser = OptionParser()
    parser.add_option("-i", "--import", help="Import new photos from card, \
first argument is the path to the source, second the path to destination", 
    dest="imp", nargs=2 )
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True,
                                        help="don't print status messages to stdout")

    (option,args) = parser.parse_args(sys.argv)
    
    if option.imp:
        mm = MediaManager()
        mm.media = option.imp[0]
        mm.select_destination(option.imp[1])
        mm.import_content()
 
