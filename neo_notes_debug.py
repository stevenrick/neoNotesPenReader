import datetime
import Tkinter
import tkFileDialog
import os
import struct


def read_page_data(in_file):
    with open(in_file, "rb") as f:
        fileId = f.read(3)
        fileVersion = f.read(4)
        noteId = f.read(4)
        pageNum = f.read(4)
        notebookWidth = f.read(4)
        notebookHeight = f.read(4)
        createdTime = f.read(8)
        modifiedTime = f.read(8)
        dirtyBit = f.read(1)
        numStrokes = f.read(4)

        print fileId.decode("utf-8")
        print struct.unpack('i', fileVersion)[0]
        print 'note id:', struct.unpack('i', noteId)[0]
        print 'page num:', struct.unpack('i', pageNum)[0]
        print 'notebook width:', struct.unpack('i', notebookWidth)[0]
        print 'notebook height:', struct.unpack('i', notebookHeight)[0]
        print 'raw created timestamp:', struct.unpack('q', createdTime)[0]
        print 'created time:', datetime.datetime.fromtimestamp(
            struct.unpack('q', createdTime)[0]/ 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        print 'modified time:', datetime.datetime.fromtimestamp(
            struct.unpack('q', modifiedTime)[0]/ 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        print 'dirty bit:', ord(dirtyBit)
        strokes = struct.unpack('i', numStrokes)[0]
        print 'strokes:', strokes
        n = 0
        while n < strokes:
            print 'stroke number:', n
            type = ord(f.read(1))
            if type == 0:
                print 'type of data: stroke'
                r = ord(f.read(1))
                g = ord(f.read(1))
                b = ord(f.read(1))
                a = ord(f.read(1))
                color = [r,g,b,a]
                print 'color:', color
                thickness = ord(f.read(1))
                print 'thickness:', thickness
                numDots = struct.unpack('i', f.read(4))[0]
                print 'dots:', numDots
                strokeStartTime = struct.unpack('q', f.read(8))[0]
                print strokeStartTime
                m = 0
                while m < numDots:
                    print 'dot number:', m
                    x_coord = struct.unpack('i', f.read(4))[0]
                    y_coord = struct.unpack('i', f.read(4))[0]
                    pressure = struct.unpack('i', f.read(4))[0]
                    timeDiff = ord(f.read(1))
                    print "(", x_coord, ",", y_coord, ")"
                    print "pressure:", pressure
                    print 'time diff:', timeDiff
                    m += 1
                end_garbage = f.read(2)
                # skip two bytes at end of a stroke cause neonotes has undocumented garbage
            elif type == 1:
                print 'type of data: audio'
                audioTime = f.read(8)
                print datetime.datetime.fromtimestamp(
                    struct.unpack('q', audioTime)[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
                fileName = f.read(60)
                print fileName.decode("utf-8")

                status = ord(f.read(1))
                print 'audio status:', status
                notebook_id = struct.unpack('i', f.read(4))[0]
                print 'audio notebook id:', notebook_id

                notebook_uuid = f.read(30)
                print notebook_uuid.decode("utf-8")

                audioPageNum = struct.unpack('i', f.read(4))[0]
                print 'audio page num:', audioPageNum
            n += 1
        guidStringLen = struct.unpack('i', f.read(4))[0]
        print 'guid string len:', guidStringLen
        if guidStringLen != 0:
            page_guid = f.read(guidStringLen)
            print page_guid
        print 'done'

    return


def main():
    root = Tkinter.Tk()
    root.withdraw()
    directory = tkFileDialog.askdirectory()
    for file_name in os.listdir(directory):
        print file_name
        file_path = os.path.join(directory, file_name)
        read_page_data(file_path)


main()