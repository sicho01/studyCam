#!/usr/bin/env python3
import sys, getopt, os, pty, shutil

SCRIPT_PATH = os.path.abspath(sys.argv[0])
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)

ROOT_DIR = os.path.dirname(SCRIPT_PATH)
NODE_MODULE_DIR = ROOT_DIR + '/node_modules'
ANDROID_BUILD_DIR = ROOT_DIR + '/android'
IOS_BUILD_DIR = ROOT_DIR + '/ios'

METRO_TEMP_DIR = '/tmp/metro-cache'

USAGE_TEXT=SCRIPT_NAME + ''' [-h] [-s n] -- build script for hypermeeting application
where:
    -h               show this help text
    -m --metro       start metro server
    -a --android     build and install application for android devices
    -i --ios         build and install application for ios devices
    -c --clean       remove the previous outputs
'''

def main(argv):
   try:
       opts, args = getopt.getopt(argv,"hmaic", ["metro","android", "ios", "clean"])
   except getopt.GetoptError:
      print(USAGE_TEXT)
      sys.exit(2)

   for opt, arg in opts:
      if opt in ('-h', '--help'):
         print(USAGE_TEXT)
         sys.exit()

      elif opt in ('-m', '--metro'):
         pty.spawn(["yarn", "start", "--reset-cache"])

      elif opt in ('-a', '--android'):
         pty.spawn(['yarn', 'run', 'android'])

      elif opt in ('-i', '--ios'):
         pty.spawn(['yarn', 'run', 'ios'])

      elif opt in ("-c", "--clean"):
         if os.path.isdir(NODE_MODULE_DIR):
            shutil.rmtree(NODE_MODULE_DIR)
         pty.spawn(["yarn"])

         os.chdir(ANDROID_BUILD_DIR)
         pty.spawn(["./gradlew", "clean"])
         os.chdir(ROOT_DIR)

         if os.path.isdir(METRO_TEMP_DIR):
            shutil.rmtree(METRO_TEMP_DIR)

if __name__ == "__main__":
   if len(sys.argv) < 2:
      print(USAGE_TEXT)
      sys.exit(2)
   main(sys.argv[1:])
