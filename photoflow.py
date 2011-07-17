#!/usr/bin/python

# This script is released under the Apache 2.0 License.
# I'm too lazy to paste the license text here.
#
# Author: Marco Dinacci - www.intransitione.com -

import os, time, shutil
join = os.path.join

LAST_MOD_FILE = ".lastmod"

IMAGE_FILTER = ("jpg",)
VIDEO_FILTER = ("mov","avi",)
RAW_FILTER = ("raw",)

class MediaManager(object):
    last_media_name = ""
    _has_gui = False

    def register_gui(self, gui):
        self._gui = gui
        self._has_gui = True

    def import_photos(self):
        self._import_content(IMAGE_FILTER)

    def import_videos(self):
        self._import_content(VIDEO_FILTER)

    def import_media(self, media, dest):
        mod_time = os.path.getmtime(media)
        time_struct = time.gmtime(mod_time)
        day = str(time_struct.tm_mday)
        month = str(time_struct.tm_mon)
        year = str(time_struct.tm_year)
        
        # media is new, check if destination directories exists
        
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
        
        final_dest = join(dest, year, month, day, os.path.basename(media))
        #print "Copying %s to %s" % (media, final_dest)
        if media != final_dest:
            shutil.copyfile(media, final_dest)
            if self._has_gui:
                self._gui.update(final_dest)
        else:
            print "Source and destination files are the same, skipping"

    def _import_content(self, media_filters):
        self.media_filters = media_filters
        
        def is_valid(media):
            media_lower = media.lower()
            for media_filter in self.media_filters:
                print media_lower, media_filter, media_lower.endswith(media_filter)
                if media_lower.endswith(media_filter):
                    return True
            return False

        self.list_of_medias = []
        def scan(media, temp_last_media):
            target = ""
            for f in os.listdir(media):
                target = join(media, f) 
                if os.path.isdir(target):
                    scan(target,"")
                else:
                    if f > self.last_media_name and is_valid(f):
                        self.list_of_medias.append((target, self.destination))
                        #import_media(target, self.destination)
                        if f > temp_last_media:
                            temp_last_media = f
                            self.temp_last_media_name = temp_last_media
        
        scan(self.source, "") 
        if self._has_gui:
            self._gui.set_total(len(self.list_of_medias))
        self.import_media_list(self.list_of_medias)
        
        # update LAST_MOD_FILE
        if hasattr(self, "temp_last_media_name"):
            print "Updating last media name"
            f = open(self.last_mod_file,"w")
            f.write(self.temp_last_media_name)
            f.close()

            if self._has_gui:
                self._gui.message("lastmod updated to: %s" % self.temp_last_media_name)
        else:
            msg = "Medias are up to date"
            if self._has_gui:
                self._gui.alert(msg)
            print msg

        if self._has_gui:
            self._gui.exit()
        
    def import_media_list(self, medias):
        for media in medias:
            self.import_media(media[0], media[1])

    def set_source(self, source):
        self.source = source
        
    def set_destination(self, dest):
        self.destination = dest
        self.last_mod_file = os.path.join(self.destination, LAST_MOD_FILE)
        if os.path.exists(self.last_mod_file):
            f = open(self.last_mod_file)
            self.last_media_name = f.readline()
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
    dest="photos", nargs=2 )
    parser.add_option("-v", "--video-import", help="Import videos from card, \
    argument is the destination path", dest="videos", nargs=2)
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True,
                                        help="don't print status messages to stdout")

    (option,args) = parser.parse_args(sys.argv)
    
    mm = MediaManager()

    if option.photos:
        mm.select_source(option.photos[0])
        mm.select_destination(option.photos[1])
        mm.import_photos()

    if option.videos:
        mm.select_source(option.videos[0])
        mm.select_destination(option.videos[1])
        mm.import_videos()
 
